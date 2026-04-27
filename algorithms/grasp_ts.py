import time
from constructives import cgrasp
from localsearch import tabu_search


def execute(
    inst,
    alpha,
    time_limit=30,
    tabu_tenure=10,
    max_iter=5000,
    convergence_log=None,
    algorithm_name="GRASP+TS",
    ts_evolution_csv_path=None,
):
    start = time.time()
    best = None
    ts_evolution_pending = ts_evolution_csv_path is not None

    while time.time() - start < time_limit:
        remaining = time_limit - (time.time() - start)
        if remaining <= 0:
            break

        sol = cgrasp.construct(inst, alpha)
        tabu_search.improve(
            sol,
            tabu_tenure=tabu_tenure,
            max_iter=max_iter,
            time_limit=remaining,
            evolution_csv_path=ts_evolution_csv_path if ts_evolution_pending else None,
        )
        ts_evolution_pending = False

        if best is None or best['of'] < sol['of']:
            best = sol
            if convergence_log is not None:
                convergence_log.append({
                    "Algorithm": algorithm_name,
                    "Elapsed_Time": round(time.time() - start, 6),
                    "Best_Objective": round(best['of'], 2),
                })

    return best
