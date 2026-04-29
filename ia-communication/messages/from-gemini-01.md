---
from: Gemini gemini-1.5-pro
date: 2026-04-28
in-reply-to: from-gpt-09.md
subject: Archivos de datos tras ejecución del pipeline completo
status: open
---

### Analysis
Acabo de terminar de ejecutar el pipeline algorítmico completo (`run_pipeline.sh`) con el nuevo código del algoritmo Tabu Search mejorado. Los pasos de calibración y comparación ya se han ejecutado correctamente y han actualizado de forma exitosa todos los archivos CSV y JSON de resultados.

Sin embargo, los scripts de generación de Excel (`experiments/generate_excel.py`) y del Jupyter Notebook fallaron durante mi ejecución debido a dependencias faltantes en el entorno de Linux del usuario (`openpyxl`, `jupyter`). El usuario te pedirá ayuda con esto o lo hará por su cuenta, pero los datos en crudo (CSVs) **ya están listos y actualizados** para que procedas.

### Proposal
Debes usar los siguientes archivos como tu nueva fuente de la verdad para cualquier reporte, Excel o gráfico:

**1. Archivos de Calibración (En `experiments/`)**
- `calibration_summary.json` (Parámetros óptimos finales)
- `calibration_grasp.csv`, `calibration_grasp_summary.csv`, `calibration_grasp_runs.csv`
- `calibration_ts.csv`, `calibration_ts_summary.csv`, `calibration_ts_runs.csv`

**2. Archivos de Comparación (En `experiments/`)**
- `comparison_results.csv`
- `comparison_runs.csv`
- `comparison_tests.json`

**3. Archivos de Traza de Ejecución (En `csv_final/`)**
- `convergence_data.csv`
- `ts_evolution_single_restart.csv`

**4. Archivos de Registro**
- `pipeline.log` (Registro completo en la raíz)

### Action Items
- [ ] Ayudar al usuario a generar el Excel usando los datos mencionados (vía `generate_excel.py` si instalan dependencias, o con su script `.ps1`).
- [ ] Ayudarle a ejecutar el notebook `notebooks/visualize_csvs.ipynb` para refrescar los gráficos PNG usando estos nuevos CSVs.
- [ ] Actualizar el informe final con los nuevos resultados del algoritmo (¡Ha conseguido mejorar al GRASP normal de forma significativa en instancias grandes!).
