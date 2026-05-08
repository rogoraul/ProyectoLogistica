# Proyecto de Logistica Basada en Datos
## Metaheuristicas para el Problema de la Maxima Diversidad: GRASP y Busqueda Tabu

---

## 1. Introduccion y problema

El Problema de la Maxima Diversidad (MDP, Maximum Diversity Problem) consiste en seleccionar un subconjunto de exactamente `p` elementos, dentro de un conjunto de `n` candidatos, maximizando la suma de distancias entre todos los pares seleccionados:

```text
max sum d(i, j), para i,j en S e i < j
```

Es un problema NP-dificil, por lo que se emplean metaheuristicas para obtener soluciones de alta calidad en tiempos razonables.

Las instancias usadas pertenecen a la familia MDG-a:

| Tipo | n | p | Numero de instancias |
| ---- | - | - | -------------------- |
| Pequenas | 100 | 10 | 6 |
| Grandes | 500 | 50 | 9 |

---

## 2. Algoritmos implementados

### 2.1 GRASP

GRASP combina una fase constructiva greedy-aleatoria con una busqueda local de mejor mejora.

En la construccion, el parametro `alpha` controla el equilibrio entre voracidad y aleatoriedad:

- `alpha=0` aproxima una construccion greedy.
- `alpha=1` aproxima una construccion aleatoria.
- `alpha=-1` aleatoriza el valor de `alpha` durante la construccion.

Tras construir una solucion, se aplica busqueda local exhaustiva de intercambio 1-1 hasta no encontrar ningun movimiento con mejora positiva.

### 2.2 Busqueda Tabu

La Busqueda Tabu parte de una solucion y explora intercambios 1-1 permitiendo tambien movimientos que empeoran temporalmente la solucion actual. Esto permite escapar de optimos locales.

La version actual usa:

- memoria tabu bidireccional: elementos que salen no pueden reentrar inmediatamente, y elementos que entran no pueden salir inmediatamente;
- listas FIFO de corto plazo;
- tenure dinamico entre `tabu_tenure` y `1.5 * tabu_tenure`;
- criterio de aspiracion: un movimiento tabu puede aceptarse si mejora el mejor global conocido;
- limite de tiempo global y limite de iteraciones sin mejora.

### 2.3 GRASP+TS

GRASP+TS usa GRASP para construir soluciones iniciales y Busqueda Tabu como fase de mejora. El presupuesto de tiempo es global: cada llamada a Tabu Search recibe solo el tiempo restante. Ademas, la telemetria actual registra cada mejora estricta del mejor global dentro de Tabu Search, lo que permite dibujar curvas reales de convergencia.

---

## 3. Implementacion relevante

La solucion se representa como un diccionario Python:

```python
sol = {
    "sol": set(),
    "of": 0.0,
    "instance": inst,
}
```

El uso de `set` permite comprobar pertenencia en O(1). La funcion objetivo se actualiza incrementalmente: al sacar un nodo se resta su contribucion marginal y al meter otro se suma su nueva contribucion respecto al conjunto resultante. Esto evita recomputar desde cero la suma de todas las distancias.

La busqueda local y la Busqueda Tabu comparten el vecindario de intercambio:

```text
delta = contribucion(v_in sin v_out) - contribucion(v_out)
```

GRASP acepta solo mejoras locales positivas. Tabu Search, en cambio, puede aceptar empeoramientos, siempre respetando la memoria tabu salvo aspiracion.

---

## 4. Experimentacion

### 4.1 Configuracion experimental

| Fase | Tiempo por run | Runs |
| ---- | -------------- | ---- |
| Calibracion | 10 s | 3 por configuracion |
| Comparacion final | 30 s | 5 por instancia y algoritmo |
| Curvas largas | 180 s | 1 por instancia y algoritmo |

La calibracion es secuencial: primero se calibra `alpha`; despues se fija ese valor y se calibra `tenure`.

### 4.2 Parametros seleccionados

| Grupo | GRASP alpha | GRASP+TS alpha | GRASP+TS tenure |
| ----- | ----------- | -------------- | --------------- |
| Pequenas | 0.1 | -1 | 5 |
| Grandes | 0.1 | 0.1 | 10 |

