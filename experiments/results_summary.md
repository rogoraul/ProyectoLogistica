# Resumen de resultados actuales

Fecha de actualizacion: 2026-05-07

Este documento resume los resultados vigentes generados a partir de los CSV y JSON actuales en `experiments/` y `csv_final/`. La fuente de verdad es la reejecucion completa del pipeline del 2026-04-30, con `comparison_tests.json` recalculado desde `comparison_runs.csv` al disponer ya de `scipy`.

## Fuente de datos

- `experiments/calibration_summary.json`
- `experiments/calibration_grasp_summary.csv`
- `experiments/calibration_ts_summary.csv`
- `experiments/comparison_results.csv`
- `experiments/comparison_runs.csv`
- `experiments/comparison_tests.json`
- `csv_final/ts_evolution_single_restart.csv`
- `csv_final/convergence_curves_large.csv`

## Parametros seleccionados

| Grupo | GRASP alpha | GRASP+TS alpha | GRASP+TS tenure |
| ----- | ----------- | -------------- | --------------- |
| small | 0.1 | -1 | 5 |
| large | 0.1 | 0.1 | 10 |

En `small`, todas las configuraciones relevantes empatan con desviacion media 0.0%, por lo que los parametros son desempates practicos. En `large`, GRASP prefiere `alpha=0.1`; GRASP+TS tambien selecciona `alpha=0.1`, con `tenure=10`.

## Comparacion final

### Small

Las 6 instancias pequenas producen 30 empates exactos en las 30 parejas de ejecucion. El test de Wilcoxon se omite porque todas las diferencias son cero.

### Large

| Metrica | GRASP | GRASP+TS |
| ------- | ----- | -------- |
| Avg dev% | 0.6379% | 0.2284% |
| Desviacion estandar media | 20.57 | 20.27 |
| Best hits | 0 | 12 |
| Paired wins | 8 | 36 |
| Ties | - | 1 |
| Mean delta (TS - GRASP) | - | +31.7891 |
| Wilcoxon W | - | 79.0 |
| Wilcoxon p-value | - | 8.24e-08 |

La direccion de la diferencia favorece a GRASP+TS. El valor medio de `TS - GRASP` es positivo y el test de Wilcoxon bilateral sobre las diferencias no nulas (`zero_method="wilcox"`) indica una diferencia estadisticamente significativa.

## Resultados por instancia grande

| Instancia | GRASP avg | TS avg | Delta TS-GRASP | Best observado | TS best hits |
| --------- | --------- | ------ | -------------- | -------------- | ------------ |
| MDG-a_2 | 7695.50 | 7729.77 | +34.27 | 7741.07 | 1 |
| MDG-a_5 | 7697.35 | 7739.21 | +41.86 | 7755.23 | 2 |
| MDG-a_6 | 7712.16 | 7754.04 | +41.88 | 7770.48 | 1 |
| MDG-a_9 | 7730.84 | 7741.52 | +10.68 | 7758.44 | 1 |
| MDG-a_13 | 7737.72 | 7761.13 | +23.41 | 7786.43 | 1 |
| MDG-a_16 | 7739.38 | 7756.25 | +16.87 | 7792.77 | 1 |
| MDG-a_17 | 7723.03 | 7772.74 | +49.71 | 7785.36 | 2 |
| MDG-a_19 | 7702.49 | 7745.61 | +43.12 | 7755.41 | 2 |
| MDG-a_20 | 7688.01 | 7712.33 | +24.32 | 7727.13 | 1 |

GRASP+TS supera a GRASP en media en todas las instancias grandes del experimento actual.

## Graficas solicitadas por el profesor

### Evolucion interna de Tabu Search

`csv_final/ts_evolution_single_restart.csv` contiene 2586 iteraciones de una reiniciacion de Tabu Search. De ellas, 1403 son movimientos de empeoramiento (`was_worsening_move=True`). Esto demuestra la mecanica esperada: la solucion actual puede empeorar temporalmente, mientras el mejor global se conserva y mejora de forma escalonada.

Figura asociada: `csv_final/ts_evolution_plot.png`.

### Curvas con mas tiempo

`csv_final/convergence_curves_large.csv` compara GRASP y GRASP+TS durante 180 segundos por algoritmo en dos instancias grandes representativas.

| Instancia | GRASP final | GRASP+TS final |
| --------- | ----------- | -------------- |
| MDG-a_16 | 7726.43 | 7792.77 |
| MDG-a_13 | 7734.12 | 7798.43 |

Figura asociada: `csv_final/convergence_curves_large.png`.

## Conclusiones

1. En instancias pequenas, GRASP y GRASP+TS son indistinguibles bajo el presupuesto actual.
2. En instancias grandes, GRASP+TS domina los resultados actuales: menor desviacion media, mas wins pareados, mas mejores observados y Wilcoxon significativo.
3. La traza interna de Tabu Search muestra movimientos de empeoramiento, que son necesarios para escapar de optimos locales.
4. Las curvas a 180 segundos muestran que GRASP+TS sigue mejorando cuando recibe mas tiempo, especialmente dentro de fases largas de busqueda tabu.
