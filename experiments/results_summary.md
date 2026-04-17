# Resumen y análisis de los resultados en la carpeta `experiments`

Fecha de generación: 2026-04-17

Este documento resume y analiza los resultados contenidos en los archivos CSV/JSON del directorio `experiments`. Se han inspeccionado y consolidado los siguientes ficheros: `calibration_summary.json`, `calibration_grasp_summary.csv`, `calibration_grasp.csv`, `calibration_grasp_runs.csv`, `calibration_ts.csv`, `calibration_ts_runs.csv`, `calibration_ts_summary.csv`, `comparison_results.csv`, `comparison_runs.csv` y `comparison_tests.json`.

Objetivo del análisis
- Identificar las mejores configuraciones de parámetros para las variantes GRASP y GRASP+TS (Tabu Search) en dos grupos de instancias (`small`, n≈100; y `large`, n≈500).
- Resumir comportamiento por instancia y por grupo: calidad de solución (desviación respecto a referencia), estabilidad (desviación estándar / variabilidad entre ejecuciones) y coste temporal medio.
- Interpretar los test estadísticos y proponer recomendaciones de configuración.

Resumen ejecutivo
- Para el conjunto `small` (instancias con n≈100): ambas técnicas (GRASP y GRASP+TS) alcanzan soluciones idénticas a las referencias en la mayoría de configuraciones; la variabilidad es prácticamente nula y no hay diferencias relevantes entre parámetros explorados. Esto provoca que muchos pares resulten empatados en las comparaciones.
- Para el conjunto `large` (instancias con n≈500): los experimentos de calibración y las métricas agregadas muestran que GRASP alcanza su mejor rendimiento con `alpha = 0.1` (desviación promedio ≈ 0.2536%), mientras que la combinación con Tabu Search (TS) obtiene mejores promedios con `alpha = 0.9` y `tenure = 10` (desviación promedio ≈ 0.0906%). En resumen: GRASP+TS domina en calidad promedio en las instancias grandes.
- El test de comparación emparejada (Wilcoxon) sobre las diferencias entre TS y GRASP en el grupo `large` arroja un p-valor de 0.002628 (estadísticamente significativo) y una diferencia media `mean_delta_ts_minus_grasp = -25.1271` (signo negativo que indica que, en promedio, la métrica asociada al algoritmo TS es mejor en la dirección medida). Para el grupo `small` la prueba fue omitida por estar todas las parejas empatadas.

Descripción de los ficheros analizados
- `calibration_summary.json`: JSON con resumen de la calibración global por grupos (`small`/`large`) y por método (GRASP y TS); contiene los mejores parámetros y la desviación media asociada.
- `calibration_grasp_summary.csv`: resumen por `alpha` de GRASP (por grupo) con `avg_dev_pct` y tiempos medios.
- `calibration_grasp.csv` y `calibration_grasp_runs.csv`: resultados por instancia y por ejecución (of = objective function), tiempos y desviaciones.
- `calibration_ts.csv` y `calibration_ts_runs.csv`: resultados análogos para el procedimiento con Tabu Search (incluye barridos por `alpha` y `tenure`).
- `calibration_ts_summary.csv`: resumen agregado para TS (barridos de `alpha` y `tenure`).
- `comparison_results.csv` y `comparison_runs.csv`: comparaciones finales por instancia entre las configuraciones seleccionadas para GRASP y GRASP+TS (promedios y estadísticas resumen por instancia).
- `comparison_tests.json`: resultados de las pruebas estadísticas emparejadas (conteo de wins/ties, estadísticos de Wilcoxon y p-valores) separadas por grupo y global.

Lectura rápida de los números clave
- `calibration_summary.json` (extracto):
  - `small`: GRASP best_alpha = 0.1 (best_avg_dev_pct = 0.0); TS best_alpha = 0.25, best_tenure = 15 (best_avg_dev_pct = 0.0). Conclusión: para instancias pequeñas ambas técnicas logran soluciones equivalentes al benchmark.
  - `large`: GRASP best_alpha = 0.1 (best_avg_dev_pct = 0.2536); TS best_alpha = 0.9, best_tenure = 10 (best_avg_dev_pct = 0.0906). Conclusión: TS mejora la calidad en promedio en instancias grandes.
