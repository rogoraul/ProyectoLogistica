from structure import solution

def improve(sol):
    improve = True
    while improve:
        improve = tryImprove(sol)


def tryImprove(sol):
    sel, ofVarSel, unsel, ofVarUnsel = selectInterchange(sol)
    if ofVarSel < ofVarUnsel:
        solution.removeFromSolution(sol, sel, ofVarSel)
        solution.addToSolution(sol, unsel, ofVarUnsel)
        return True
    return False


def selectInterchange(sol):
    n = sol['instance']['n']
    best_delta = None
    best_v_out = -1
    best_v_in = -1
    best_of_var_out = 0
    best_of_var_in = 0

    for v_out in sol['sol']:
        of_var_out = solution.distanceToSol(sol, v_out)
        for v_in in range(n):
            if solution.contains(sol, v_in):
                continue
            of_var_in = solution.distanceToSol(sol, v_in, without=v_out)
            delta = of_var_in - of_var_out
            if best_delta is None or delta > best_delta:
                best_delta = delta
                best_v_out = v_out
                best_v_in = v_in
                best_of_var_out = round(of_var_out, 2)
                best_of_var_in = round(of_var_in, 2)

    return best_v_out, best_of_var_out, best_v_in, best_of_var_in