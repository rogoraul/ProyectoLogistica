import os
import time
import random
import sys
import csv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from structure import instance
from algorithms import grasp_timed, grasp_ts


# ------------------- #
# COMPARISON SETTINGS #
# ------------------- #

INSTANCES_DIR  = "instances"
RANDOM_SEED    = 42
ALPHA          = -1       # random alpha per GRASP iteration
TIME_LIMIT     = 30       # seconds - same for BOTH algorithms (fair comparison)
MAX_ITER       = 5000     # max non-improving iterations for Tabu Search

# Set these to the best values found in calibration.py
TABU_TENURE_SMALL = 15   # calibrated: best dev=0.0000% on n=100 instances
TABU_TENURE_LARGE = 25   # calibrated: best dev=0.0969% on n=500 instances

RUNS_PER_INSTANCE = 5    # independent runs per algorithm per instance

RESULTS_CSV     = "experiments/comparison_results.csv"
RUNS_CSV        = "experiments/comparison_runs.csv"    # one row per individual run

# All 15 instances - edit filenames to match yours exactly
ALL_INSTANCES = [
    # Small (n=100, m=10)
    ("MDG-a_1_100_m10.txt",   "small"),
    ("MDG-a_4_100_m10.txt",   "small"),
    ("MDG-a_10_100_m10.txt",  "small"),
    ("MDG-a_12_100_m10.txt",  "small"),
    ("MDG-a_14_100_m10.txt",  "small"),
    ("MDG-a_20_100_m10.txt",  "small"),
    # Large (n=500, m=50)
    ("MDG-a_2_n500_m50.txt",  "large"),
    ("MDG-a_5_n500_m50.txt",  "large"),
    ("MDG-a_6_n500_m50.txt",  "large"),
    ("MDG-a_9_n500_m50.txt",  "large"),
    ("MDG-a_13_n500_m50.txt", "large"),
    ("MDG-a_16_n500_m50.txt", "large"),
    ("MDG-a_17_n500_m50.txt", "large"),
    ("MDG-a_19_n500_m50.txt", "large"),
    ("MDG-a_20_n500_m50.txt", "large"),
]


# ---------- #
# HELPERS    #
# ---------- #

def run_algorithm(algo_fn, inst, runs, **kwargs):
    """
    Execute algo_fn(inst, **kwargs) for `runs` independent seeds.
    Returns list of (of_value, elapsed_seconds).
    """
    results = []
    for r in range(runs):
        random.seed(RANDOM_SEED + r)
        t0 = time.time()
        sol = algo_fn(inst, **kwargs)
        elapsed = round(time.time() - t0, 3)
        results.append((round(sol['of'], 2), elapsed))
    return results


def summarise(run_results, best_known):
    """
    From a list of (of, time) compute descriptive stats and dev%.
    best_known is the best OF across both algorithms for this instance.
    """
    of_vals   = [r[0] for r in run_results]
    time_vals = [r[1] for r in run_results]
    n         = len(of_vals)
    avg_of    = round(sum(of_vals) / n, 2)
    avg_time  = round(sum(time_vals) / n, 2)
    best_run  = max(of_vals)
    worst_run = min(of_vals)
    variance  = sum((x - avg_of) ** 2 for x in of_vals) / (n - 1) if n > 1 else 0.0
    std_of    = round(variance ** 0.5, 4)
    dev_pct   = round((best_known - avg_of) / best_known * 100, 4) if best_known > 0 else 0.0
    n_best    = sum(1 for v in of_vals if abs(v - best_known) < 1e-6)
    return avg_of, best_run, worst_run, std_of, avg_time, dev_pct, n_best


# ---------- #
# MAIN       #
# ---------- #

