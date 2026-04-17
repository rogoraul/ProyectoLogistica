# Comparativa por instancia — GRASP vs GRASP+TS

Generado automáticamente a partir de los CSV en `experiments`.

## Instancia: MDG-a_10_100_m10.txt

- Mejor conocido (best_known): **355.500**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 355.500 | 0.000 | 355.500 | 355.500 | 10.003 | 0.000 | 0.000 |
| 0.1 | 355.500 | 0.000 | 355.500 | 355.500 | 10.001 | 0.000 | 0.000 |
| 0.25 | 355.500 | 0.000 | 355.500 | 355.500 | 10.001 | 0.000 | 0.000 |
| 0.5 | 355.500 | 0.000 | 355.500 | 355.500 | 10.003 | 0.000 | 0.000 |
| 0.75 | 355.500 | 0.000 | 355.500 | 355.500 | 10.002 | 0.000 | 0.000 |
| 0.9 | 355.500 | 0.000 | 355.500 | 355.500 | 10.003 | 0.000 | 0.000 |

### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 15 | 355.500 | 0.000 | 355.500 | 355.500 | 10.001 | 0.096 | 0.000 |
| 0.1 | 15 | 355.500 | 0.000 | 355.500 | 355.500 | 10.001 | 0.000 | 0.000 |
| 0.25 | 5 | 355.500 | 0.000 | 355.500 | 355.500 | 10.000 | 0.271 | 0.000 |
| 0.25 | 10 | 355.500 | 0.000 | 355.500 | 355.500 | 10.001 | 0.000 | 0.000 |
| 0.25 | 15 | 355.500 | 0.000 | 355.500 | 355.500 | 10.000 | 0.000 | 0.000 |
| 0.25 | 20 | 355.500 | 0.000 | 355.500 | 355.500 | 10.001 | 0.000 | 0.000 |
| 0.25 | 25 | 355.500 | 0.000 | 355.500 | 355.500 | 10.001 | 0.065 | 0.000 |
| 0.25 | 30 | 355.500 | 0.000 | 355.500 | 355.500 | 10.001 | 0.000 | 0.000 |
| 0.5 | 15 | 355.500 | 0.000 | 355.500 | 355.500 | 10.000 | 0.000 | 0.000 |
| 0.75 | 15 | 355.500 | 0.000 | 355.500 | 355.500 | 10.000 | 0.000 | 0.000 |
| 0.9 | 15 | 355.500 | 0.000 | 355.500 | 355.500 | 10.000 | 0.000 | 0.000 |

### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 355.500
- GRASP+TS alpha: 0.25, tenure: 15 → mean: 355.500

### Resumen comparativo

- Best known: 355.500
- Mejor GRASP (por proximidad a best_known): alpha=-1 → mean=355.500, abs_dev=0.000
- Mejor GRASP+TS: alpha=-1, tenure=15 → mean=355.500, abs_dev=0.000
- Conclusión: Ambos están igual de cerca del best_known.

---

## Instancia: MDG-a_12_100_m10.txt

- Mejor conocido (best_known): **354.250**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 354.250 | 0.000 | 354.250 | 354.250 | 10.002 | 0.000 | 0.000 |
| 0.1 | 354.250 | 0.000 | 354.250 | 354.250 | 10.001 | 0.000 | 0.000 |
| 0.25 | 354.250 | 0.000 | 354.250 | 354.250 | 10.001 | 0.000 | 0.000 |
| 0.5 | 354.250 | 0.000 | 354.250 | 354.250 | 10.002 | 0.000 | 0.000 |
| 0.75 | 354.250 | 0.000 | 354.250 | 354.250 | 10.002 | 0.000 | 0.000 |
| 0.9 | 354.250 | 0.000 | 354.250 | 354.250 | 10.002 | 0.000 | 0.000 |

### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 15 | 353.440 | 1.403 | 354.250 | 351.820 | 10.001 | 0.096 | 0.810 |
| 0.1 | 15 | 354.250 | 0.000 | 354.250 | 354.250 | 10.001 | 0.000 | 0.000 |
| 0.25 | 5 | 352.680 | 2.725 | 354.250 | 349.530 | 10.001 | 0.271 | 1.570 |
| 0.25 | 10 | 354.250 | 0.000 | 354.250 | 354.250 | 10.001 | 0.000 | 0.000 |
| 0.25 | 15 | 354.250 | 0.000 | 354.250 | 354.250 | 10.000 | 0.000 | 0.000 |
| 0.25 | 20 | 354.250 | 0.000 | 354.250 | 354.250 | 10.000 | 0.000 | 0.000 |
| 0.25 | 25 | 354.250 | 0.000 | 354.250 | 354.250 | 10.001 | 0.065 | 0.000 |
| 0.25 | 30 | 354.250 | 0.000 | 354.250 | 354.250 | 10.000 | 0.000 | 0.000 |
| 0.5 | 15 | 354.250 | 0.000 | 354.250 | 354.250 | 10.001 | 0.000 | 0.000 |
| 0.75 | 15 | 354.250 | 0.000 | 354.250 | 354.250 | 10.001 | 0.000 | 0.000 |
| 0.9 | 15 | 354.250 | 0.000 | 354.250 | 354.250 | 10.000 | 0.000 | 0.000 |

### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 354.250
- GRASP+TS alpha: 0.25, tenure: 15 → mean: 354.250

### Resumen comparativo

- Best known: 354.250
- Mejor GRASP (por proximidad a best_known): alpha=-1 → mean=354.250, abs_dev=0.000
- Mejor GRASP+TS: alpha=0.1, tenure=15 → mean=354.250, abs_dev=0.000
- Conclusión: Ambos están igual de cerca del best_known.

---

## Instancia: MDG-a_13_n500_m50.txt

- Mejor conocido (best_known): **7,780.220**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 7,705.030 | 15.047 | 7,722.300 | 7,694.770 | 11.359 | 0.337 | 75.190 |
| 0.1 | 7,731.370 | 14.140 | 7,739.850 | 7,715.050 | 10.480 | 0.254 | 48.850 |
| 0.25 | 7,714.660 | 32.995 | 7,752.670 | 7,693.400 | 10.790 | 0.287 | 65.560 |
| 0.5 | 7,713.260 | 13.342 | 7,727.900 | 7,701.780 | 11.006 | 0.582 | 66.960 |
| 0.75 | 7,695.380 | 30.107 | 7,727.060 | 7,667.140 | 11.109 | 0.727 | 84.840 |
| 0.9 | 7,662.500 | 15.209 | 7,679.360 | 7,649.820 | 11.093 | 0.555 | 117.720 |

### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 15 | 7,709.920 | 19.420 | 7,732.330 | 7,698.010 | 10.031 | 0.371 | 70.300 |
| 0.1 | 15 | 7,660.040 | 44.084 | 7,710.710 | 7,630.490 | 10.023 | 0.470 | 120.180 |
| 0.25 | 15 | 7,712.720 | 17.841 | 7,723.990 | 7,692.150 | 10.047 | 0.332 | 67.500 |
| 0.5 | 15 | 7,717.660 | 18.763 | 7,733.080 | 7,696.770 | 10.022 | 0.511 | 62.560 |
| 0.75 | 15 | 7,709.780 | 9.703 | 7,720.290 | 7,701.160 | 10.029 | 0.264 | 70.440 |
| 0.9 | 5 | 7,697.310 | 67.819 | 7,740.160 | 7,619.120 | 10.034 | 0.362 | 82.910 |
| 0.9 | 10 | 7,771.100 | 8.143 | 7,780.220 | 7,764.550 | 10.024 | 0.091 | 9.120 |
| 0.9 | 15 | 7,757.290 | 28.076 | 7,780.220 | 7,725.980 | 10.029 | 0.147 | 22.930 |
| 0.9 | 20 | 7,756.920 | 27.914 | 7,780.220 | 7,725.980 | 10.046 | 0.180 | 23.300 |
| 0.9 | 25 | 7,756.920 | 27.914 | 7,780.220 | 7,725.980 | 10.033 | 0.287 | 23.300 |
| 0.9 | 30 | 7,757.310 | 28.082 | 7,780.220 | 7,725.980 | 10.040 | 0.280 | 22.910 |

### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 7,737.720
- GRASP+TS alpha: 0.9, tenure: 10 → mean: 7,747.950

### Resumen comparativo