- `calibration_grasp_summary.csv`: para `large` la desviación relativa promedio (`avg_dev_pct`) por `alpha` muestra que `alpha=0.1` es el mejor entre los examinados (≈0.2536%), y valores de `alpha` más altos (0.5, 0.75, 0.9) empeoran la desviación.
- `calibration_ts_summary.csv`: para `large` `alpha=0.9` y barridos de `tenure` muestran el mejor resultado en promedio con `tenure=10` (≈0.0906%). En `small` la mayoría de configuraciones devuelven `avg_dev_pct = 0.0`.
- `comparison_tests.json`:
  - `overall`: n_pairs = 75, wins_grasp = 30, wins_ts = 15, ties = 30, mean_delta_ts_minus_grasp = -15.0763, pvalue = 0.002628 → hay evidencia estadística de diferencia global.
  - `small`: todas las parejas empatadas (skipped).
  - `large`: n_pairs = 45, wins_grasp = 30, wins_ts = 15, ties = 0, mean_delta_ts_minus_grasp = -25.1271, pvalue = 0.002628 → diferencia significativa en `large`.

Interpretación detallada
1) Efecto del tamaño de la instancia
- Instancias `small` (n≈100) son relativamente fáciles respecto al presupuesto de tiempo usado en los experimentos: tanto GRASP como GRASP+TS alcanzan la solución de referencia de forma estable (variación nula en muchas ejecuciones). Por eso los resultados de calibración y las comparaciones aparecen como empates. Cuando todas las ejecuciones devuelven la misma `of` para todas las semillas/configuraciones, las pruebas emparejadas quedan sin información útil y el análisis estadístico se marca como `skipped`.
- Instancias `large` (n≈500) presentan diferencias donde la fase de búsqueda local/intenificación importa: GRASP por sí solo tiene mayor sensibilidad al parámetro `alpha` y, aun con el mejor `alpha` (0.1), mantiene una desviación promedio mayor que la versión con Tabu Search. La combinación con TS reduce la desviación promedio de forma consistente.

2) ¿Por qué TS mejora en instancias grandes?
- Intensificación: Tabu Search proporciona una búsqueda local más agresiva y memoria (tenure) que permite escapar de ciclos locales y explorar vecindarios más amplios; en instancias grandes esto suele traducirse en mejoras de magnitud mayor.
- Control de diversificación/exploración: en GRASP el parámetro `alpha` controla cuánto azar introducir en la construcción; en instancias grandes un `alpha` bajo (0.1) produce soluciones iniciales relativamente buenas y consistentes. Sin embargo, TS puede explotar mejor buenas semillas y refinar soluciones con mayor efecto cuando el espacio de soluciones es grande.
- Tiempo de ejecución vs ganancia: los tiempos medios reportados por los CSV de calibración muestran que las ejecuciones tienen tiempos comparables (orden de 10s por ejecución en calibraciones y ~30s en las comparaciones finales), por lo que las mejoras de TS no provienen de un mayor presupuesto de tiempo sino del propio método de búsqueda local.

3) Discrepancia entre conteo de `wins` y diferencia media (`mean_delta`)
- Observación: en el grupo `large` el conteo de pares favorece a GRASP (wins_grasp = 30; wins_ts = 15) pero la `mean_delta_ts_minus_grasp` es negativa y de magnitud ≈ -25.1271.
- Interpretación: estos dos indicadores miden cosas distintas. El conteo de `wins` registra en cuántas instancias un algoritmo obtuvo la mejor solución (por cantidad de pares), sin tener en cuenta la magnitud de la diferencia. La diferencia media (y la prueba de Wilcoxon) consideran la magnitud y la distribución de las diferencias emparejadas. Por tanto, es compatible que GRASP gane con pequeñas mejoras en más instancias, mientras que TS ofrezca grandes mejoras en menos instancias; la suma/mediana de esas diferencias puede resultar a favor de TS y dar un valor promedio negativo.
- Resultado práctico: la significativa `pvalue = 0.002628` indica que la diferencia en la distribución de pares no es atribuible al azar; la dirección de `mean_delta` sugiere que, en términos de magnitud media de la mejora, TS es preferible en `large`.

4) Robustez y variabilidad
- Las columnas `std_of` en los CSV de calibración muestran que en `small` la desviación estándar es 0.0 en muchas configuraciones (soluciones idénticas entre repeticiones). En `large` las `std_of` varían (ej. 20–50 en algunas instancias), lo que indica que la dispersión entre ejecuciones es apreciable.
- El `avg_dev_pct` agregado resulta útil para comparar a nivel grupo: GRASP presenta valores alrededor de 0.25–0.58% según `alpha`, mientras que TS reduce esa desviación al rededor de 0.09–0.47% según `alpha` y `tenure` (mejor combinación en `large`: alpha=0.9, tenure=10 → ~0.0906%).

