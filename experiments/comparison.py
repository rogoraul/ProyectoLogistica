import csv
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from structure import instance
from algorithms import grasp_timed, grasp_ts

try:
    from scipy.stats import wilcoxon
except Exception:
    wilcoxon = None


# ------------------- #
# COMPARISON SETTINGS #
# ------------------- #

INSTANCES_DIR = "instances"
RANDOM_SEED = 42
TIME_LIMIT = 30
MAX_ITER = 5000
RUNS_PER_INSTANCE = 5

CALIBRATION_SUMMARY_JSON = "experiments/calibration_summary.json"
RESULTS_CSV = "experiments/comparison_results.csv"
RUNS_CSV = "experiments/comparison_runs.csv"
TESTS_JSON = "experiments/comparison_tests.json"

FALLBACK_GRASP_ALPHA = -1
FALLBACK_TS_ALPHA = -1
FALLBACK_TENURE = {
    "small": 15,
    "large": 25,
}

ALL_INSTANCES = [
    ("MDG-a_1_100_m10.txt", "small"),
    ("MDG-a_4_100_m10.txt", "small"),
    ("MDG-a_10_100_m10.txt", "small"),
    ("MDG-a_12_100_m10.txt", "small"),
    ("MDG-a_14_100_m10.txt", "small"),
    ("MDG-a_20_100_m10.txt", "small"),
    ("MDG-a_2_n500_m50.txt", "large"),
    ("MDG-a_5_n500_m50.txt", "large"),
    ("MDG-a_6_n500_m50.txt", "large"),
    ("MDG-a_9_n500_m50.txt", "large"),
    ("MDG-a_13_n500_m50.txt", "large"),
    ("MDG-a_16_n500_m50.txt", "large"),
    ("MDG-a_17_n500_m50.txt", "large"),
    ("MDG-a_19_n500_m50.txt", "large"),
    ("MDG-a_20_n500_m50.txt", "large"),
]


# ------- #
# HELPERS #
# ------- #

def sample_std(values):
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    return round(variance ** 0.5, 4)


def run_algorithm(algo_fn, inst, runs, **kwargs):
    results = []
    for run_idx in range(runs):
        seed = RANDOM_SEED + run_idx
        random.seed(seed)
        start = time.time()
        sol = algo_fn(inst, **kwargs)
        elapsed = round(time.time() - start, 3)
        results.append({
            "run": run_idx,
            "seed": seed,
            "of": round(sol["of"], 2),
            "elapsed_s": elapsed,
        })
    return results


def summarise(run_results, best_known):
    of_values = [row["of"] for row in run_results]
    time_values = [row["elapsed_s"] for row in run_results]
    count = len(of_values)
    avg_of = round(sum(of_values) / count, 2)
    best_run = max(of_values)
    worst_run = min(of_values)
    std_of = sample_std(of_values)
    avg_time = round(sum(time_values) / count, 3)
    dev_pct = round((best_known - avg_of) / best_known * 100, 4) if best_known > 0 else 0.0
    n_best = sum(1 for value in of_values if abs(value - best_known) < 1e-6)
    return avg_of, best_run, worst_run, std_of, avg_time, dev_pct, n_best


def default_group_params():
    return {
        "small": {
            "grasp_alpha": FALLBACK_GRASP_ALPHA,
            "ts_alpha": FALLBACK_TS_ALPHA,
            "ts_tenure": FALLBACK_TENURE["small"],
            "source": "fallback",
        },
        "large": {
            "grasp_alpha": FALLBACK_GRASP_ALPHA,
            "ts_alpha": FALLBACK_TS_ALPHA,
            "ts_tenure": FALLBACK_TENURE["large"],
            "source": "fallback",
        },
    }