- Best known: 7,780.220
- Mejor GRASP (por proximidad a best_known): alpha=0.1 → mean=7,731.370, abs_dev=48.850
- Mejor GRASP+TS: alpha=0.9, tenure=10 → mean=7,771.100, abs_dev=9.120
- Conclusión: GRASP+TS está más cerca del best_known (por 39.730 unidades).

---

## Instancia: MDG-a_14_100_m10.txt

- Mejor conocido (best_known): **356.060**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 356.060 | 0.000 | 356.060 | 356.060 | 10.002 | 0.000 | 0.000 |
| 0.1 | 356.060 | 0.000 | 356.060 | 356.060 | 10.000 | 0.000 | 0.000 |
| 0.25 | 356.060 | 0.000 | 356.060 | 356.060 | 10.000 | 0.000 | 0.000 |
| 0.5 | 356.060 | 0.000 | 356.060 | 356.060 | 10.002 | 0.000 | 0.000 |
| 0.75 | 356.060 | 0.000 | 356.060 | 356.060 | 10.003 | 0.000 | 0.000 |
| 0.9 | 356.060 | 0.000 | 356.060 | 356.060 | 10.001 | 0.000 | 0.000 |

### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 15 | 356.060 | 0.000 | 356.060 | 356.060 | 10.001 | 0.096 | 0.000 |
| 0.1 | 15 | 356.060 | 0.000 | 356.060 | 356.060 | 10.001 | 0.000 | 0.000 |
| 0.25 | 5 | 352.820 | 3.131 | 356.060 | 349.810 | 10.001 | 0.271 | 3.240 |
| 0.25 | 10 | 356.060 | 0.000 | 356.060 | 356.060 | 10.001 | 0.000 | 0.000 |
| 0.25 | 15 | 356.060 | 0.000 | 356.060 | 356.060 | 10.001 | 0.000 | 0.000 |
| 0.25 | 20 | 356.060 | 0.000 | 356.060 | 356.060 | 10.001 | 0.000 | 0.000 |
| 0.25 | 25 | 354.900 | 2.003 | 356.060 | 352.590 | 10.001 | 0.065 | 1.160 |
| 0.25 | 30 | 356.060 | 0.000 | 356.060 | 356.060 | 10.001 | 0.000 | 0.000 |
| 0.5 | 15 | 356.060 | 0.000 | 356.060 | 356.060 | 10.000 | 0.000 | 0.000 |
| 0.75 | 15 | 356.060 | 0.000 | 356.060 | 356.060 | 10.001 | 0.000 | 0.000 |
| 0.9 | 15 | 356.060 | 0.000 | 356.060 | 356.060 | 10.001 | 0.000 | 0.000 |

### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 356.060
- GRASP+TS alpha: 0.25, tenure: 15 → mean: 356.060

### Resumen comparativo

- Best known: 356.060
- Mejor GRASP (por proximidad a best_known): alpha=-1 → mean=356.060, abs_dev=0.000
- Mejor GRASP+TS: alpha=-1, tenure=15 → mean=356.060, abs_dev=0.000
- Conclusión: Ambos están igual de cerca del best_known.

---

## Instancia: MDG-a_16_n500_m50.txt

- Mejor conocido (best_known): **7,757.500**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 7,739.38 | 18.2951 | 7,757.50 | 7,713.12 | 30.250 | 0.2336 | 18.12 |
### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.9 | 10 | 7,690.25 | 31.0416 | 7,728.40 | 7,653.24 | 30.019 | 0.8669 | 67.25 |
### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 7,739.380
- GRASP+TS alpha: 0.9, tenure: 10 → mean: 7,690.250

### Resumen comparativo

- Best known: 7,757.500
- Mejor GRASP (por proximidad a best_known): `alpha=0.1` → mean=7,739.38, abs_dev=18.12
- Mejor GRASP+TS: `alpha=0.9`, `tenure=10` → mean=7,690.25, abs_dev=67.25
- Conclusión: GRASP está más cerca del `best_known` para esta instancia.

---

## Instancia: MDG-a_17_n500_m50.txt

