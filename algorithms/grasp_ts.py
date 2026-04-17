import time
from constructives import cgrasp
from localsearch import tabu_search


def execute(inst, alpha, time_limit=30, tabu_tenure=10, max_iter=5000):
    start = time.time()
    best = None

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
        )
        if best is None or best['of'] < sol['of']:
            best = sol

    return best
