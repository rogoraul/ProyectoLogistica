import random
import time
import csv
import os

from algorithms import grasp_timed, grasp_ts
from structure import instance, solution


INSTANCE_PATH = "instances/MDG-a_2_n500_m50.txt"
TIME_LIMIT = 120  # seconds for each algorithm run


def run_and_export():
    if not os.path.exists(INSTANCE_PATH):
        print(f"Instance not found: {INSTANCE_PATH}")
        return

    # Load a fresh copy for each algorithm to avoid any in-place mutations
    inst_grasp = instance.readInstance(INSTANCE_PATH)
    inst_ts = instance.readInstance(INSTANCE_PATH)

    # Run GRASP and collect convergence events
    grasp_log = []
    print(f"Running GRASP for {TIME_LIMIT}s...")
    random.seed(1)
    best_grasp = grasp_timed.execute(
        inst_grasp,
        0.1,
        time_limit=TIME_LIMIT,
        convergence_log=grasp_log,
        algorithm_name="GRASP",
    )
    print("GRASP finished. Best OF:", best_grasp['of'])

    # Run GRASP+TS and collect convergence events; request TS evolution CSV for the first restart
    ts_log = []
    CSV_DIR = "csv_final"
    ts_evolution_path = os.path.join(CSV_DIR, "ts_evolution_single_restart.csv")
    os.makedirs(CSV_DIR, exist_ok=True)
    print(f"Running GRASP+TS for {TIME_LIMIT}s (first TS restart will log evolution)...")
    random.seed(1)
    best_ts = grasp_ts.execute(
        inst_ts,
        0.9,
        time_limit=TIME_LIMIT,
        tabu_tenure=10,
        max_iter=5000,
        convergence_log=ts_log,
        algorithm_name="GRASP+TS",
        ts_evolution_csv_path=ts_evolution_path,
    )
    print("GRASP+TS finished. Best OF:", best_ts['of'])

    # Merge convergence logs and write a single CSV
    convergence_rows = []
    for row in (grasp_log + ts_log):
        convergence_rows.append({
            "Algorithm": row.get("Algorithm"),
            "Elapsed_Time": row.get("Elapsed_Time"),
            "Best_Objective": row.get("Best_Objective"),
        })

    os.makedirs(CSV_DIR, exist_ok=True)
    conv_path = os.path.join(CSV_DIR, "convergence_data.csv")
    with open(conv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Algorithm", "Elapsed_Time", "Best_Objective"])
        writer.writeheader()
        writer.writerows(convergence_rows)

    print(f"Convergence data written to: {conv_path}")
    print(f"TS evolution (single restart) written to: {ts_evolution_path}")


if __name__ == '__main__':
    run_and_export()
