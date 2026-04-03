# Proyecto de Logística Basada en Datos
## Metaheurísticas para el Problema de la Máxima Diversidad: GRASP y Búsqueda Tabú

---

## 1. Introducción y definición del problema

El **Problema de la Máxima Diversidad** (MDP, *Maximum Diversity Problem*) consiste en seleccionar, de un conjunto de *n* elementos con distancias conocidas entre todos los pares, un subconjunto de exactamente *p* elementos que maximice la suma total de las distancias entre los elementos seleccionados:

$$\text{maximizar} \sum_{i,j \in S,\ i < j} d(i, j)$$

El problema es NP-difícil, por lo que se recurre a metaheurísticas para obtener soluciones de alta calidad en tiempo razonable.

El interés logístico es directo: seleccionar *p* localizaciones de entre *n* candidatas maximizando la dispersión geográfica (cobertura máxima del territorio), o construir una cartera de activos lo más diversa posible. En ambos casos, maximizar la distancia total entre elementos seleccionados es equivalente a maximizar la cobertura o la diversificación.

Las instancias utilizadas pertenecen a la colección MDG-a:

| Tipo | n | p | Instancias |
|------|---|---|------------|
| Pequeñas | 100 | 10 | 6 instancias |
| Grandes | 500 | 50 | 9 instancias |

---

## 2. Algoritmos implementados

### 2.1 GRASP (Greedy Randomized Adaptive Search Procedure)

GRASP es una metaheurística iterativa de dos fases que se repite mientras haya presupuesto de tiempo:

1. **Construcción**: se construye una solución greedy-aleatoria usando una Lista Restringida de Candidatos (RCL). El parámetro *alpha* controla el equilibrio entre codicia y aleatoriedad: `alpha = 0` es totalmente greedy (siempre el mejor candidato), `alpha = 1` es totalmente aleatorio. Con `alpha = -1`, se aleatoriza el propio alpha en cada iteración.

2. **Mejora local**: se aplica una búsqueda local de mejor mejora (*best-improvement*) sobre la solución construida, intercambiando un elemento seleccionado por uno no seleccionado hasta alcanzar un óptimo local.

La versión implementada usa un límite de tiempo global compartido entre todas las iteraciones GRASP.

### 2.2 Búsqueda Tabú (Tabu Search)

La Búsqueda Tabú mejora una solución mediante intercambios (1 elemento entra, 1 sale), aceptando también movimientos que empeoran la solución actual para escapar de óptimos locales. Para evitar ciclos, mantiene una **lista tabú**: los elementos recientemente eliminados de la solución no pueden re-entrar durante *tenure* iteraciones.

Componentes implementados:
- **Lista tabú FIFO**: los elementos eliminados se añaden al final; cuando supera la capacidad `tenure`, se elimina el más antiguo.
- **Criterio de aspiración**: un movimiento tabú puede aceptarse si produce una solución mejor que el mejor global conocido hasta ese momento.
- **Límite de tiempo** y **límite de iteraciones sin mejora** como criterios de parada.

### 2.3 GRASP + Búsqueda Tabú

La combinación usa GRASP para la fase de construcción y Búsqueda Tabú como fase de mejora. El presupuesto de tiempo es global: cada llamada a la Búsqueda Tabú recibe el tiempo restante del presupuesto total, no un tiempo fijo independiente. Esto garantiza que ninguna iteración monopolice el tiempo disponible.

---

## 3. Detalles de implementación

### 3.1 Representación de la solución

La solución se representa como un diccionario Python con tres campos:

```python
sol = {
    'sol': set(),      # conjunto de índices de nodos seleccionados
    'of': 0.0,         # valor de la función objetivo
    'instance': inst   # referencia a la instancia
}
```

La elección de `set` para almacenar los nodos seleccionados es deliberada: la operación de pertenencia (`v in sol['sol']`) es O(1), lo cual es crítico porque se ejecuta miles de veces en cada evaluación del vecindario.

### 3.2 Evaluación incremental de la función objetivo