def load_group_params():
    params = default_group_params()

    if not os.path.exists(CALIBRATION_SUMMARY_JSON):
        print(f"  Calibration summary not found -> {CALIBRATION_SUMMARY_JSON}")
        print("  Using fallback parameters.")
        return params

    try:
        with open(CALIBRATION_SUMMARY_JSON, "r") as handle:
            data = json.load(handle)
    except Exception as exc:
        print(f"  Could not read calibration summary: {exc}")
        print("  Using fallback parameters.")
        return params

    groups = data.get("groups", {})
    for group_name, group_params in params.items():
        group_data = groups.get(group_name, {})
        grasp_data = group_data.get("grasp", {})
        ts_data = group_data.get("ts", {})

        if "best_alpha" in grasp_data:
            group_params["grasp_alpha"] = grasp_data["best_alpha"]
        if "best_alpha" in ts_data:
            group_params["ts_alpha"] = ts_data["best_alpha"]
        if "best_tenure" in ts_data:
            group_params["ts_tenure"] = ts_data["best_tenure"]
        if group_data:
            group_params["source"] = "calibration_summary"

    print(f"  Loaded calibrated parameters from: {CALIBRATION_SUMMARY_JSON}")
    return params


def collect_pairs(run_rows, group_name=None):
    paired = {}
    for row in run_rows:
        if group_name is not None and row["group"] != group_name:
            continue
        key = (row["instance"], row["seed"])
        paired.setdefault(key, {})[row["algorithm"]] = row["of"]

    grasp_values = []
    ts_values = []
    for key in sorted(paired):
        pair = paired[key]
        if "GRASP" in pair and "GRASP+TS" in pair:
            grasp_values.append(pair["GRASP"])
            ts_values.append(pair["GRASP+TS"])
    return grasp_values, ts_values


def run_paired_test(grasp_values, ts_values):
    result = {
        "n_pairs": len(grasp_values),
        "wins_grasp": 0,
        "wins_ts": 0,
        "ties": 0,
        "mean_delta_ts_minus_grasp": 0.0,
    }

    if len(grasp_values) != len(ts_values):
        result["status"] = "invalid"
        result["reason"] = "unpaired_lengths"
        return result

    if not grasp_values:
        result["status"] = "skipped"
        result["reason"] = "no_pairs"
        return result

    deltas = [round(ts - grasp, 6) for grasp, ts in zip(grasp_values, ts_values)]
    result["wins_grasp"] = sum(1 for delta in deltas if delta < 0)
    result["wins_ts"] = sum(1 for delta in deltas if delta > 0)
    result["ties"] = sum(1 for delta in deltas if abs(delta) < 1e-12)
    result["mean_delta_ts_minus_grasp"] = round(sum(deltas) / len(deltas), 4)

    non_zero_grasp = []
    non_zero_ts = []
    for grasp, ts in zip(grasp_values, ts_values):
        if abs(ts - grasp) > 1e-12:
            non_zero_grasp.append(grasp)
            non_zero_ts.append(ts)

    if not non_zero_grasp:
        result["status"] = "skipped"
        result["reason"] = "all_pairs_tied"
        return result

    if wilcoxon is None:
        result["status"] = "unavailable"
        result["reason"] = "scipy_not_installed"
        return result

    try:
        statistic, pvalue = wilcoxon(non_zero_grasp, non_zero_ts, zero_method="wilcox")
        result["status"] = "ok"
        result["test"] = "wilcoxon"
        result["non_zero_pairs"] = len(non_zero_grasp)
        result["statistic"] = round(float(statistic), 6)
        result["pvalue"] = round(float(pvalue), 6)
    except Exception as exc:
        result["status"] = "error"
        result["reason"] = str(exc)

    return result


def print_test_result(label, result):
    prefix = f"  {label}: n={result['n_pairs']}  wins_TS={result['wins_ts']}  wins_GRASP={result['wins_grasp']}  ties={result['ties']}  mean_delta={result['mean_delta_ts_minus_grasp']}"
    if result["status"] == "ok":
        print(f"{prefix}  Wilcoxon p={result['pvalue']}")
    else:
        print(f"{prefix}  test={result['status']} ({result.get('reason', 'n/a')})")


def write_csv(path, rows, fieldnames):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# ---- #
# MAIN #
# ---- #

