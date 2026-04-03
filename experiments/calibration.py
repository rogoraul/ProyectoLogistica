import csv
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from structure import instance
from algorithms import grasp_timed, grasp_ts


# -------------------- #
# CALIBRATION SETTINGS #
# -------------------- #

INSTANCES_DIR = "instances"
RANDOM_SEED = 42
CALIBRATION_MODE = "sequential"   # "sequential" or "joint"
ALPHA_VALUES = [0.1, 0.25, 0.5, 0.75, 0.9, -1]
TENURE_VALUES = [5, 10, 15, 20, 25, 30]
ALPHA_SWEEP_TENURE = 15          # anchor tenure used by sequential TS alpha sweep
TIME_LIMIT = 10                  # shorter budget to keep calibration practical
MAX_ITER = 5000
RUNS_PER_CONF = 3

GRASP_DETAIL_CSV = "experiments/calibration_grasp.csv"
GRASP_SUMMARY_CSV = "experiments/calibration_grasp_summary.csv"
GRASP_RUNS_CSV = "experiments/calibration_grasp_runs.csv"
TS_DETAIL_CSV = "experiments/calibration_ts.csv"
TS_SUMMARY_CSV = "experiments/calibration_ts_summary.csv"
TS_RUNS_CSV = "experiments/calibration_ts_runs.csv"
SUMMARY_JSON = "experiments/calibration_summary.json"

GROUPS = {
    "small": {
        "label": "SMALL (n=100)",
        "instances": [
            "MDG-a_1_100_m10.txt",
            "MDG-a_4_100_m10.txt",
            "MDG-a_10_100_m10.txt",
            "MDG-a_12_100_m10.txt",
            "MDG-a_14_100_m10.txt",
        ],
    },
    "large": {
        "label": "LARGE (n=500)",
        "instances": [
            "MDG-a_2_n500_m50.txt",
            "MDG-a_5_n500_m50.txt",
            "MDG-a_6_n500_m50.txt",
            "MDG-a_9_n500_m50.txt",
            "MDG-a_13_n500_m50.txt",
        ],
    },
}


# ------- #
# HELPERS #
# ------- #

def load_instances(names):
    loaded = []
    for name in names:
        path = os.path.join(INSTANCES_DIR, name)
        if not os.path.exists(path):
            print(f"  WARNING: file not found -> {path}")
            continue
        loaded.append((name, instance.readInstance(path)))
    return loaded


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


def summarise_runs(run_results):
    of_values = [row["of"] for row in run_results]
    time_values = [row["elapsed_s"] for row in run_results]
    count = len(of_values)
    return {
        "avg_of": round(sum(of_values) / count, 2),
        "best_of": max(of_values),
        "worst_of": min(of_values),
        "std_of": sample_std(of_values),
        "avg_time_s": round(sum(time_values) / count, 3),
    }


def compute_avg_dev(detail_rows, config_keys):
    best_by_instance = {}
    for row in detail_rows:
        inst_name = row["instance"]
        best_by_instance[inst_name] = max(best_by_instance.get(inst_name, 0), row["avg_of"])

    totals = {}
    counts = {}
    for row in detail_rows:
        config = tuple(row[key] for key in config_keys)
        best_of = best_by_instance[row["instance"]]
        dev = 0.0 if best_of <= 0 else (best_of - row["avg_of"]) / best_of * 100
        totals[config] = totals.get(config, 0.0) + dev
        counts[config] = counts.get(config, 0) + 1

    return {
        config: round(totals[config] / counts[config], 4)
        for config in totals
    }


