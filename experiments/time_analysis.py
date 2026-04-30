import csv
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms import grasp_timed, grasp_ts
from structure import instance


INSTANCES_DIR = "instances"
CSV_DIR = "csv_final"
OUTPUT_CSV = os.path.join(CSV_DIR, "convergence_curves_large.csv")

INSTANCE_FILES = [
    "MDG-a_16_n500_m50.txt",
    "MDG-a_13_n500_m50.txt",
]

TIME_LIMIT = float(os.environ.get("TIME_ANALYSIS_LIMIT", 180))
RANDOM_SEED = 1

GRASP_ALPHA = 0.1
TS_ALPHA = 0.9
TABU_TENURE = 10
MAX_ITER = 5000


def write_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Instance", "Algorithm", "Elapsed_Time", "Best_Objective"],
        )
        writer.writeheader()
        writer.writerows(rows)


def add_instance_name(rows, instance_name):
    return [
        {
            "Instance": instance_name,
            "Algorithm": row["Algorithm"],
            "Elapsed_Time": row["Elapsed_Time"],
            "Best_Objective": row["Best_Objective"],
        }
        for row in rows
    ]


def run_grasp(instance_name):
    inst = instance.readInstance(os.path.join(INSTANCES_DIR, instance_name))
    convergence_log = []
    random.seed(RANDOM_SEED)
    best = grasp_timed.execute(
        inst,
        GRASP_ALPHA,
        time_limit=TIME_LIMIT,
        convergence_log=convergence_log,
        algorithm_name="GRASP",
    )
    return best, add_instance_name(convergence_log, instance_name)


def run_grasp_ts(instance_name):
    inst = instance.readInstance(os.path.join(INSTANCES_DIR, instance_name))
    convergence_log = []
    random.seed(RANDOM_SEED)
    best = grasp_ts.execute(
        inst,
        TS_ALPHA,
        time_limit=TIME_LIMIT,
        tabu_tenure=TABU_TENURE,
        max_iter=MAX_ITER,
        convergence_log=convergence_log,
        algorithm_name="GRASP+TS",
    )
    return best, add_instance_name(convergence_log, instance_name)


def main():
    all_rows = []

    for instance_name in INSTANCE_FILES:
        print(f"Running time analysis for {instance_name} ({TIME_LIMIT:.0f}s per algorithm)")

        grasp_best, grasp_rows = run_grasp(instance_name)
        all_rows.extend(grasp_rows)
        print(f"  GRASP best OF: {round(grasp_best['of'], 2)}  points: {len(grasp_rows)}")

        ts_best, ts_rows = run_grasp_ts(instance_name)
        all_rows.extend(ts_rows)
        print(f"  GRASP+TS best OF: {round(ts_best['of'], 2)}  points: {len(ts_rows)}")

    write_csv(OUTPUT_CSV, all_rows)
    print(f"Convergence curves written to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
