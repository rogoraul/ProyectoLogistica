import copy
import time
import random
from structure import solution


# ----------- #
# TABU SEARCH #
# ----------- #

def improve(sol, tabu_tenure=10, max_iter=5000, time_limit=30,
            dynamic=False, tenure_min=5, tenure_max=20):
    """
    Tabu Search local search phase.

    Parameters
    ----------
    sol         : solution dict (modified in place, best is restored at end)
    tabu_tenure : fixed list size when dynamic=False
    max_iter    : maximum iterations without improvement before stopping
    time_limit  : wall-clock seconds limit for the whole improve call
    dynamic     : if True, tenure varies randomly in [tenure_min, tenure_max]
    tenure_min  : lower bound for dynamic tenure
    tenure_max  : upper bound for dynamic tenure
    """
    start_time = time.time()
    best_sol = copy.deepcopy(sol)
    tabu_list = []
    freq = [0] * sol['instance']['n']

    for v in sol['sol']:
        freq[v] += 1

    iter_no_improve = 0
    current_tenure = tabu_tenure

    while iter_no_improve < max_iter:

        # -------------- #
        # TIME CRITERION #
        # -------------- #
        if time.time() - start_time >= time_limit:
            break

        # -------------------- #
        # DYNAMIC TENURE CHECK #
        # -------------------- #
        if dynamic:
            current_tenure = random.randint(tenure_min, tenure_max)

        v_out, of_var_out, v_in, of_var_in = selectInterchange(sol, tabu_list, best_sol['of'])

        if v_out == -1:
            break

        solution.removeFromSolution(sol, v_out, of_var_out)
        solution.addToSolution(sol, v_in, of_var_in)

        # -------------- #
        # UPDATE FREQ    #
        # -------------- #
        freq[v_in] += 1

        # -------------- #
        # UPDATE TABU    #
        # -------------- #
        tabu_list.append(v_out)
        if len(tabu_list) > current_tenure:
            tabu_list.pop(0)

        # -------------------- #
        # UPDATE BEST SOLUTION #
        # -------------------- #
        if sol['of'] > best_sol['of']:
            best_sol = copy.deepcopy(sol)
            iter_no_improve = 0
        else:
            iter_no_improve += 1

    sol['sol'] = best_sol['sol']
    sol['of'] = best_sol['of']
    sol['instance'] = best_sol['instance']
    sol['freq'] = freq


# -------------------- #
# SELECT INTERCHANGE   #
# -------------------- #

def selectInterchange(sol, tabu_list, best_of):
    n = sol['instance']['n']
    best_delta = None
    best_v_out = -1
    best_v_in = -1
    best_of_var_out = 0
    best_of_var_in = 0

    # Aspiration: best tabu move that would exceed best_of
    asp_delta = None
    asp_v_out = -1
    asp_v_in = -1
    asp_of_var_out = 0
    asp_of_var_in = 0

    for v_out in sol['sol']:
        of_var_out = solution.distanceToSol(sol, v_out)
        for v_in in range(n):
            if solution.contains(sol, v_in):
                continue
            of_var_in = solution.distanceToSol(sol, v_in, without=v_out)
            delta = of_var_in - of_var_out

            if v_in in tabu_list:
                # Aspiration criterion: override tabu status if move beats best known
                if sol['of'] + delta > best_of:
                    if asp_delta is None or delta > asp_delta:
                        asp_delta = delta
                        asp_v_out = v_out
                        asp_v_in = v_in
                        asp_of_var_out = round(of_var_out, 2)
                        asp_of_var_in = round(of_var_in, 2)
                continue

            if best_delta is None or delta > best_delta:
                best_delta = delta
                best_v_out = v_out
                best_v_in = v_in
                best_of_var_out = round(of_var_out, 2)
                best_of_var_in = round(of_var_in, 2)

    # Prefer aspiration move only if it outperforms the best non-tabu move
    if asp_delta is not None and (best_delta is None or asp_delta > best_delta):
        return asp_v_out, asp_of_var_out, asp_v_in, asp_of_var_in

    return best_v_out, best_of_var_out, best_v_in, best_of_var_in