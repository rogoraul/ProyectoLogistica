import time
from constructives import cgrasp
from localsearch import lsbestimp


def execute(inst, alpha, time_limit=30, convergence_log=None, algorithm_name="GRASP"):
    start = time.time()
    best = None

    while time.time() - start < time_limit:
        sol = cgrasp.construct(inst, alpha)
        lsbestimp.improve(sol)
        if best is None or best['of'] < sol['of']:
            best = sol
            if convergence_log is not None:
                convergence_log.append({
                    "Algorithm": algorithm_name,
                    "Elapsed_Time": round(time.time() - start, 6),
                    "Best_Objective": round(best['of'], 2),
                })

    return best
