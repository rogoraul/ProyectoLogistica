import time
from constructives import cgrasp
from localsearch import lsbestimp


# ----------- #
# GRASP TIMED #
# ----------- #

def execute(inst, alpha, time_limit=30, verbose=False):
    """
    Baseline GRASP with best-improvement local search, stopped by time limit.

    Parameters
    ----------
    inst       : instance dict produced by instance.readInstance()
    alpha      : GRASP greediness parameter (-1 = random per iteration)
    time_limit : total wall-clock seconds for the full execute() call
    verbose    : print iteration log
    """
    start_time = time.time()
    best = None
    iteration = 0

    while time.time() - start_time < time_limit:
        iteration += 1
        sol = cgrasp.construct(inst, alpha)

        if verbose:
            print(f"  Iter {iteration}: C -> {round(sol['of'], 2)}", end=", ")

        lsbestimp.improve(sol)

        if verbose:
            print(f"LS -> {round(sol['of'], 2)}")

        if best is None or sol['of'] > best['of']:
            best = sol

    return best
