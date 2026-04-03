"""
generate_excel.py
Generates resultados.xlsx from the CSV/JSON files produced by calibration.py
and comparison.py.

Run from the project root:
    python3 experiments/generate_excel.py
"""

import csv
import json
import os
import sys

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --------- #
# PATHS     #
# --------- #

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = os.path.join(BASE, "experiments")

GRASP_SUMMARY_CSV  = os.path.join(EXP, "calibration_grasp_summary.csv")
TS_SUMMARY_CSV     = os.path.join(EXP, "calibration_ts_summary.csv")
COMPARISON_CSV     = os.path.join(EXP, "comparison_results.csv")
RUNS_CSV           = os.path.join(EXP, "comparison_runs.csv")
TESTS_JSON         = os.path.join(EXP, "comparison_tests.json")
OUTPUT_XLSX        = os.path.join(EXP, "resultados.xlsx")


# ----------- #
# STYLE UTILS #
# ----------- #

HEADER_FILL   = PatternFill("solid", fgColor="2F5496")
HEADER_FONT   = Font(bold=True, color="FFFFFF", size=10)
BEST_FILL     = PatternFill("solid", fgColor="E2EFDA")   # light green
SUBHEAD_FILL  = PatternFill("solid", fgColor="D9E1F2")   # light blue
SUBHEAD_FONT  = Font(bold=True, size=10)
BORDER_THIN   = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"), bottom=Side(style="thin"),
)


def style_header_row(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER_THIN


def style_data_row(ws, row, ncols, fill=None):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.border = BORDER_THIN
        cell.alignment = Alignment(horizontal="center", vertical="center")
        if fill:
            cell.fill = fill


def autofit(ws):
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            try:
                max_len = max(max_len, len(str(cell.value or "")))
            except Exception:
                pass
        ws.column_dimensions[col_letter].width = min(max(max_len + 2, 10), 35)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# --------------------------------- #
# SHEET 1 — Calibración GRASP       #
# --------------------------------- #

def sheet_calibracion_grasp(wb):
    ws = wb.create_sheet("Calibración GRASP")
    rows = read_csv(GRASP_SUMMARY_CSV)

    headers = ["Grupo", "Alpha", "Avg Dev%", "Media avg OF", "Tiempo medio (s)"]
    ws.append(headers)
    style_header_row(ws, 1, len(headers))

    # Find best per group
    best_per_group = {}
    for r in rows:
        g = r["group"]
        dev = float(r["avg_dev_pct"])
        if g not in best_per_group or dev < best_per_group[g]:
            best_per_group[g] = dev

    for r in rows:
        row_data = [
            r["group"],
            r["alpha"],
            float(r["avg_dev_pct"]),
            float(r["mean_avg_of"]),
            float(r["mean_time_s"]),
        ]
        ws.append(row_data)
        row_idx = ws.max_row
        is_best = float(r["avg_dev_pct"]) == best_per_group[r["group"]]
        style_data_row(ws, row_idx, len(headers), fill=BEST_FILL if is_best else None)

    ws.cell(1, 3).number_format = "0.0000%"
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=3):
        for cell in row:
            cell.number_format = "0.0000%"

    ws.freeze_panes = "A2"
    autofit(ws)
    return ws


# --------------------------------- #
# SHEET 2 — Calibración TS          #
# --------------------------------- #

def sheet_calibracion_ts(wb):
    ws = wb.create_sheet("Calibración TS")
    rows = read_csv(TS_SUMMARY_CSV)

    headers = ["Grupo", "Fase", "Alpha", "Tenure", "Avg Dev%", "Media avg OF", "Tiempo medio (s)"]
    ws.append(headers)
    style_header_row(ws, 1, len(headers))

    # best per (group, phase)
    best_per = {}
    for r in rows:
        key = (r["group"], r["phase"])
        dev = float(r["avg_dev_pct"])
        if key not in best_per or dev < best_per[key]:
            best_per[key] = dev

    for r in rows:
        row_data = [
            r["group"],
            r["phase"],
            r["alpha"],
            r["tenure"] if r["tenure"] else "-",
            float(r["avg_dev_pct"]),
            float(r["mean_avg_of"]),
            float(r["mean_time_s"]),
        ]
        ws.append(row_data)
        row_idx = ws.max_row
        key = (r["group"], r["phase"])
        is_best = float(r["avg_dev_pct"]) == best_per[key]
        style_data_row(ws, row_idx, len(headers), fill=BEST_FILL if is_best else None)

    ws.freeze_panes = "A2"
    autofit(ws)
    return ws


# ------------------------------------------ #
# SHEET 3 — Comparación por instancia         #
# ------------------------------------------ #