Recomputar la función objetivo desde cero tras cada movimiento costaría O(p²) operaciones. En su lugar, se calcula la **variación marginal** de añadir o eliminar un nodo: la suma de las distancias entre ese nodo y todos los nodos actualmente en la solución. Esta variación, denominada `ofVariation`, se precalcula una vez y se usa para actualizar `sol['of']` de forma incremental:

```python
# Al eliminar un nodo u con variación precalculada:
sol['of'] -= ofVariation
sol['sol'].remove(u)

# Al añadir un nodo u con variación precalculada:
sol['of'] += ofVariation
sol['sol'].add(u)
```

Esta optimización reduce el coste de cada movimiento de O(p²) a O(p), un factor crítico para instancias con n=500 y p=50.

### 3.3 Fase de construcción GRASP

El primer nodo se elige **aleatoriamente** (no de forma greedy), asegurando diversidad desde el primer elemento. Para los nodos siguientes:

1. Se construye una lista de candidatos (todos los nodos no seleccionados) con su ganancia marginal actualizada.
2. Se calcula el umbral de la RCL: `threshold = gmax - alpha * (gmax - gmin)`.
3. Se añaden a la RCL todos los candidatos con ganancia >= threshold.
4. Se elige un elemento de la RCL al azar.
5. Las ganancias marginales de los candidatos restantes se actualizan de forma incremental: `c[0] += d[nuevo_nodo][c[1]]`.

El alfa adaptativo (`alpha = -1`) aleatoriza el propio valor de alpha en cada iteración GRASP, combinando automáticamente fases más greedy y más aleatorias dentro del mismo presupuesto de tiempo.

### 3.4 Búsqueda local de mejor mejora

La búsqueda local evalúa **todos los intercambios posibles** (v_out, v_in) donde v_out está en la solución y v_in no lo está. Para cada par, calcula la variación de la función objetivo:

```
delta = ofVariacion(v_in, sin v_out) - ofVariacion(v_out)
```

Se aplica el intercambio con mayor delta positivo. Si ningún delta es positivo, la búsqueda termina (se alcanzó un óptimo local respecto al vecindario de intercambio 1-1).

El coste por iteración es O(p × (n-p)). Para n=500, p=50, esto son 22.500 evaluaciones por iteración.

**Nota de implementación**: en una versión anterior, la búsqueda local solo evaluaba intercambios para el nodo seleccionado con menor contribución (no todos los nodos seleccionados). Esto es una heurística más rápida pero más débil, y no corresponde a la definición estricta de *best-improvement*. Se corrigió a la versión exhaustiva.

### 3.5 Búsqueda Tabú: lista y criterio de aspiración

La lista tabú es una lista Python estándar usada como cola FIFO:

```python
tabu_list.append(v_out)         # elemento eliminado -> entra en lista tabú
if len(tabu_list) > tenure:
    tabu_list.pop(0)            # el más antiguo sale
```

El **criterio de aspiración** permite ignorar el estado tabú de un movimiento si con ese movimiento se mejoraría el mejor global conocido:

```python
if v_in in tabu_list:
    if sol['of'] + delta > best_of:   # aspiración
        # registrar como candidato de aspiración
    continue

# si el movimiento de aspiración supera al mejor movimiento no-tabú, prevalece
```

Esta implementación es conservadora: la aspiración solo se activa cuando el movimiento no solo mejora la solución actual, sino que supera el mejor global. Además, el movimiento de aspiración solo prevalece si su ganancia es estrictamente mayor que la del mejor movimiento no-tabú disponible. Esto evita aceptar movimientos tabú que aunque mejoren el global, sean peores que una alternativa no-tabú.

### 3.6 Presupuesto de tiempo compartido en GRASP+TS

La integración de ambos algoritmos gestiona el tiempo de forma global:

```python
while time.time() - start_time < time_limit:
    remaining = time_limit - (time.time() - start_time)
    sol = cgrasp.construct(inst, alpha)
    tabu_search.improve(sol, time_limit=remaining, ...)
    if sol['of'] > best['of']:
        best = sol
```