def build_config_summary(detail_rows, config_keys, extra_fields=None):
    extra_fields = extra_fields or []
    dev_by_config = compute_avg_dev(detail_rows, config_keys)
    grouped_rows = {}

    for row in detail_rows:
        config = tuple(row[key] for key in config_keys)
        row["avg_dev_pct"] = dev_by_config[config]
        grouped_rows.setdefault(config, []).append(row)

    summary_rows = []
    for config, rows in grouped_rows.items():
        summary_row = {key: value for key, value in zip(config_keys, config)}
        for field in extra_fields:
            summary_row[field] = rows[0][field]
        summary_row["avg_dev_pct"] = dev_by_config[config]
        summary_row["mean_avg_of"] = round(sum(row["avg_of"] for row in rows) / len(rows), 2)
        summary_row["mean_time_s"] = round(sum(row["avg_time_s"] for row in rows) / len(rows), 3)
        summary_rows.append(summary_row)

    summary_rows.sort(key=lambda row: (row["avg_dev_pct"], -row["mean_avg_of"], row["mean_time_s"]))
    best_row = summary_rows[0] if summary_rows else None
    return summary_rows, best_row


def write_csv(path, rows, fieldnames):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_summary_table(title, summary_rows):
    print(f"\n{'=' * 72}")
    print(f"  {title}")
    print(f"{'=' * 72}")
    for row in summary_rows:
        params = []
        if "phase" in row:
            params.append(f"phase={row['phase']}")
        if "alpha" in row:
            params.append(f"alpha={row['alpha']}")
        if "tenure" in row:
            params.append(f"tenure={row['tenure']}")
        param_text = "  ".join(params)
        marker = "  <-- BEST" if row is summary_rows[0] else ""
        print(
            f"  {param_text:<32} avg_dev={row['avg_dev_pct']:>8.4f}%"
            f"  mean_OF={row['mean_avg_of']:>10.2f}{marker}"
        )
    print(f"{'=' * 72}")


# ---------------- #
# CALIBRATION RUNS #
# ---------------- #

def calibrate_grasp(group_key, inst_list):
    detail_rows = []
    run_rows = []

    print(f"\n{'#' * 72}")
    print(f"  CALIBRATING GRASP BASELINE - {GROUPS[group_key]['label']}")
    print(f"  alpha values: {ALPHA_VALUES}")
    print(f"  runs/config: {RUNS_PER_CONF}  |  time_limit: {TIME_LIMIT}s")
    print(f"{'#' * 72}")

    for alpha in ALPHA_VALUES:
        print(f"\n  -- alpha = {alpha} --")
        for name, inst in inst_list:
            run_results = run_algorithm(
                grasp_timed.execute,
                inst,
                RUNS_PER_CONF,
                alpha=alpha,
                time_limit=TIME_LIMIT,
            )
            stats = summarise_runs(run_results)
            detail_rows.append({
                "group": group_key,
                "instance": name,
                "alpha": alpha,
                **stats,
            })
            for run in run_results:
                run_rows.append({
                    "group": group_key,
                    "instance": name,
                    "alpha": alpha,
                    **run,
                })
            print(
                f"    {name:35s} avg_OF={stats['avg_of']:10.2f}  "
                f"std={stats['std_of']:7.4f}  avg_time={stats['avg_time_s']:.3f}s"
            )

    summary_rows, best_row = build_config_summary(detail_rows, ("alpha",), extra_fields=["group"])
    print_summary_table(f"GRASP SUMMARY - {GROUPS[group_key]['label']}", summary_rows)
    return best_row, detail_rows, summary_rows, run_rows


def evaluate_ts_configs(group_key, inst_list, phase, alpha_values, tenure_values):
    detail_rows = []
    run_rows = []

    for alpha in alpha_values:
        for tenure in tenure_values:
            print(f"\n  -- phase={phase}  alpha={alpha}  tenure={tenure} --")
            for name, inst in inst_list:
                run_results = run_algorithm(
                    grasp_ts.execute,
                    inst,
                    RUNS_PER_CONF,
                    alpha=alpha,
                    time_limit=TIME_LIMIT,
                    tabu_tenure=tenure,
                    max_iter=MAX_ITER,
                )
                stats = summarise_runs(run_results)
                detail_rows.append({
                    "group": group_key,
                    "phase": phase,
                    "instance": name,
                    "alpha": alpha,
                    "tenure": tenure,
                    **stats,
                })
                for run in run_results:
                    run_rows.append({
                        "group": group_key,
                        "phase": phase,
                        "instance": name,
                        "alpha": alpha,
                        "tenure": tenure,
                        **run,
                    })
                print(
                    f"    {name:35s} avg_OF={stats['avg_of']:10.2f}  "
                    f"std={stats['std_of']:7.4f}  avg_time={stats['avg_time_s']:.3f}s"
                )

    summary_rows, best_row = build_config_summary(
        detail_rows,
        ("alpha", "tenure"),
        extra_fields=["group", "phase"],
    )
    return best_row, detail_rows, summary_rows, run_rows


