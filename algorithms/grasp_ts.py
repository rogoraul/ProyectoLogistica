import time
from constructives import cgrasp
from localsearch import tabu_search


# --------- #
# GRASP +TS #
# --------- #

def execute(inst, alpha, time_limit=30, tabu_tenure=10, max_iter=5000,
            dynamic=False, tenure_min=5, tenure_max=20, verbose=False):
    """
    GRASP + Tabu Search executed under a global time limit.

    The algorithm repeatedly constructs a greedy-random solution and
    applies Tabu Search as the improvement phase. Both phases share
    the same global wall-clock budget (time_limit seconds).

    Parameters
    ----------
    inst        : instance dict produced by instance.readInstance()
    alpha       : GRASP greediness parameter (-1 = random per iteration)
    time_limit  : total wall-clock seconds for the full execute() call
    tabu_tenure : fixed tabu list size (used when dynamic=False)
    max_iter    : max iterations without improvement inside Tabu Search
    dynamic     : use dynamic tenure instead of fixed
    tenure_min  : lower bound for dynamic tenure
    tenure_max  : upper bound for dynamic tenure
    verbose     : print iteration log
    """
    start_time = time.time()
    best = None
    iteration = 0
    history = []   # [(iteration, elapsed_s, best_of)] — appended each time best improves

    while time.time() - start_time < time_limit:
        iteration += 1
        elapsed = time.time() - start_time
        remaining = time_limit - elapsed

        if remaining <= 0:
            break

        sol = cgrasp.construct(inst, alpha)

        if verbose:
            print(f"  Iter {iteration}: C -> {round(sol['of'], 2)}", end=", ")

        # Each TS call gets the remaining global time as its own limit.
        # max_iter acts as a secondary safety brake.
        tabu_search.improve(
            sol,
            tabu_tenure=tabu_tenure,
            max_iter=max_iter,
            time_limit=remaining,
            dynamic=dynamic,
            tenure_min=tenure_min,
            tenure_max=tenure_max
        )

        if verbose:
            print(f"TS -> {round(sol['of'], 2)}")

        if best is None or sol['of'] > best['of']:
            best = sol
            history.append((iteration, round(time.time() - start_time, 3), round(best['of'], 2)))

    best['history'] = history
    return best