El tiempo restante se pasa a cada llamada a la Búsqueda Tabú. Así, si la construcción de una iteración tarda más de lo habitual, la Búsqueda Tabú correspondiente dispondrá de menos tiempo, pero el presupuesto global siempre se respeta. La alternativa (asignar un tiempo fijo a cada componente) correría el riesgo de que iteraciones tardías quedaran sin tiempo para la fase de mejora.

### 3.7 Pipeline de experimentación: calibración secuencial y handoff JSON

La calibración de hiperparámetros podría haberse hecho con un grid completo (alpha × tenure), lo que con los valores planteados habría requerido aproximadamente 17 horas de cómputo. Se optó por una **calibración secuencial** en dos pasos:

1. Fijar tenure = 15 (valor central) y calibrar alpha.
2. Fijar el mejor alpha encontrado y calibrar tenure.

Esto reduce el coste a ~1.5 horas con muy poca pérdida de información, ya que la interacción entre alpha y tenure es baja a este nivel de presupuesto de tiempo.

Los mejores parámetros se guardan automáticamente en `experiments/calibration_summary.json`, que el script de comparación lee al arrancar. Si el fichero no existe, el script usa valores por defecto seguros. Este diseño evita que el experimento de comparación dependa de que el usuario copie manualmente los valores calibrados.

---

## 4. Experimentación

### 4.1 Configuración experimental

| Parámetro | Calibración | Comparación final |
|-----------|-------------|-------------------|
| Tiempo por run | 10 s | 30 s |
| Runs por configuración | 3 | 5 |
| Instancias usadas | 5 pequeñas + 5 grandes | 6 pequeñas + 9 grandes |
| Semilla base | 42 (+ índice de run) | 42 (+ índice de run) |

### 4.2 Calibración de alpha (GRASP)

**Instancias pequeñas (n=100)**: los seis valores de alpha produjeron exactamente el mismo resultado (OF media = 356.34, desviación estándar = 0). El algoritmo converge al mismo óptimo local independientemente del alpha. El valor seleccionado (alpha = 0.1) es un desempate, no una señal de sensibilidad real.

**Instancias grandes (n=500)**:

| Alpha | Avg Dev% | Media avg OF |
|-------|----------|--------------|
| **0.1** | **0.2536%** | **7694.55** |
| 0.25 | 0.2868% | 7691.99 |
| -1 | 0.3373% | 7688.07 |
| 0.9 | 0.5551% | 7671.26 |
| 0.5 | 0.5816% | 7669.25 |
| 0.75 | 0.7272% | 7658.02 |

GRASP con búsqueda local de mejor mejora prefiere **alpha bajo (0.1)**: soluciones de partida greedy dan mejores resultados porque la búsqueda local no puede escapar de cuencas de atracción locales; cuanto mejor la solución inicial, mejor el óptimo local alcanzado.

### 4.3 Calibración de (alpha, tenure) para GRASP+TS

**Alpha sweep (tenure fijado a 15)**:

| Alpha | Avg Dev% | Media avg OF |
|-------|----------|--------------|
| **0.9** | **0.1094%** | **7700.98** |
| 0.75 | 0.2635% | 7689.05 |
| 0.25 | 0.3319% | 7683.78 |
| -1 | 0.3714% | 7680.75 |
| 0.1 | 0.4696% | 7673.12 |
| 0.5 | 0.5106% | 7670.05 |

**Tenure sweep (alpha fijado a 0.9)**:

| Tenure | Avg Dev% | Media avg OF |
|--------|----------|--------------|
| **10** | **0.0906%** | **7705.39** |
| 15 | 0.1475% | 7700.98 |
| 20 | 0.1804% | 7698.44 |
| 30 | 0.2803% | 7690.76 |
| 25 | 0.2875% | 7690.20 |
| 5 | 0.3623% | 7684.35 |

**Hallazgo destacable**: GRASP+TS prefiere **alpha alto (0.9)**, lo opuesto a GRASP solo. La explicación es estructural: la Búsqueda Tabú es suficientemente potente para mejorar soluciones de baja calidad, y se beneficia de la diversidad que aportan puntos de partida más aleatorios. Con soluciones iniciales demasiado greedy, la Búsqueda Tabú converge rápido a la misma región del espacio de búsqueda en todas las iteraciones, reduciendo la exploración global.