def calibrate_ts(group_key, inst_list):
    print(f"\n{'#' * 72}")
    print(f"  CALIBRATING GRASP+TS - {GROUPS[group_key]['label']}")
    print(f"  mode: {CALIBRATION_MODE}")
    print(f"  alpha values: {ALPHA_VALUES}")
    print(f"  tenure values: {TENURE_VALUES}")
    print(f"  runs/config: {RUNS_PER_CONF}  |  time_limit: {TIME_LIMIT}s")
    print(f"{'#' * 72}")

    if CALIBRATION_MODE == "joint":
        best_row, detail_rows, summary_rows, run_rows = evaluate_ts_configs(
            group_key,
            inst_list,
            "joint",
            ALPHA_VALUES,
            TENURE_VALUES,
        )
        print_summary_table(f"GRASP+TS SUMMARY - {GROUPS[group_key]['label']}", summary_rows)
        return {
            "best_alpha": best_row["alpha"],
            "best_tenure": best_row["tenure"],
            "best_avg_dev_pct": best_row["avg_dev_pct"],
            "phase_best_rows": {"joint": best_row},
            "detail_rows": detail_rows,
            "summary_rows": summary_rows,
            "run_rows": run_rows,
        }

    alpha_best, alpha_detail, alpha_summary, alpha_runs = evaluate_ts_configs(
        group_key,
        inst_list,
        "alpha_sweep",
        ALPHA_VALUES,
        [ALPHA_SWEEP_TENURE],
    )
    print_summary_table(
        f"GRASP+TS ALPHA SWEEP - {GROUPS[group_key]['label']}",
        alpha_summary,
    )

    tenure_best, tenure_detail, tenure_summary, tenure_runs = evaluate_ts_configs(
        group_key,
        inst_list,
        "tenure_sweep",
        [alpha_best["alpha"]],
        TENURE_VALUES,
    )
    print_summary_table(
        f"GRASP+TS TENURE SWEEP - {GROUPS[group_key]['label']}",
        tenure_summary,
    )

    return {
        "best_alpha": tenure_best["alpha"],
        "best_tenure": tenure_best["tenure"],
        "best_avg_dev_pct": tenure_best["avg_dev_pct"],
        "phase_best_rows": {
            "alpha_sweep": alpha_best,
            "tenure_sweep": tenure_best,
        },
        "detail_rows": alpha_detail + tenure_detail,
        "summary_rows": alpha_summary + tenure_summary,
        "run_rows": alpha_runs + tenure_runs,
    }


# ---- #
# MAIN #
# ---- #

