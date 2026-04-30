---
from: Gemini gemini-1.5-pro
date: 2026-04-28
in-reply-to: from-gemini-02.md
subject: Strategic Plan - Addressing Professor's Feedback on Time & Evolution
status: implemented
---

### Analysis
El usuario y yo acabamos de trazar la estrategia final para incorporar el feedback de su profesor de forma extremadamente eficiente, sin desechar los resultados estadísticos (a 30s) que ya tenemos calculados en `experiments/comparison_results.csv`.

El profesor solicitó:
1. Observar gráficamente cómo evoluciona Tabu Search (cómo empeora soluciones temporalmente para escapar de óptimos locales).
2. Estudiar el impacto del tiempo de ejecución, asumiendo que TS se distanciará de GRASP si se le concede más tiempo para buscar.

Realizar ejecuciones discretas repetidas (10s, 30s, 60s) en todas las instancias es matemáticamente redundante y costoso. Asimismo, graficar la evolución de la lista tabú en las 15 instancias saturaría innecesariamente el informe académico.

### Proposal
Nuestra estrategia "quirúrgica" (acordada explícitamente con el usuario) es la siguiente:

1. **Evolución interna del Tabú:** Utilizaremos el archivo que ya generó el pipeline anterior (`csv_final/ts_evolution_single_restart.csv`) para graficar un único "electrocardiograma" de una instancia representativa. Esto demuestra visualmente la mecánica del algoritmo sin saturar el TFG.
2. **Impacto del Tiempo (Curvas de Convergencia):** Implementaremos un muestreo continuo del tiempo. En lugar de tocar el `main.py` o ejecutar las 15 instancias, correremos un experimento aislado de **180 segundos** solo en 2 o 3 de las instancias Grandes más difíciles (ej. `MDG-a_16_n500_m50.txt`, `MDG-a_13_n500_m50.txt`). 

### Action Items
Te dejo el testigo para que implementes la parte de código. **Recuerda usar *chat diffs* o bloques de código en el chat**, respetando las <user_global> rules de no sobrescribir ni generar los scripts por tu cuenta:

- [ ] **Fix Tracking Bug:** Modifica `localsearch/tabu_search.py` para corregir el bug mencionado en el mensaje anterior. El algoritmo debe registrar/devolver el `time.time() - start_time` exacto cada vez que logre mejorar el `global_best`.
- [ ] **Nuevo script `experiments/time_analysis.py`:** Redacta un script aislado que instancie GRASP y GRASP+TS en las 2-3 instancias seleccionadas, los ejecute durante 180s y guarde el histórico de convergencia en `csv_final/convergence_curves_large.csv`.
- [ ] **Actualización Visual:** Ofrécele al usuario el código de Python (o celdas de Jupyter) para plotear estos nuevos datos respondiendo directamente a la petición de su tribunal.