def sheet_comparacion(wb):
    ws = wb.create_sheet("Comparación instancias")
    rows = read_csv(COMPARISON_CSV)

    headers = [
        "Instancia", "Grupo",
        "Mejor conocido",
        "GRASP alpha", "GRASP avg OF", "GRASP best", "GRASP worst", "GRASP std", "GRASP dev%", "#Best GRASP", "GRASP tiempo(s)",
        "TS alpha", "TS tenure", "TS avg OF", "TS best", "TS worst", "TS std", "TS dev%", "#Best TS", "TS tiempo(s)",
    ]
    ws.append(headers)
    style_header_row(ws, 1, len(headers))

    for r in rows:
        row_data = [
            r["instance"], r["group"],
            float(r["best_known"]),
            float(r["grasp_alpha"]), float(r["grasp_avg_of"]), float(r["grasp_best"]),
            float(r["grasp_worst"]), float(r["grasp_std"]), float(r["grasp_dev_pct"]),
            int(r["grasp_nbest"]), float(r["grasp_avg_time"]),
            float(r["ts_alpha"]), int(r["ts_tenure"]) if r["ts_tenure"] else "-",
            float(r["ts_avg_of"]), float(r["ts_best"]),
            float(r["ts_worst"]), float(r["ts_std"]), float(r["ts_dev_pct"]),
            int(r["ts_nbest"]), float(r["ts_avg_time"]),
        ]
        ws.append(row_data)
        row_idx = ws.max_row
        # highlight row if TS avg > GRASP avg
        fill = BEST_FILL if float(r["ts_avg_of"]) > float(r["grasp_avg_of"]) else None
        style_data_row(ws, row_idx, len(headers), fill=fill)

    ws.freeze_panes = "C2"
    autofit(ws)
    return ws


# --------------------------------- #
# SHEET 4 — Runs individuales       #
# --------------------------------- #

def sheet_runs(wb):
    ws = wb.create_sheet("Runs individuales")
    rows = read_csv(RUNS_CSV)

    headers = ["Instancia", "Grupo", "Algoritmo", "Run", "Seed", "Alpha", "Tabu Tenure", "OF", "Tiempo (s)"]
    ws.append(headers)
    style_header_row(ws, 1, len(headers))

    for r in rows:
        row_data = [
            r["instance"], r["group"], r["algorithm"],
            int(r["run"]), int(r["seed"]),
            r["alpha"], r["tabu_tenure"] if r["tabu_tenure"] else "-",
            float(r["of"]), float(r["elapsed_s"]),
        ]
        ws.append(row_data)
        row_idx = ws.max_row
        style_data_row(ws, row_idx, len(headers))

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    autofit(ws)
    return ws


# --------------------------------- #
# SHEET 5 — Test estadístico        #
# --------------------------------- #

def sheet_test(wb):
    ws = wb.create_sheet("Test estadístico")

    with open(TESTS_JSON, encoding="utf-8") as f:
        data = json.load(f)

    # Title
    ws["A1"] = "Wilcoxon Signed-Rank Test — GRASP vs GRASP+TS (por run, pareado por semilla)"
    ws["A1"].font = Font(bold=True, size=12)
    ws.merge_cells("A1:I1")

    headers = ["Grupo", "N pares", "Wins GRASP", "Wins TS", "Empates", "Media delta (TS-GRASP)", "Pares no-cero", "Estadístico W", "p-valor"]
    ws.append(headers)
    style_header_row(ws, 2, len(headers))

    for group_key in ("overall", "small", "large"):
        t = data[group_key]
        if t["status"] == "ok":
            row_data = [
                group_key,
                t["n_pairs"],
                t["wins_grasp"],
                t["wins_ts"],
                t["ties"],
                t["mean_delta_ts_minus_grasp"],
                t.get("non_zero_pairs", "-"),
                t.get("statistic", "-"),
                t.get("pvalue", "-"),
            ]
        else:
            row_data = [
                group_key,
                t["n_pairs"],
                t.get("wins_grasp", "-"),
                t.get("wins_ts", "-"),
                t.get("ties", "-"),
                t.get("mean_delta_ts_minus_grasp", "-"),
                "-", "-",
                t["status"] + ": " + t.get("reason", ""),
            ]
        ws.append(row_data)
        row_idx = ws.max_row
        style_data_row(ws, row_idx, len(headers))
        # highlight significant result
        if t.get("status") == "ok" and isinstance(t.get("pvalue"), float) and t["pvalue"] < 0.05:
            ws.cell(row_idx, len(headers)).fill = BEST_FILL
            ws.cell(row_idx, len(headers)).font = Font(bold=True)

    # Note
    note_row = ws.max_row + 2
    ws.cell(note_row, 1).value = "Nota: test de dos colas, zero_method='wilcox'. Celdas verdes = p < 0.05 (significativo al 95%)."
    ws.cell(note_row, 1).font = Font(italic=True, size=9)
    ws.merge_cells(f"A{note_row}:I{note_row}")

    autofit(ws)
    return ws


# ---- #
# MAIN #
# ---- #

if __name__ == "__main__":
    wb = openpyxl.Workbook()
    wb.remove(wb.active)   # remove default empty sheet

    print("Generating sheets...")
    sheet_calibracion_grasp(wb)
    print("  [1/5] Calibracion GRASP")
    sheet_calibracion_ts(wb)
    print("  [2/5] Calibracion TS")
    sheet_comparacion(wb)
    print("  [3/5] Comparacion instancias")
    sheet_runs(wb)
    print("  [4/5] Runs individuales")
    sheet_test(wb)
    print("  [5/5] Test estadistico")

    wb.save(OUTPUT_XLSX)
    print(f"\nSaved: {OUTPUT_XLSX}")