if __name__ == "__main__":
    print("Loading calibration subsets...")

    grasp_detail_rows = []
    grasp_summary_rows = []
    grasp_run_rows = []
    ts_detail_rows = []
    ts_summary_rows = []
    ts_run_rows = []

    summary_doc = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "mode": CALIBRATION_MODE,
        "time_limit_s": TIME_LIMIT,
        "runs_per_config": RUNS_PER_CONF,
        "alpha_values": ALPHA_VALUES,
        "tenure_values": TENURE_VALUES,
        "alpha_sweep_tenure": ALPHA_SWEEP_TENURE,
        "groups": {},
    }

    for group_key, group_cfg in GROUPS.items():
        inst_list = load_instances(group_cfg["instances"])
        if not inst_list:
            print(f"Skipping group {group_key}: no instances loaded")
            continue

        best_grasp, g_detail, g_summary, g_runs = calibrate_grasp(group_key, inst_list)
        ts_result = calibrate_ts(group_key, inst_list)

        grasp_detail_rows.extend(g_detail)
        grasp_summary_rows.extend(g_summary)
        grasp_run_rows.extend(g_runs)
        ts_detail_rows.extend(ts_result["detail_rows"])
        ts_summary_rows.extend(ts_result["summary_rows"])
        ts_run_rows.extend(ts_result["run_rows"])

        summary_doc["groups"][group_key] = {
            "label": group_cfg["label"],
            "grasp": {
                "best_alpha": best_grasp["alpha"],
                "best_avg_dev_pct": best_grasp["avg_dev_pct"],
            },
            "ts": {
                "best_alpha": ts_result["best_alpha"],
                "best_tenure": ts_result["best_tenure"],
                "best_avg_dev_pct": ts_result["best_avg_dev_pct"],
            },
        }

        if CALIBRATION_MODE == "sequential":
            summary_doc["groups"][group_key]["ts"]["alpha_sweep"] = {
                "tenure": ts_result["phase_best_rows"]["alpha_sweep"]["tenure"],
                "best_alpha": ts_result["phase_best_rows"]["alpha_sweep"]["alpha"],
                "best_avg_dev_pct": ts_result["phase_best_rows"]["alpha_sweep"]["avg_dev_pct"],
            }
            summary_doc["groups"][group_key]["ts"]["tenure_sweep"] = {
                "alpha": ts_result["phase_best_rows"]["tenure_sweep"]["alpha"],
                "best_tenure": ts_result["phase_best_rows"]["tenure_sweep"]["tenure"],
                "best_avg_dev_pct": ts_result["phase_best_rows"]["tenure_sweep"]["avg_dev_pct"],
            }

    write_csv(
        GRASP_DETAIL_CSV,
        grasp_detail_rows,
        ["group", "instance", "alpha", "avg_of", "best_of", "worst_of", "std_of", "avg_time_s", "avg_dev_pct"],
    )
    write_csv(
        GRASP_SUMMARY_CSV,
        grasp_summary_rows,
        ["group", "alpha", "avg_dev_pct", "mean_avg_of", "mean_time_s"],
    )
    write_csv(
        GRASP_RUNS_CSV,
        grasp_run_rows,
        ["group", "instance", "alpha", "run", "seed", "of", "elapsed_s"],
    )
    write_csv(
        TS_DETAIL_CSV,
        ts_detail_rows,
        ["group", "phase", "instance", "alpha", "tenure", "avg_of", "best_of", "worst_of", "std_of", "avg_time_s", "avg_dev_pct"],
    )
    write_csv(
        TS_SUMMARY_CSV,
        ts_summary_rows,
        ["group", "phase", "alpha", "tenure", "avg_dev_pct", "mean_avg_of", "mean_time_s"],
    )
    write_csv(
        TS_RUNS_CSV,
        ts_run_rows,
        ["group", "phase", "instance", "alpha", "tenure", "run", "seed", "of", "elapsed_s"],
    )

    os.makedirs(os.path.dirname(SUMMARY_JSON), exist_ok=True)
    with open(SUMMARY_JSON, "w") as handle:
        json.dump(summary_doc, handle, indent=2)

    print("\n" + "=" * 72)
    print("  FINAL CALIBRATION RECOMMENDATION")
    print("=" * 72)
    for group_key, group_info in summary_doc["groups"].items():
        print(
            f"  {group_key}: GRASP alpha={group_info['grasp']['best_alpha']}  |  "
            f"GRASP+TS alpha={group_info['ts']['best_alpha']}  "
            f"tenure={group_info['ts']['best_tenure']}"
        )
    print(f"\n  GRASP detail CSV   -> {GRASP_DETAIL_CSV}")
    print(f"  GRASP summary CSV  -> {GRASP_SUMMARY_CSV}")
    print(f"  GRASP runs CSV     -> {GRASP_RUNS_CSV}")
    print(f"  TS detail CSV      -> {TS_DETAIL_CSV}")
    print(f"  TS summary CSV     -> {TS_SUMMARY_CSV}")
    print(f"  TS runs CSV        -> {TS_RUNS_CSV}")
    print(f"  Summary JSON       -> {SUMMARY_JSON}")
    print("=" * 72)