La curva de tenure muestra un comportamiento no monótono: tenure = 5 es demasiado corto (el algoritmo cicla), valores por encima de 10 comienzan a bloquear movimientos buenos. El óptimo claro es tenure = 10.

**Parámetros seleccionados para la comparación final**:

| Grupo | GRASP alpha | GRASP+TS alpha | GRASP+TS tenure |
|-------|-------------|----------------|-----------------|
| Pequeñas (n=100) | 0.1 | 0.25 | 15 |
| Grandes (n=500) | 0.1 | 0.9 | 10 |

### 4.4 Comparación final — instancias pequeñas (n=100)

Ambos algoritmos producen **resultados idénticos en los 30 runs** (6 instancias × 5 runs). La desviación estándar es 0.0 en todos los casos. El test de Wilcoxon se omite porque todos los pares son empates exactos.

Conclusión: a esta escala, con un presupuesto de 30 segundos, la búsqueda local de mejor mejora ya converge al mismo óptimo local independientemente de si se aplica o no la Búsqueda Tabú encima. Las instancias pequeñas confirman que la implementación es correcta y consistente, pero no permiten discriminar entre los dos algoritmos.

### 4.5 Comparación final — instancias grandes (n=500)

**Parámetros**: GRASP con alpha = 0.1; GRASP+TS con alpha = 0.9, tenure = 10.

| Instancia | GRASP avg | GRASP std | TS avg | TS std | Delta (TS-GRASP) | Mejor obs. | GRASP=mejor | TS=mejor |
|-----------|-----------|-----------|--------|--------|------------------|------------|-------------|----------|
| MDG-a_2 | 7695.50 | 22.67 | 7694.42 | 40.22 | -1.1 | 7756.24 | - | si |
| MDG-a_5 | 7697.35 | 29.16 | 7635.25 | 77.71 | -62.1 | 7755.23 | - | si |
| MDG-a_6 | 7712.16 | 26.79 | 7691.21 | 31.49 | -20.9 | 7752.31 | si | - |
| MDG-a_9 | 7730.84 | 11.93 | 7700.91 | 40.82 | -29.9 | 7755.20 | - | si |
| MDG-a_13 | 7737.72 | 8.70 | 7747.95 | 36.99 | +10.2 | 7780.22 | - | si |
| MDG-a_16 | 7739.38 | 18.30 | 7690.25 | 31.04 | -49.1 | 7757.50 | si | - |
| MDG-a_17 | 7723.03 | 29.49 | 7704.35 | 54.84 | -18.7 | 7785.30 | - | si |
| MDG-a_19 | 7702.49 | 20.26 | 7677.74 | 28.99 | -24.7 | 7729.01 | si | - |
| MDG-a_20 | 7688.01 | 17.80 | 7658.29 | 33.11 | -29.7 | 7718.59 | si | - |

*"Mejor obs." = máximo observado en cualquier run de cualquier algoritmo para esa instancia.*

**Resumen agregado (instancias grandes)**:

| Métrica | GRASP | GRASP+TS |
|---------|-------|----------|
| Avg dev% | 0.5200% | 0.8443% |
| Desv. estándar media | 20.57 | 41.69 |
| Instancias en que alcanza el mejor observado | 4/9 | 5/9 |
| Wins en comparación pareada (45 pares) | **30** | 15 |
| Delta medio (TS - GRASP) | - | -25.13 |
| Wilcoxon W | - | 256.0 |
| Wilcoxon p-valor | - | **0.0026** |

El test de Wilcoxon signed-rank (bilateral, `zero_method="wilcox"`, 45 pares no empatados) confirma que la ventaja de GRASP sobre GRASP+TS en calidad media de run es **estadísticamente significativa** (p = 0.0026, nivel de significancia 0.05).

**Caso MDG-a_5**: este es el ejemplo más extremo de la varianza de GRASP+TS. En un run alcanzó el mejor valor observado (7755.23), pero tres runs cayeron por debajo de 7620 (peor: 7560.80), resultando en la mayor desviación estándar del benchmark (77.71) y el mayor delta negativo (-62.1). No es ruido aleatorio: es consecuencia directa de que GRASP+TS realiza menos reinicios por presupuesto de tiempo, explorando menos regiones del espacio de búsqueda.

