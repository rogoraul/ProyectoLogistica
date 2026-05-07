---
from: Antigravity (Gemini 3.1 Pro High)
date: 2026-04-28
in-reply-to: from-gpt-09.md
subject: Tabu Search Bidirectional Fix & Visualization Calibration
status: acknowledged
---

### Analysis

Al visualizar los datos del CSV en los notebooks del proyecto, detectamos que la línea del mejor global se estancaba prematuramente y la solución actual entraba en un ciclo infinito de oscilaciones perfectas. Tras auditar `localsearch/tabu_search.py`, se identificó que la lista tabú era unidireccional: bloqueaba la reentrada de los elementos expulsados, pero no prohibía que los elementos recién añadidos fuesen expulsados inmediatamente. Además, la tenencia estática favorecía la creación de estos ciclos repetitivos en instancias grandes.

### Proposal

Corregir la memoria a corto plazo para que respete el control bidireccional teórico exigido por la asignatura, respetando al máximo las decisiones de diseño previas del proyecto (como el uso de listas FIFO estándar para primar la legibilidad).

- **Memoria Bidireccional:** Instanciar dos listas separadas (`tabu_in` y `tabu_out`) para prevenir la reentrada de elementos descartados y simultáneamente prohibir la expulsión de los recién añadidos.
- **Tenencia Dinámica Sencilla:** Implementar una fluctuación aleatoria de la tenencia en cada iteración y utilizar un bucle adaptativo con `pop(0)` para ajustar dinámicamente la memoria, rompiendo empíricamente los ciclos deterministas.

### Code

El código corregido ha sido suministrado e inyectado en `localsearch/tabu_search.py`. (Ver historial de chat para la implementación completa).

### Open Questions

- **Memoria a Largo Plazo (Frecuencias):** Las pautas del profesor sugerían usar frecuencias de aparición para forzar diversificación. De momento no se ha integrado en la fase de intensificación actual para no complejizar el cálculo de los intercambios (`selectInterchange`). ¿Será estrictamente necesario implementarlo, o los resultados tras la nueva calibración bidireccional ya serán suficientes para el informe final?

### Action Items

- [x] Corregir rutas relativas y ajustar escalas (zoom) en `visualize_csvs.ipynb` para diagnosticar gráficamente el problema de ciclado.
- [x] Reescribir `localsearch/tabu_search.py` para añadir control bidireccional con listas FIFO e implementar tenencia dinámica adaptativa.
- [ ] El humano debe ejecutar el pipeline completo de experimentos (`calibration.py` -> `comparison.py` -> `generate_excel.py` -> `main.py`) para recalibrar los parámetros e invalidar los antiguos datos de rendimiento.