- Mejor conocido (best_known): **7,785.300**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 7,723.03 | 29.4929 | 7,756.16 | 7,692.77 | 30.328 | 0.7998 | 62.27 |
### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.9 | 10 | 7,704.35 | 54.8396 | 7,785.30 | 7,633.16 | 30.025 | 1.0398 | 80.95 |
### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 7,723.030
- GRASP+TS alpha: 0.9, tenure: 10 → mean: 7,704.350

### Resumen comparativo

- Best known: 7,785.300
- Mejor GRASP (por proximidad a best_known): `alpha=0.1` → mean=7,723.03, abs_dev=62.27
- Mejor GRASP+TS: `alpha=0.9`, `tenure=10` → mean=7,704.35, abs_dev=80.95
- Conclusión: GRASP está más cerca del `best_known` para esta instancia.

---

## Instancia: MDG-a_19_n500_m50.txt

- Mejor conocido (best_known): **7,729.010**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 7,702.49 | 20.2550 | 7,729.01 | 7,675.00 | 30.345 | 0.3431 | 26.52 |
### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.9 | 10 | 7,677.74 | 28.9908 | 7,722.68 | 7,645.06 | 30.026 | 0.6633 | 51.27 |
### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 7,702.490
- GRASP+TS alpha: 0.9, tenure: 10 → mean: 7,677.740

### Resumen comparativo

- Best known: 7,729.010
- Mejor GRASP (por proximidad a best_known): `alpha=0.1` → mean=7,702.49, abs_dev=26.52
- Mejor GRASP+TS: `alpha=0.9`, `tenure=10` → mean=7,677.74, abs_dev=51.27
- Conclusión: GRASP está más cerca del `best_known` para esta instancia.

---

## Instancia: MDG-a_1_100_m10.txt

- Mejor conocido (best_known): **360.150**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 360.150 | 0.000 | 360.150 | 360.150 | 10.002 | 0.000 | 0.000 |
| 0.1 | 360.150 | 0.000 | 360.150 | 360.150 | 10.001 | 0.000 | 0.000 |
| 0.25 | 360.150 | 0.000 | 360.150 | 360.150 | 10.001 | 0.000 | 0.000 |
| 0.5 | 360.150 | 0.000 | 360.150 | 360.150 | 10.004 | 0.000 | 0.000 |
| 0.75 | 360.150 | 0.000 | 360.150 | 360.150 | 10.003 | 0.000 | 0.000 |
| 0.9 | 360.150 | 0.000 | 360.150 | 360.150 | 10.003 | 0.000 | 0.000 |

### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 15 | 359.250 | 1.565 | 360.150 | 357.440 | 10.000 | 0.096 | 0.900 |
| 0.1 | 15 | 360.150 | 0.000 | 360.150 | 360.150 | 10.000 | 0.000 | 0.000 |
| 0.25 | 5 | 360.150 | 0.000 | 360.150 | 360.150 | 10.000 | 0.271 | 0.000 |
| 0.25 | 10 | 360.150 | 0.000 | 360.150 | 360.150 | 10.001 | 0.000 | 0.000 |
| 0.25 | 15 | 360.150 | 0.000 | 360.150 | 360.150 | 10.001 | 0.000 | 0.000 |
| 0.25 | 20 | 360.150 | 0.000 | 360.150 | 360.150 | 10.000 | 0.000 | 0.000 |
| 0.25 | 25 | 360.150 | 0.000 | 360.150 | 360.150 | 10.001 | 0.065 | 0.000 |
| 0.25 | 30 | 360.150 | 0.000 | 360.150 | 360.150 | 10.000 | 0.000 | 0.000 |
| 0.5 | 15 | 360.150 | 0.000 | 360.150 | 360.150 | 10.000 | 0.000 | 0.000 |
| 0.75 | 15 | 360.150 | 0.000 | 360.150 | 360.150 | 10.000 | 0.000 | 0.000 |
| 0.9 | 15 | 360.150 | 0.000 | 360.150 | 360.150 | 10.000 | 0.000 | 0.000 |

### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 360.150
- GRASP+TS alpha: 0.25, tenure: 15 → mean: 360.150

### Resumen comparativo

- Best known: 360.150
- Mejor GRASP (por proximidad a best_known): alpha=-1 → mean=360.150, abs_dev=0.000
- Mejor GRASP+TS: alpha=0.1, tenure=15 → mean=360.150, abs_dev=0.000
- Conclusión: Ambos están igual de cerca del best_known.