En instancias pequenas todas las configuraciones relevantes saturan, asi que la seleccion es un desempate practico. En instancias grandes, la configuracion `alpha=0.1, tenure=10` de GRASP+TS consigue la menor desviacion media durante la calibracion.

### 4.3 Comparacion en instancias pequenas

En las 6 instancias pequenas, con 5 semillas por instancia, los 30 pares GRASP vs GRASP+TS son empates exactos. El test de Wilcoxon se omite porque todas las diferencias son cero.

Conclusion: con `n=100` y 30 segundos, ambas variantes alcanzan la misma calidad. La Busqueda Tabu no aporta una mejora medible en este grupo.

### 4.4 Comparacion en instancias grandes

| Instancia | GRASP avg | TS avg | Delta TS-GRASP | Mejor observado | TS best hits |
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

Resumen agregado en grandes:

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

El test de Wilcoxon signed-rank bilateral, aplicado a los pares no empatados, confirma que la diferencia es estadisticamente significativa. La direccion de la diferencia favorece a GRASP+TS.

---

## 5. Analisis solicitado por el profesor

### 5.1 Evolucion interna de Tabu Search

El archivo `csv_final/ts_evolution_single_restart.csv` registra una reiniciacion individual de Tabu Search. Contiene 2586 iteraciones, de las cuales 1403 son movimientos de empeoramiento.

Esto demuestra visualmente el comportamiento esperado: la solucion actual puede bajar para escapar de un optimo local, mientras el mejor global se mantiene y mejora por escalones.

Figura asociada: `csv_final/ts_evolution_plot.png`.

### 5.2 Efecto de dar mas tiempo

El experimento `experiments/time_analysis.py` ejecuta GRASP y GRASP+TS durante 180 segundos por algoritmo en dos instancias grandes representativas.

| Instancia | GRASP final | GRASP+TS final |
| --------- | ----------- | -------------- |
| MDG-a_16 | 7726.43 | 7792.77 |
| MDG-a_13 | 7734.12 | 7798.43 |

Figura asociada: `csv_final/convergence_curves_large.png`.

Estas curvas muestran que GRASP+TS sigue encontrando mejoras dentro de fases largas de Busqueda Tabu y alcanza valores finales superiores a GRASP en las dos instancias analizadas.

---

## 6. Conclusiones

1. En instancias pequenas, GRASP y GRASP+TS son equivalentes bajo el presupuesto experimental usado.
2. En instancias grandes, los datos actuales favorecen claramente a GRASP+TS: menor desviacion media, mas victorias pareadas, mas mejores observados y Wilcoxon significativo.
3. La correccion de telemetria permite observar correctamente la convergencia interna de GRASP+TS; antes, las mejoras dentro de Tabu Search quedaban colapsadas en un unico punto final.
4. La traza de Tabu Search muestra empeoramientos temporales, que son parte normal y deseable del mecanismo de escape.
5. Al ampliar el presupuesto de tiempo a 180 segundos, GRASP+TS sigue mejorando y supera a GRASP en las instancias grandes seleccionadas.

La conclusion final es que la Busqueda Tabu si aporta valor al proyecto en instancias grandes. No solo mejora los mejores valores alcanzados, sino tambien la calidad media bajo la implementacion y los datos actuales.

---

## 7. Ficheros principales

| Fichero | Descripcion |
| ------- | ----------- |
| `algorithms/grasp_timed.py` | GRASP con presupuesto de tiempo y telemetria opcional |
| `algorithms/grasp_ts.py` | GRASP+TS con presupuesto global y logging de mejoras |
| `localsearch/tabu_search.py` | Busqueda Tabu bidireccional con tenure dinamico y aspiracion |
| `experiments/calibration.py` | Calibracion secuencial |
| `experiments/comparison.py` | Comparacion final y test de Wilcoxon |
| `experiments/generate_excel.py` | Generacion de tablas Excel |
| `experiments/time_analysis.py` | Curvas de convergencia a 180 segundos |
| `experiments/plot_time_analysis.py` | Grafica de convergencia larga |
| `notebooks/visualize_csvs.ipynb` | Visualizacion de CSVs principales |
| `csv_final/ts_evolution_single_restart.csv` | Evolucion interna de una reiniciacion Tabu |
| `csv_final/convergence_curves_large.csv` | Curvas temporales en instancias grandes |
