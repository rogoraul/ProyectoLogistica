import csv
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms import grasp_timed, grasp_ts
from structure import instance


INSTANCE_PATH = "instances/MDG-a_2_n500_m50.txt"
TIME_LIMIT = 120
MAX_ITER = 5000
RANDOM_SEED = 1

GRASP_ALPHA = 0.1
TS_ALPHA = 0.9
TABU_TENURE = 10

CONVERGENCE_CSV = "experiments/convergence_data.csv"
TS_EVOLUTION_CSV = "experiments/ts_evolution_single_restart.csv"


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    inst = instance.readInstance(INSTANCE_PATH)
    convergence_rows = []

    random.seed(RANDOM_SEED)
    grasp_best = grasp_timed.execute(
        inst,
        GRASP_ALPHA,
        time_limit=TIME_LIMIT,
        convergence_log=convergence_rows,
        algorithm_name="GRASP",
    )

    random.seed(RANDOM_SEED)
    ts_best = grasp_ts.execute(
        inst,
        TS_ALPHA,
        time_limit=TIME_LIMIT,
        tabu_tenure=TABU_TENURE,
        max_iter=MAX_ITER,
        convergence_log=convergence_rows,
        algorithm_name="GRASP+TS",
        ts_evolution_csv_path=TS_EVOLUTION_CSV,
    )

    write_csv(
        CONVERGENCE_CSV,
        convergence_rows,
        ["Algorithm", "Elapsed_Time", "Best_Objective"],
    )

    print(f"GRASP best OF: {round(grasp_best['of'], 2)}")
    print(f"GRASP+TS best OF: {round(ts_best['of'], 2)}")
    print(f"Convergence CSV -> {CONVERGENCE_CSV}")
    print(f"TS evolution CSV -> {TS_EVOLUTION_CSV}")


if __name__ == "__main__":
    main()