Conclusiones y recomendaciones
1. Recomendación operativa de parámetros:
  - Para instancias pequeñas (`small`, n≈100): usar configuraciones conservadoras por simplicidad: GRASP con `alpha = 0.1` es una buena opción por su estabilidad; añadir TS no aporta mejoras significativas dadas las condiciones experimentales. Si el objetivo es simplicidad y velocidad de implementación mantener sólo GRASP.
  - Para instancias grandes (`large`, n≈500): preferir la variante con Tabu Search. De la calibración, la combinación recomendada es `alpha = 0.9` con `tenure = 10` (o tomar la recomendación del `alpha_sweep` y `tenure_sweep` que sugieren esa pareja), porque consigue la menor `avg_dev_pct` promedio (~0.0906%). Sin embargo, también hay evidencia de que GRASP con `alpha = 0.1` muestra buen comportamiento (más wins), por lo que una opción práctica es ejecutar ambas configuraciones en paralelo y seleccionar la mejor solución final.

2. Interpretación estadística:
  - El test de Wilcoxon (p ≈ 0.0026) en el grupo `large` señala una diferencia estadísticamente significativa entre las distribuciones emparejadas de resultados; por tanto, la mejora observada con TS no es sólo ruido de muestreo.
  - Para `small` no hay evidencia de diferencia (todos los pares empatados), por tanto no debe invertirse tiempo en optimizar parámetros para ese grupo salvo por requisitos específicos de tiempo/implementación.

3. Sugerencias para experimentación futura y verificación adicional:
  - Aumentar el número de repeticiones por configuración para refinar intervalos de confianza y estimaciones de varianza, especialmente en `large` donde la dispersión es mayor.
  - Reportar además de `avg_of` y `avg_dev_pct` medidas robustas como mediana, cuantiles y percentiles (p. ej. 25/75), para caracterizar casos con grandes saltos en rendimiento.
  - Evaluar el coste/beneficio en tiempo real (ej. curvas calidad-tiempo) para comparar si la inclusión de TS sigue siendo ventajosa bajo presupuestos de tiempo más restrictivos.
  - Realizar un análisis por instancia para identificar subclases de instancias donde GRASP o TS sean particularmente buenos (por topología, densidad, m, etc.).

Anexo: tablas rápidas (extracto de resultados)

- `calibration_summary.json` (valores clave):
  - small:
    - GRASP best_alpha = 0.1 → best_avg_dev_pct = 0.0
    - TS best_alpha = 0.25, best_tenure = 15 → best_avg_dev_pct = 0.0
  - large:
    - GRASP best_alpha = 0.1 → best_avg_dev_pct = 0.2536
    - TS best_alpha = 0.9, best_tenure = 10 → best_avg_dev_pct = 0.0906

- `calibration_grasp_summary.csv` (fragmento para `large`):
  - alpha=0.1 → avg_dev_pct = 0.2536 (mean_avg_of ≈ 7694.55)
  - alpha=0.25 → avg_dev_pct = 0.2868
  - alpha=-1  → avg_dev_pct = 0.3373
  - alpha=0.9 → avg_dev_pct = 0.5551

- `calibration_ts_summary.csv` (fragmento para `large`):
  - alpha=0.9 (alpha_sweep, tenure=15) → avg_dev_pct = 0.1094
  - tenure_sweep alpha=0.9, tenure=10 → avg_dev_pct = 0.0906 (mejor encontrado)

- `comparison_tests.json` (valores clave):
  - overall: n_pairs=75, wins_grasp=30, wins_ts=15, ties=30, mean_delta_ts_minus_grasp=-15.0763, pvalue=0.002628
  - small: skipped (todas las parejas empatadas)
  - large: n_pairs=45, wins_grasp=30, wins_ts=15, ties=0, mean_delta_ts_minus_grasp=-25.1271, pvalue=0.002628

Notas finales y advertencias
- Interpretación de señales opuestas (más `wins` vs mejor `mean_delta`): ambos son estadísticamente válidos; la decisión práctica debe considerar qué métrica interesa más: frecuencia de ganar (nº de instancias donde un método es mejor) o magnitud media de la mejora. Si se buscan ganancias grandes ocasionales, TS parece más apropiado; si se prefiere ganar con consistencia pequeña, GRASP puro (alpha bajo) puede ofrecer más wins.
- Siempre confirmar la dirección del objetivo (minimizar o maximizar) con el equipo o la documentación del problema. En este conjunto de datos las columnas `avg_of` parecen representar el valor objetivo en la misma dirección para ambos algoritmos y la `avg_dev_pct` se calcula respecto a una referencia, por lo que la interpretación numérica de mejoras y desviaciones en este informe está basada en esos porcentajes mostrados en los archivos de calibración.

Si quieres, continúo con cualquiera de estas acciones:
- Guardar este fichero en repo y hacer commit + push (lo puedo hacer ahora).
- Generar tablas adicionales (CSV) con los resúmenes numéricos usados para tablas del documento.
- Hacer gráficos (calidad vs parámetros, histogramas de diferencias, boxplots para `large`) y añadir las figuras al informe.

--
*Fin del informe generado automáticamente a partir de los archivos en `experiments`.*
