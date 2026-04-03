import os
import csv
import time
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from structure import instance
from algorithms import grasp_ts


# ------------------- #
# CALIBRATION SETTINGS #
# ------------------- #

INSTANCES_DIR = "instances"
RANDOM_SEED   = 42
ALPHA         = -1          # random alpha per GRASP iteration
TIME_LIMIT    = 30          # seconds per run during calibration
MAX_ITER      = 5000        # max non-improving iterations inside TS
RUNS_PER_CONF = 5           # independent runs to average out randomness

# Tenure values to test (static memory)
TENURE_VALUES = [5, 10, 15, 20, 25, 30]

# Instance groups - edit these lists to match your exact filenames
SMALL_INSTANCES = [
    "MDG-a_1_100_m10.txt",
    "MDG-a_4_100_m10.txt",
    "MDG-a_10_100_m10.txt",
    "MDG-a_12_100_m10.txt",
    "MDG-a_14_100_m10.txt",
]

LARGE_INSTANCES = [
    "MDG-a_2_n500_m50.txt",
    "MDG-a_5_n500_m50.txt",
    "MDG-a_6_n500_m50.txt",
    "MDG-a_9_n500_m50.txt",
    "MDG-a_13_n500_m50.txt",
]


# ---------- #
# HELPERS    #
# ---------- #

def load_instances(names):
    instances = []
    for name in names:
        path = os.path.join(INSTANCES_DIR, name)
        if not os.path.exists(path):
            print(f"  WARNING: file not found -> {path}")
            continue
        inst = instance.readInstance(path)
        instances.append((name, inst))
    return instances


def run_tenure(inst_list, tenure, runs, dynamic=False):
    """
    Run GRASP+TS with a given tenure on every instance in inst_list.
    Returns a list of (instance_name, avg_of, avg_time) tuples.
    """
    results = []
    for name, inst in inst_list:
        of_values = []
        times = []
        for r in range(runs):
            random.seed(RANDOM_SEED + r)
            t0 = time.time()
            sol = grasp_ts.execute(
                inst,
                alpha=ALPHA,
                time_limit=TIME_LIMIT,
                tabu_tenure=tenure,
                max_iter=MAX_ITER,
                dynamic=dynamic,
                tenure_min=max(2, tenure - 5),
                tenure_max=tenure + 5,
            )
            elapsed = time.time() - t0
            of_values.append(sol['of'])
            times.append(elapsed)
        avg_of   = round(sum(of_values) / runs, 2)
        avg_time = round(sum(times) / runs, 2)
        results.append((name, avg_of, avg_time))
        print(f"    {name:35s}  avg_OF={avg_of:10.2f}  avg_time={avg_time:.1f}s")
    return results


def compute_dev(results_by_tenure):
    """
    Given {tenure: [(name, avg_of, avg_time), ...]},
    compute the Dev% of each tenure relative to the best known OF per instance.
    Returns {tenure: avg_dev_pct}
    """
    # Collect best OF per instance across all tenures
    best_of = {}
    for tenure, rows in results_by_tenure.items():
        for name, avg_of, _ in rows:
            best_of[name] = max(best_of.get(name, 0), avg_of)

    avg_devs = {}
    for tenure, rows in results_by_tenure.items():
        devs = []
        for name, avg_of, _ in rows:
            if best_of[name] > 0:
                dev = (best_of[name] - avg_of) / best_of[name] * 100
            else:
                dev = 0.0
            devs.append(dev)
        avg_devs[tenure] = round(sum(devs) / len(devs), 4) if devs else 0.0
    return avg_devs


def print_summary_table(group_name, results_by_tenure, avg_devs):
    print(f"\n{'='*60}")
    print(f"  CALIBRATION SUMMARY - {group_name}")
    print(f"{'='*60}")
    print(f"  {'Tenure':>8}  {'Avg Dev%':>10}  {'Best?':>6}")
    print(f"  {'-'*8}  {'-'*10}  {'-'*6}")
    best_tenure = min(avg_devs, key=avg_devs.get)
    for tenure, dev in sorted(avg_devs.items()):
        marker = "<-- BEST" if tenure == best_tenure else ""
        print(f"  {tenure:>8}  {dev:>10.4f}  {marker}")
    print(f"{'='*60}")
    return best_tenure


# ---------- #
# MAIN       #
# ---------- #

def calibrate(inst_list, group_name):
    print(f"\n{'#'*60}")
    print(f"  CALIBRATING: {group_name}  ({len(inst_list)} instances)")
    print(f"  Tenure values: {TENURE_VALUES}")
    print(f"  Runs per config: {RUNS_PER_CONF}  |  Time limit: {TIME_LIMIT}s")
    print(f"{'#'*60}")

    results_by_tenure = {}
    raw_rows = []

    for tenure in TENURE_VALUES:
        print(f"\n  -- Static tenure = {tenure} --")
        res = run_tenure(inst_list, tenure, RUNS_PER_CONF)
        results_by_tenure[tenure] = res
        for name, avg_of, avg_time in res:
            raw_rows.append({
                "group":      group_name,
                "tenure":     tenure,
                "instance":   name,
                "avg_of":     avg_of,
                "avg_time_s": avg_time,
            })

    avg_devs = compute_dev(results_by_tenure)
    best = print_summary_table(group_name, results_by_tenure, avg_devs)
    return best, avg_devs, raw_rows


if __name__ == "__main__":
    print("Loading instances...")
    small_list = load_instances(SMALL_INSTANCES)
    large_list = load_instances(LARGE_INSTANCES)

    best_small, devs_small, rows_small = calibrate(small_list, "SMALL (n=100)")
    best_large, devs_large, rows_large = calibrate(large_list, "LARGE (n=500)")

    print("\n\n" + "="*60)
    print("  FINAL CALIBRATION RECOMMENDATION")
    print("="*60)
    print(f"  Small instances -> best tabu_tenure = {best_small}  (dev={devs_small[best_small]:.4f}%)")
    print(f"  Large instances -> best tabu_tenure = {best_large}  (dev={devs_large[best_large]:.4f}%)")
    print("="*60)

    # ---------------------- #
    # EXPORT CALIBRATION CSV #
    # ---------------------- #
    all_rows = rows_small + rows_large
    csv_path = "experiments/calibration_results.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    fieldnames = ["group", "tenure", "instance", "avg_of", "avg_time_s"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"\n  Raw calibration data saved to: {csv_path}")
