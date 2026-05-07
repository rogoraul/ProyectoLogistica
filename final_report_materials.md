# Materiales para el informe final

Fecha de revision: 2026-05-07

Este documento deja fijado que materiales del repositorio deben usarse para reconstruir el informe final y cuales deben evitarse por estar desactualizados.

## Fuente de verdad actual

La fuente de verdad son los resultados regenerados el 2026-04-30 y los artefactos recalculados el 2026-05-07:

- `experiments/comparison_results.csv`
- `experiments/comparison_runs.csv`
- `experiments/comparison_tests.json`
- `experiments/calibration_summary.json`
- `experiments/calibration_grasp_summary.csv`
- `experiments/calibration_ts_summary.csv`
- `csv_final/ts_evolution_single_restart.csv`
- `csv_final/convergence_curves_large.csv`
- `csv_final/convergence_data.csv`

No usar como fuente principal documentos o Excels anteriores a esa fecha.

## Documentos de texto utiles

| Archivo | Uso recomendado |
| ------- | --------------- |
| `report.md` | Base principal para redactar el informe final completo. |
| `results.md` | Fuente tecnica para la seccion de resultados experimentales. |
| `experiments/results_summary.md` | Resumen corto de resultados y conclusiones. |
| `ia-communication/messages/from-gpt-11.md` | Trazabilidad de la reconciliacion de datos, textos, graficas y Excel. |
| `README.md` | Descripcion actualizada del repositorio y de los resultados vigentes. |

## Tablas y Excel utiles

| Archivo | Uso recomendado |
| ------- | --------------- |
| `experiments/calibracion_grasp.xlsx` | Tabla formateada de calibracion de alpha para GRASP. |
| `experiments/calibracion_ts.xlsx` | Tabla formateada de calibracion de alpha y tenure para GRASP+TS. |
| `experiments/comparacion_final.xlsx` | Tabla formateada de comparacion final y test estadistico. |

Los Excels antiguos que estaban en `resultados_excel/` se han movido a `basura/legacy_excels/`.

## Figuras utiles

| Archivo | Uso recomendado |
| ------- | --------------- |
| `csv_final/ts_evolution_plot.png` | Figura principal para mostrar la evolucion interna de Tabu Search y sus empeoramientos temporales. |
| `csv_final/convergence_curves_large.png` | Figura principal para responder a la pregunta de que ocurre si se da mas tiempo a GRASP+TS. |
| `csv_final/convergence_plot.png` | Figura secundaria de convergencia en la instancia usada por `main.py`. Usar solo si hay espacio o como apoyo. |

## Datos clave que deben aparecer en el informe

### Parametros seleccionados

| Grupo | GRASP alpha | GRASP+TS alpha | GRASP+TS tenure |
| ----- | ----------- | -------------- | --------------- |
| small | 0.1 | -1 | 5 |
| large | 0.1 | 0.1 | 10 |

### Comparacion final en instancias grandes

| Metrica | GRASP | GRASP+TS |
| ------- | ----- | -------- |
| Avg dev% | 0.6379% | 0.2284% |
| Desviacion estandar media | 20.57 | 20.27 |
| Best hits | 0 | 12 |
| Wins pareados | 8 | 36 |
| Empates | - | 1 |
| Delta medio TS-GRASP | - | +31.7891 |
| Wilcoxon W | - | 79.0 |
| Wilcoxon p-valor | - | 8.24e-08 |

Interpretacion: en instancias grandes, los resultados actuales favorecen claramente a GRASP+TS.

### Instancias pequenas

En las 6 instancias pequenas, los 30 pares de ejecucion son empates exactos. El test de Wilcoxon se omite porque todas las diferencias son cero.

### Evolucion interna de Tabu Search

`csv_final/ts_evolution_single_restart.csv` contiene 2586 iteraciones de una reiniciacion de Tabu Search, con 1403 movimientos de empeoramiento. Esta es la evidencia principal para explicar que Tabu Search puede empeorar temporalmente la solucion actual para escapar de optimos locales.

### Convergencia con mas tiempo

`csv_final/convergence_curves_large.csv` contiene ejecuciones de 180 segundos por algoritmo en dos instancias grandes:

| Instancia | GRASP final | GRASP+TS final |
| --------- | ----------- | -------------- |
| MDG-a_16 | 7748.58 | 7789.24 |
| MDG-a_13 | 7755.63 | 7798.43 |

Interpretacion: con mas tiempo, GRASP+TS sigue encontrando mejoras dentro de fases largas de Busqueda Tabu.

## Material movido a `basura/`

Estos archivos no deben usarse para el informe final, salvo como historico:

| Ubicacion actual | Motivo |
| ---------------- | ------ |
| `basura/legacy_reports/mdp_report_final_professor (1).docx` | Informe antiguo anterior a la reconciliacion de resultados. |
| `basura/legacy_reports/mdp_report_final_professor (1).pdf` | PDF antiguo anterior a la reconciliacion de resultados. |
| `basura/legacy_excels/resultados_excel/` | Excels antiguos de abril 3-8. |
| `basura/legacy_experiment_notes/comparative_by_instance.md` | Resumen antiguo de otra fase experimental. |
| `basura/legacy_experiment_notes/results_lastpull.txt` | Nota temporal antigua. |
| `basura/legacy_experiment_notes/calibration.log` | Log antiguo y no necesario para el informe. |
| `basura/tool_noise/AGENTS.md` | Contexto temporal de herramienta, no material del proyecto. |

## Material a excluir al preparar entrega

Si se entrega el directorio completo comprimido, excluir:

- `.git/`
- `.idea/`
- `venv/`
- `__pycache__/`
- `basura/`
- cualquier fichero `.pyc`

Estos elementos no forman parte del entregable academico.

## Orden recomendado para reconstruir el informe final

1. Usar `report.md` como base textual.
2. Insertar las tablas resumidas desde `experiments/comparacion_final.xlsx`.
3. Insertar `csv_final/ts_evolution_plot.png` en la seccion de evolucion interna de Tabu Search.
4. Insertar `csv_final/convergence_curves_large.png` en la seccion de efecto del tiempo.
5. Revisar que no queden afirmaciones antiguas:
   - `GRASP es mejor en grandes`
   - `p = 0.0026`
   - `GRASP+TS alpha=0.9` como configuracion final
   - `scipy_not_installed`
6. Exportar a `.docx` o `.pdf`.
7. Hacer revision visual final de tablas, saltos de pagina, figuras y conclusiones.