---

## Instancia: MDG-a_20_100_m10.txt

- Mejor conocido (best_known): **349.310**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|

### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|

### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 349.310
- GRASP+TS alpha: 0.25, tenure: 15 → mean: 349.310

### Resumen comparativo

- Best known: 349.310
- No hay datos de GRASP para esta instancia.
- No hay datos de GRASP+TS para esta instancia.
- Conclusión: Datos insuficientes para comparar proximidad al best_known.

---

## Instancia: MDG-a_20_n500_m50.txt

- Mejor conocido (best_known): **7,718.590**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 7,688.01 | 17.8010 | 7,718.59 | 7,672.84 | 30.412 | 0.3962 | 30.58 |
### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.9 | 10 | 7,658.29 | 33.1065 | 7,686.17 | 7,605.82 | 30.025 | 0.7812 | 60.30 |
### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 7,688.010
- GRASP+TS alpha: 0.9, tenure: 10 → mean: 7,658.290

### Resumen comparativo

- Best known: 7,718.590
- Mejor GRASP (por proximidad a best_known): `alpha=0.1` → mean=7,688.01, abs_dev=30.58
- Mejor GRASP+TS: `alpha=0.9`, `tenure=10` → mean=7,658.29, abs_dev=60.30
- Conclusión: GRASP está más cerca del `best_known` para esta instancia.

---

## Instancia: MDG-a_2_n500_m50.txt

- Mejor conocido (best_known): **7,756.240**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 7,656.020 | 20.589 | 7,675.530 | 7,634.500 | 11.692 | 0.337 | 100.220 |
| 0.1 | 7,688.610 | 34.657 | 7,720.380 | 7,651.650 | 10.335 | 0.254 | 67.630 |
| 0.25 | 7,691.040 | 18.177 | 7,706.870 | 7,671.190 | 10.729 | 0.287 | 65.200 |
| 0.5 | 7,678.870 | 56.374 | 7,742.570 | 7,635.400 | 11.159 | 0.582 | 77.370 |
| 0.75 | 7,626.040 | 22.535 | 7,651.710 | 7,609.500 | 10.735 | 0.727 | 130.200 |
| 0.9 | 7,703.770 | 53.941 | 7,754.900 | 7,647.400 | 11.525 | 0.555 | 52.470 |

### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 15 | 7,670.650 | 55.174 | 7,710.040 | 7,607.590 | 10.029 | 0.371 | 85.590 |
| 0.1 | 15 | 7,672.900 | 41.636 | 7,720.250 | 7,642.020 | 10.023 | 0.470 | 83.340 |
| 0.25 | 15 | 7,673.090 | 29.905 | 7,692.590 | 7,638.660 | 10.041 | 0.332 | 83.150 |
| 0.5 | 15 | 7,667.180 | 53.178 | 7,728.360 | 7,632.040 | 10.032 | 0.511 | 89.060 |
| 0.75 | 15 | 7,665.190 | 17.937 | 7,684.110 | 7,648.430 | 10.026 | 0.264 | 91.050 |
| 0.9 | 5 | 7,709.840 | 40.879 | 7,756.240 | 7,679.130 | 10.038 | 0.362 | 46.400 |
| 0.9 | 10 | 7,692.340 | 62.006 | 7,756.240 | 7,632.420 | 10.022 | 0.091 | 63.900 |
| 0.9 | 15 | 7,705.350 | 53.322 | 7,756.240 | 7,649.890 | 10.020 | 0.147 | 50.890 |
| 0.9 | 20 | 7,667.460 | 76.491 | 7,755.630 | 7,618.810 | 10.022 | 0.180 | 88.780 |
| 0.9 | 25 | 7,669.160 | 75.723 | 7,756.240 | 7,618.810 | 10.039 | 0.287 | 87.080 |
| 0.9 | 30 | 7,669.160 | 75.723 | 7,756.240 | 7,618.810 | 10.038 | 0.280 | 87.080 |

### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 7,695.500
- GRASP+TS alpha: 0.9, tenure: 10 → mean: 7,694.420

### Resumen comparativo