---

## 5. Discusión y conclusiones

### 5.1 Trade-off exploración vs. explotación bajo un presupuesto fijo

El resultado principal no es que un algoritmo domine al otro, sino que hay un **trade-off entre amplitud y profundidad** condicionado al presupuesto de tiempo:

- **GRASP** completa muchos reinicios cortos (construcción + búsqueda local). Con 30 segundos, alcanza mayor calidad media y menor varianza: avg dev% 0.52%, desv. estándar media 20.6, 30 de 45 wins, diferencia estadísticamente significativa (p = 0.0026).

- **GRASP+TS** invierte más tiempo en explotar cada solución construida. Llega a valores máximos más altos en más instancias (5/9 vs 4/9), pero lo hace con mayor varianza e irregularidad. Cuando acierta, alcanza soluciones que GRASP nunca encontrará con ninguna semilla.

Este trade-off está corroborado por el hallazgo de calibración: GRASP se beneficia de soluciones iniciales greedy (alpha = 0.1) para que la búsqueda local rápida sea eficiente, mientras que GRASP+TS se beneficia de soluciones iniciales aleatorias (alpha = 0.9) para que la Búsqueda Tabú tenga más diversidad con la que trabajar. La política óptima de construcción depende de la fuerza de la fase de mejora.

### 5.2 ¿Contribuye la Búsqueda Tabú a mejorar GRASP?

La respuesta es **condicional**:

- En **instancias pequeñas (n=100)**: no, porque ambos algoritmos saturan al mismo óptimo local. El problema es suficientemente fácil a esta escala.

- En **instancias grandes (n=500) con 30 segundos**: GRASP puro produce mejor calidad media. GRASP+TS produce mejores picos. La Búsqueda Tabú mejora la capacidad de encontrar los mejores valores del espacio, pero a costa de consistencia.

- Con un **presupuesto mayor** (p. ej., 120 segundos), la situación cambia probablemente. GRASP+TS completaría más reinicios y su mayor capacidad de explotación por iteración comenzaría a compensar. La ventaja de GRASP en breadth es mayor cuando el tiempo es corto; la ventaja de TS en depth es mayor cuando el tiempo es suficiente para explotar varias regiones.

### 5.3 Limitaciones y trabajo futuro

- El array `freq` (frecuencia de selección de cada nodo) se registra en la Búsqueda Tabú pero no se usa para diversificación. Podría usarse para penalizar nodos muy frecuentes en fases de diversificación, una extensión estándar de la Búsqueda Tabú a largo plazo.

- La calibración es secuencial, lo que puede perderse interacciones entre alpha y tenure. En un proyecto con más tiempo computacional, un grid completo o una búsqueda bayesiana permitiría explorar el espacio conjunto.

- Sin tiempo de cómputo extendido, no es posible confirmar empíricamente la conjetura sobre presupuestos mayores. Queda como hipótesis fundamentada en la estructura del algoritmo.

---

## Ficheros entregados

| Fichero | Descripción |
|---------|-------------|
| `algorithms/grasp.py` | GRASP + búsqueda local, versión con límite de iteraciones |
| `algorithms/grasp_timed.py` | GRASP + búsqueda local, versión con límite de tiempo |
| `algorithms/grasp_ts.py` | GRASP + Búsqueda Tabú con presupuesto de tiempo global |
| `constructives/cgrasp.py` | Construcción greedy-aleatoria (RCL) |
| `localsearch/lsbestimp.py` | Búsqueda local de mejor mejora exhaustiva |
| `localsearch/tabu_search.py` | Búsqueda Tabú con criterio de aspiración |
| `structure/instance.py` | Lectura de instancias MDG |
| `structure/solution.py` | Representación de soluciones |
| `experiments/calibration.py` | Pipeline de calibración secuencial |
| `experiments/comparison.py` | Comparación con test de Wilcoxon |
| `experiments/generate_excel.py` | Generación del fichero Excel |
| `experiments/resultados.xlsx` | Tablas de experimentación (5 pestañas) |