def compare():
    rows = []       # aggregate rows — one per instance
    run_rows = []   # per-run rows for Wilcoxon-ready output

    print(f"\n{'='*70}")
    print(f"  COMPARISON: GRASP vs GRASP+TS  |  time_limit={TIME_LIMIT}s  |  runs={RUNS_PER_INSTANCE}")
    print(f"{'='*70}\n")

    # ------------------- #
    # PER-INSTANCE LOOP   #
    # ------------------- #
    for fname, group in ALL_INSTANCES:
        path = os.path.join(INSTANCES_DIR, fname)
        if not os.path.exists(path):
            print(f"  SKIP (not found): {path}")
            continue

        tenure = TABU_TENURE_SMALL if group == "small" else TABU_TENURE_LARGE
        inst = instance.readInstance(path)

        print(f"  Instance: {fname}  [{group}]  tenure={tenure}")

        # Run GRASP baseline
        print("    Running GRASP...", end=" ", flush=True)
        grasp_results = run_algorithm(
            grasp_timed.execute, inst,
            runs=RUNS_PER_INSTANCE,
            alpha=ALPHA,
            time_limit=TIME_LIMIT
        )
        print("done")

        # Run GRASP + TS
        print("    Running GRASP+TS...", end=" ", flush=True)
        ts_results = run_algorithm(
            grasp_ts.execute, inst,
            runs=RUNS_PER_INSTANCE,
            alpha=ALPHA,
            time_limit=TIME_LIMIT,
            tabu_tenure=tenure,
            max_iter=MAX_ITER
        )
        print("done")

        # Best known = max across all runs of both algorithms
        best_known = max(
            max(r[0] for r in grasp_results),
            max(r[0] for r in ts_results)
        )

        g_avg_of, g_best, g_worst, g_std, g_avg_t, g_dev, g_nbest = summarise(grasp_results, best_known)
        t_avg_of, t_best, t_worst, t_std, t_avg_t, t_dev, t_nbest = summarise(ts_results,   best_known)

        print(f"    GRASP   : avg={g_avg_of}  best={g_best}  worst={g_worst}  std={g_std}  dev={g_dev:.4f}%  #best={g_nbest}  time={g_avg_t}s")
        print(f"    GRASP+TS: avg={t_avg_of}  best={t_best}  worst={t_worst}  std={t_std}  dev={t_dev:.4f}%  #best={t_nbest}  time={t_avg_t}s")
        print()

        rows.append({
            "instance":        fname,
            "group":           group,
            "best_known":      best_known,
            "grasp_avg_of":    g_avg_of,
            "grasp_best":      g_best,
            "grasp_worst":     g_worst,
            "grasp_std":       g_std,
            "grasp_dev_pct":   g_dev,
            "grasp_nbest":     g_nbest,
            "grasp_avg_time":  g_avg_t,
            "ts_avg_of":       t_avg_of,
            "ts_best":         t_best,
            "ts_worst":        t_worst,
            "ts_std":          t_std,
            "ts_dev_pct":      t_dev,
            "ts_nbest":        t_nbest,
            "ts_avg_time":     t_avg_t,
            "tabu_tenure":     tenure,
        })

        # Collect per-run rows (paired by seed for Wilcoxon test)
        for r_idx, (g_of, g_t) in enumerate(grasp_results):
            run_rows.append({"instance": fname, "group": group, "algorithm": "GRASP",
                             "run": r_idx, "seed": RANDOM_SEED + r_idx, "of": g_of, "elapsed_s": g_t})
        for r_idx, (t_of, t_t) in enumerate(ts_results):
            run_rows.append({"instance": fname, "group": group, "algorithm": "GRASP+TS",
                             "run": r_idx, "seed": RANDOM_SEED + r_idx, "of": t_of, "elapsed_s": t_t})

    # --------------- #
    # SUMMARY TABLE   #
    # --------------- #
    print(f"\n{'='*70}")
    print("  AGGREGATE SUMMARY")
    print(f"{'='*70}")

    if rows:
        def group_stats(group_name):
            g = [r for r in rows if r["group"] == group_name]
            if not g:
                return
            n = len(g)
            grasp_dev = round(sum(r["grasp_dev_pct"] for r in g) / n, 4)
            ts_dev    = round(sum(r["ts_dev_pct"]    for r in g) / n, 4)
            grasp_nb  = sum(r["grasp_nbest"] for r in g)
            ts_nb     = sum(r["ts_nbest"]    for r in g)
            grasp_t   = round(sum(r["grasp_avg_time"] for r in g) / n, 2)
            ts_t      = round(sum(r["ts_avg_time"]    for r in g) / n, 2)
            print(f"\n  Group: {group_name} ({n} instances)")
            print(f"  {'Metric':<18} {'GRASP':>12} {'GRASP+TS':>12}")
            print(f"  {'-'*18}  {'-'*12}  {'-'*12}")
            print(f"  {'Avg Dev%':<18} {grasp_dev:>12.4f} {ts_dev:>12.4f}")
            print(f"  {'#Best (total)':<18} {grasp_nb:>12} {ts_nb:>12}")
            print(f"  {'Avg Time (s)':<18} {grasp_t:>12.2f} {ts_t:>12.2f}")

        group_stats("small")
        group_stats("large")

        # Overall
        n_all = len(rows)
        grasp_dev_all = round(sum(r["grasp_dev_pct"] for r in rows) / n_all, 4)
        ts_dev_all    = round(sum(r["ts_dev_pct"]    for r in rows) / n_all, 4)
        grasp_nb_all  = sum(r["grasp_nbest"] for r in rows)
        ts_nb_all     = sum(r["ts_nbest"]    for r in rows)
        print(f"\n  OVERALL ({n_all} instances)")
        print(f"  {'Metric':<18} {'GRASP':>12} {'GRASP+TS':>12}")
        print(f"  {'-'*18}  {'-'*12}  {'-'*12}")
        print(f"  {'Avg Dev%':<18} {grasp_dev_all:>12.4f} {ts_dev_all:>12.4f}")
        print(f"  {'#Best (total)':<18} {grasp_nb_all:>12} {ts_nb_all:>12}")

    # ----------- #
    # EXPORT CSV  #
    # ----------- #
    os.makedirs(os.path.dirname(RESULTS_CSV), exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    if run_rows:
        run_fieldnames = ["instance", "group", "algorithm", "run", "seed", "of", "elapsed_s"]
        with open(RUNS_CSV, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=run_fieldnames)
            writer.writeheader()
            writer.writerows(run_rows)
        print(f"  Per-run data saved to: {RUNS_CSV}")

    print(f"\n  Results saved to: {RESULTS_CSV}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    compare()