def compare():
    group_params = load_group_params()
    rows = []
    run_rows = []

    print(f"\n{'=' * 78}")
    print(f"  COMPARISON: GRASP vs GRASP+TS  |  time_limit={TIME_LIMIT}s  |  runs={RUNS_PER_INSTANCE}")
    print(f"{'=' * 78}\n")

    print("  Parameters by group:")
    for group_name in ("small", "large"):
        params = group_params[group_name]
        print(
            f"    {group_name}: GRASP alpha={params['grasp_alpha']}  "
            f"GRASP+TS alpha={params['ts_alpha']}  tenure={params['ts_tenure']}  "
            f"source={params['source']}"
        )
    print()

    for fname, group in ALL_INSTANCES:
        path = os.path.join(INSTANCES_DIR, fname)
        if not os.path.exists(path):
            print(f"  SKIP (not found): {path}")
            continue

        params = group_params[group]
        grasp_alpha = params["grasp_alpha"]
        ts_alpha = params["ts_alpha"]
        tenure = params["ts_tenure"]
        inst = instance.readInstance(path)

        print(
            f"  Instance: {fname}  [{group}]  "
            f"grasp_alpha={grasp_alpha}  ts_alpha={ts_alpha}  tenure={tenure}"
        )

        print("    Running GRASP...", end=" ", flush=True)
        grasp_results = run_algorithm(
            grasp_timed.execute,
            inst,
            runs=RUNS_PER_INSTANCE,
            alpha=grasp_alpha,
            time_limit=TIME_LIMIT,
        )
        print("done")

        print("    Running GRASP+TS...", end=" ", flush=True)
        ts_results = run_algorithm(
            grasp_ts.execute,
            inst,
            runs=RUNS_PER_INSTANCE,
            alpha=ts_alpha,
            time_limit=TIME_LIMIT,
            tabu_tenure=tenure,
            max_iter=MAX_ITER,
        )
        print("done")

        best_known = max(
            max(row["of"] for row in grasp_results),
            max(row["of"] for row in ts_results),
        )

        g_avg_of, g_best, g_worst, g_std, g_avg_t, g_dev, g_nbest = summarise(grasp_results, best_known)
        t_avg_of, t_best, t_worst, t_std, t_avg_t, t_dev, t_nbest = summarise(ts_results, best_known)

        print(
            f"    GRASP   : avg={g_avg_of}  best={g_best}  worst={g_worst}  "
            f"std={g_std}  dev={g_dev:.4f}%  #best={g_nbest}  time={g_avg_t}s"
        )
        print(
            f"    GRASP+TS: avg={t_avg_of}  best={t_best}  worst={t_worst}  "
            f"std={t_std}  dev={t_dev:.4f}%  #best={t_nbest}  time={t_avg_t}s"
        )
        print()

        rows.append({
            "instance": fname,
            "group": group,
            "best_known": best_known,
            "grasp_alpha": grasp_alpha,
            "ts_alpha": ts_alpha,
            "ts_tenure": tenure,
            "grasp_avg_of": g_avg_of,
            "grasp_best": g_best,
            "grasp_worst": g_worst,
            "grasp_std": g_std,
            "grasp_dev_pct": g_dev,
            "grasp_nbest": g_nbest,
            "grasp_avg_time": g_avg_t,
            "ts_avg_of": t_avg_of,
            "ts_best": t_best,
            "ts_worst": t_worst,
            "ts_std": t_std,
            "ts_dev_pct": t_dev,
            "ts_nbest": t_nbest,
            "ts_avg_time": t_avg_t,
        })

        for row in grasp_results:
            run_rows.append({
                "instance": fname,
                "group": group,
                "algorithm": "GRASP",
                "run": row["run"],
                "seed": row["seed"],
                "alpha": grasp_alpha,
                "tabu_tenure": "",
                "of": row["of"],
                "elapsed_s": row["elapsed_s"],
            })
        for row in ts_results:
            run_rows.append({
                "instance": fname,
                "group": group,
                "algorithm": "GRASP+TS",
                "run": row["run"],
                "seed": row["seed"],
                "alpha": ts_alpha,
                "tabu_tenure": tenure,
                "of": row["of"],
                "elapsed_s": row["elapsed_s"],
            })

    print(f"\n{'=' * 78}")
    print("  AGGREGATE SUMMARY")
    print(f"{'=' * 78}")

    if rows:
        def group_stats(group_name):
            group_rows = [row for row in rows if row["group"] == group_name]
            if not group_rows:
                return
            count = len(group_rows)
            grasp_dev = round(sum(row["grasp_dev_pct"] for row in group_rows) / count, 4)
            ts_dev = round(sum(row["ts_dev_pct"] for row in group_rows) / count, 4)
            grasp_nb = sum(row["grasp_nbest"] for row in group_rows)
            ts_nb = sum(row["ts_nbest"] for row in group_rows)
            grasp_t = round(sum(row["grasp_avg_time"] for row in group_rows) / count, 3)
            ts_t = round(sum(row["ts_avg_time"] for row in group_rows) / count, 3)
            print(f"\n  Group: {group_name} ({count} instances)")
            print(f"  {'Metric':<18} {'GRASP':>12} {'GRASP+TS':>12}")
            print(f"  {'-' * 18}  {'-' * 12}  {'-' * 12}")
            print(f"  {'Avg Dev%':<18} {grasp_dev:>12.4f} {ts_dev:>12.4f}")
            print(f"  {'#Best (total)':<18} {grasp_nb:>12} {ts_nb:>12}")
            print(f"  {'Avg Time (s)':<18} {grasp_t:>12.3f} {ts_t:>12.3f}")

        group_stats("small")
        group_stats("large")

        count_all = len(rows)
        grasp_dev_all = round(sum(row["grasp_dev_pct"] for row in rows) / count_all, 4)
        ts_dev_all = round(sum(row["ts_dev_pct"] for row in rows) / count_all, 4)
        grasp_nb_all = sum(row["grasp_nbest"] for row in rows)
        ts_nb_all = sum(row["ts_nbest"] for row in rows)
        print(f"\n  OVERALL ({count_all} instances)")
        print(f"  {'Metric':<18} {'GRASP':>12} {'GRASP+TS':>12}")
        print(f"  {'-' * 18}  {'-' * 12}  {'-' * 12}")
        print(f"  {'Avg Dev%':<18} {grasp_dev_all:>12.4f} {ts_dev_all:>12.4f}")
        print(f"  {'#Best (total)':<18} {grasp_nb_all:>12} {ts_nb_all:>12}")

    test_results = {
        "overall": run_paired_test(*collect_pairs(run_rows)),
        "small": run_paired_test(*collect_pairs(run_rows, "small")),
        "large": run_paired_test(*collect_pairs(run_rows, "large")),
    }

    print(f"\n{'=' * 78}")
    print("  PAIRED TEST SUMMARY")
    print(f"{'=' * 78}")
    print_test_result("overall", test_results["overall"])
    print_test_result("small", test_results["small"])
    print_test_result("large", test_results["large"])

    if rows:
        write_csv(
            RESULTS_CSV,
            rows,
            list(rows[0].keys()),
        )
    if run_rows:
        write_csv(
            RUNS_CSV,
            run_rows,
            ["instance", "group", "algorithm", "run", "seed", "alpha", "tabu_tenure", "of", "elapsed_s"],
        )

    os.makedirs(os.path.dirname(TESTS_JSON), exist_ok=True)
    with open(TESTS_JSON, "w") as handle:
        json.dump(test_results, handle, indent=2)

    if run_rows:
        print(f"\n  Per-run data saved to: {RUNS_CSV}")
    if rows:
        print(f"  Aggregate results saved to: {RESULTS_CSV}")
    print(f"  Paired-test summary saved to: {TESTS_JSON}")
    print(f"{'=' * 78}\n")


if __name__ == "__main__":
    compare()