- Best known: 7,756.240
- Mejor GRASP (por proximidad a best_known): alpha=0.9 → mean=7,703.770, abs_dev=52.470
- Mejor GRASP+TS: alpha=0.9, tenure=5 → mean=7,709.840, abs_dev=46.400
- Conclusión: GRASP+TS está más cerca del best_known (por 6.070 unidades).

---

## Instancia: MDG-a_4_100_m10.txt

- Mejor conocido (best_known): **355.720**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 355.720 | 0.000 | 355.720 | 355.720 | 10.002 | 0.000 | 0.000 |
| 0.1 | 355.720 | 0.000 | 355.720 | 355.720 | 10.002 | 0.000 | 0.000 |
| 0.25 | 355.720 | 0.000 | 355.720 | 355.720 | 10.002 | 0.000 | 0.000 |
| 0.5 | 355.720 | 0.000 | 355.720 | 355.720 | 10.002 | 0.000 | 0.000 |
| 0.75 | 355.720 | 0.000 | 355.720 | 355.720 | 10.003 | 0.000 | 0.000 |
| 0.9 | 355.720 | 0.000 | 355.720 | 355.720 | 10.002 | 0.000 | 0.000 |

### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 15 | 355.720 | 0.000 | 355.720 | 355.720 | 10.000 | 0.096 | 0.000 |
| 0.1 | 15 | 355.720 | 0.000 | 355.720 | 355.720 | 10.000 | 0.000 | 0.000 |
| 0.25 | 5 | 355.720 | 0.000 | 355.720 | 355.720 | 10.001 | 0.271 | 0.000 |
| 0.25 | 10 | 355.720 | 0.000 | 355.720 | 355.720 | 10.000 | 0.000 | 0.000 |
| 0.25 | 15 | 355.720 | 0.000 | 355.720 | 355.720 | 10.000 | 0.000 | 0.000 |
| 0.25 | 20 | 355.720 | 0.000 | 355.720 | 355.720 | 10.001 | 0.000 | 0.000 |
| 0.25 | 25 | 355.720 | 0.000 | 355.720 | 355.720 | 10.001 | 0.065 | 0.000 |
| 0.25 | 30 | 355.720 | 0.000 | 355.720 | 355.720 | 10.000 | 0.000 | 0.000 |
| 0.5 | 15 | 355.720 | 0.000 | 355.720 | 355.720 | 10.001 | 0.000 | 0.000 |
| 0.75 | 15 | 355.720 | 0.000 | 355.720 | 355.720 | 10.000 | 0.000 | 0.000 |
| 0.9 | 15 | 355.720 | 0.000 | 355.720 | 355.720 | 10.000 | 0.000 | 0.000 |

### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 355.720
- GRASP+TS alpha: 0.25, tenure: 15 → mean: 355.720

### Resumen comparativo

- Best known: 355.720
- Mejor GRASP (por proximidad a best_known): alpha=-1 → mean=355.720, abs_dev=0.000
- Mejor GRASP+TS: alpha=-1, tenure=15 → mean=355.720, abs_dev=0.000
- Conclusión: Ambos están igual de cerca del best_known.

---

## Instancia: MDG-a_5_n500_m50.txt

- Mejor conocido (best_known): **7,755.230**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 7,694.460 | 53.721 | 7,731.540 | 7,632.850 | 10.773 | 0.337 | 60.770 |
| 0.1 | 7,655.990 | 12.695 | 7,668.680 | 7,643.290 | 10.286 | 0.254 | 99.240 |
| 0.25 | 7,657.050 | 22.984 | 7,681.310 | 7,635.600 | 10.773 | 0.287 | 98.180 |
| 0.5 | 7,638.030 | 6.042 | 7,644.910 | 7,633.600 | 10.606 | 0.582 | 117.200 |
| 0.75 | 7,644.700 | 1.296 | 7,645.540 | 7,643.210 | 11.223 | 0.727 | 110.530 |
| 0.9 | 7,648.760 | 29.585 | 7,682.510 | 7,627.320 | 11.066 | 0.555 | 106.470 |

### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 15 | 7,653.610 | 25.012 | 7,680.730 | 7,631.450 | 10.021 | 0.371 | 101.620 |
| 0.1 | 15 | 7,653.600 | 38.041 | 7,696.550 | 7,624.140 | 10.036 | 0.470 | 101.630 |
| 0.25 | 15 | 7,676.620 | 38.490 | 7,710.070 | 7,634.550 | 10.021 | 0.332 | 78.610 |
| 0.5 | 15 | 7,637.770 | 16.688 | 7,648.010 | 7,618.510 | 10.029 | 0.511 | 117.460 |
| 0.75 | 15 | 7,662.490 | 24.669 | 7,690.920 | 7,646.690 | 10.039 | 0.264 | 92.740 |
| 0.9 | 5 | 7,650.800 | 67.212 | 7,711.420 | 7,578.520 | 10.041 | 0.362 | 104.430 |
| 0.9 | 10 | 7,665.400 | 88.392 | 7,755.230 | 7,578.520 | 10.026 | 0.091 | 89.830 |
| 0.9 | 15 | 7,676.130 | 73.229 | 7,755.230 | 7,610.700 | 10.039 | 0.147 | 79.100 |
| 0.9 | 20 | 7,682.780 | 64.726 | 7,755.230 | 7,630.660 | 10.021 | 0.180 | 72.450 |
| 0.9 | 25 | 7,665.570 | 36.570 | 7,703.600 | 7,630.660 | 10.047 | 0.287 | 89.660 |
| 0.9 | 30 | 7,668.180 | 40.683 | 7,711.420 | 7,630.660 | 10.032 | 0.280 | 87.050 |

### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 7,697.350
- GRASP+TS alpha: 0.9, tenure: 10 → mean: 7,635.250

### Resumen comparativo

- Best known: 7,755.230
- Mejor GRASP (por proximidad a best_known): alpha=-1 → mean=7,694.460, abs_dev=60.770
- Mejor GRASP+TS: alpha=0.9, tenure=20 → mean=7,682.780, abs_dev=72.450
- Conclusión: GRASP está más cerca del best_known (por 11.680 unidades).

---

## Instancia: MDG-a_6_n500_m50.txt

- Mejor conocido (best_known): **7,752.310**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 7,695.610 | 23.336 | 7,710.320 | 7,668.700 | 11.042 | 0.337 | 56.700 |
| 0.1 | 7,717.680 | 34.520 | 7,752.310 | 7,683.270 | 10.166 | 0.254 | 34.630 |
| 0.25 | 7,673.980 | 18.123 | 7,687.290 | 7,653.340 | 11.446 | 0.287 | 78.330 |
| 0.5 | 7,650.690 | 24.322 | 7,677.030 | 7,629.080 | 11.144 | 0.582 | 101.620 |
| 0.75 | 7,648.920 | 36.261 | 7,689.140 | 7,618.730 | 11.012 | 0.727 | 103.390 |
| 0.9 | 7,659.760 | 29.159 | 7,690.850 | 7,633.020 | 11.283 | 0.555 | 92.550 |

### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 15 | 7,675.480 | 10.795 | 7,684.240 | 7,663.420 | 10.039 | 0.371 | 76.830 |
| 0.1 | 15 | 7,671.120 | 25.741 | 7,700.440 | 7,652.250 | 10.037 | 0.470 | 81.190 |
| 0.25 | 15 | 7,670.730 | 23.678 | 7,692.240 | 7,645.360 | 10.022 | 0.332 | 81.580 |
| 0.5 | 15 | 7,666.240 | 13.727 | 7,682.090 | 7,658.210 | 10.034 | 0.511 | 86.070 |
| 0.75 | 15 | 7,696.680 | 45.842 | 7,749.300 | 7,665.390 | 10.023 | 0.264 | 55.630 |
| 0.9 | 5 | 7,686.350 | 37.950 | 7,726.580 | 7,651.190 | 10.011 | 0.362 | 65.960 |
| 0.9 | 10 | 7,700.690 | 22.617 | 7,726.580 | 7,684.760 | 10.023 | 0.091 | 51.620 |
| 0.9 | 15 | 7,682.630 | 44.020 | 7,726.580 | 7,638.540 | 10.028 | 0.147 | 69.680 |
| 0.9 | 20 | 7,696.070 | 26.333 | 7,711.830 | 7,665.670 | 10.022 | 0.180 | 56.240 |
| 0.9 | 25 | 7,674.180 | 37.865 | 7,706.180 | 7,632.380 | 10.022 | 0.287 | 78.130 |
| 0.9 | 30 | 7,675.880 | 32.790 | 7,707.900 | 7,642.370 | 10.029 | 0.280 | 76.430 |

### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 7,712.160
- GRASP+TS alpha: 0.9, tenure: 10 → mean: 7,691.210

### Resumen comparativo

- Best known: 7,752.310
- Mejor GRASP (por proximidad a best_known): alpha=0.1 → mean=7,717.680, abs_dev=34.630
- Mejor GRASP+TS: alpha=0.9, tenure=10 → mean=7,700.690, abs_dev=51.620
- Conclusión: GRASP está más cerca del best_known (por 16.990 unidades).

---

## Instancia: MDG-a_9_n500_m50.txt

- Mejor conocido (best_known): **7,755.200**

### GRASP — resultados por `alpha`

| Alpha | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 7,689.250 | 18.282 | 7,703.270 | 7,668.570 | 11.125 | 0.337 | 65.950 |
| 0.1 | 7,679.110 | 27.185 | 7,706.340 | 7,651.970 | 10.140 | 0.254 | 76.090 |
| 0.25 | 7,723.230 | 9.130 | 7,732.640 | 7,714.410 | 10.941 | 0.287 | 31.970 |
| 0.5 | 7,665.390 | 36.542 | 7,706.050 | 7,635.300 | 11.008 | 0.582 | 89.810 |
| 0.75 | 7,675.050 | 34.785 | 7,712.310 | 7,643.430 | 11.032 | 0.727 | 80.150 |
| 0.9 | 7,681.490 | 40.858 | 7,718.590 | 7,637.700 | 10.655 | 0.555 | 73.710 |

### GRASP+TS — resultados por `alpha` / `tenure`

| Alpha | Tenure | Mean (avg_of) | Std | Best | Worst | AvgTime(s) | AvgDevPct | AbsDevFromBest |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -1 | 15 | 7,694.110 | 48.993 | 7,728.010 | 7,637.940 | 10.036 | 0.371 | 61.090 |
| 0.1 | 15 | 7,707.930 | 23.115 | 7,725.680 | 7,681.790 | 10.025 | 0.470 | 47.270 |
| 0.25 | 15 | 7,685.750 | 24.205 | 7,705.620 | 7,658.790 | 10.031 | 0.332 | 69.450 |
| 0.5 | 15 | 7,661.380 | 44.142 | 7,707.480 | 7,619.500 | 10.035 | 0.511 | 93.820 |
| 0.75 | 15 | 7,711.120 | 22.842 | 7,735.930 | 7,690.960 | 10.029 | 0.264 | 44.080 |
| 0.9 | 5 | 7,677.460 | 67.156 | 7,732.880 | 7,602.780 | 10.019 | 0.362 | 77.740 |
| 0.9 | 10 | 7,697.420 | 25.037 | 7,722.800 | 7,672.740 | 10.034 | 0.091 | 57.780 |
| 0.9 | 15 | 7,683.520 | 36.703 | 7,711.790 | 7,642.040 | 10.037 | 0.147 | 71.680 |
| 0.9 | 20 | 7,688.980 | 18.617 | 7,702.470 | 7,667.740 | 10.030 | 0.180 | 66.220 |
| 0.9 | 25 | 7,685.190 | 25.118 | 7,702.470 | 7,656.380 | 10.040 | 0.287 | 70.010 |
| 0.9 | 30 | 7,683.250 | 28.851 | 7,702.900 | 7,650.130 | 10.017 | 0.280 | 71.950 |

### Configuración utilizada en `comparison_results.csv`

- GRASP alpha: 0.1 → mean: 7,730.840
- GRASP+TS alpha: 0.9, tenure: 10 → mean: 7,700.910

### Resumen comparativo

- Best known: 7,755.200
- Mejor GRASP (por proximidad a best_known): alpha=0.25 → mean=7,723.230, abs_dev=31.970
- Mejor GRASP+TS: alpha=0.75, tenure=15 → mean=7,711.120, abs_dev=44.080
- Conclusión: GRASP está más cerca del best_known (por 12.110 unidades).

---

