import time
from constructives import cgrasp
from localsearch import lsbestimp


def execute(inst, alpha, time_limit=30):
    start = time.time()
    best = None

    while time.time() - start < time_limit:
        sol = cgrasp.construct(inst, alpha)
        lsbestimp.improve(sol)
        if best is None or best['of'] < sol['of']:
            best = sol

    return best
