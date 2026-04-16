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
    sel = -1
    bestSel = 0
    unsel = -1
    bestUnsel = 0
    bestDelta = None

    for s in sol['sol']:
        dSel = solution.distanceToSol(sol, s)
        for u in range(n):
            if solution.contains(sol, u):
                continue

            dUnsel = solution.distanceToSol(sol, u, without=s)
            delta = dUnsel - dSel
            if bestDelta is None or delta > bestDelta:
                bestDelta = delta
                sel = s
                bestSel = round(dSel, 2)
                unsel = u
                bestUnsel = round(dUnsel, 2)

    return sel, bestSel, unsel, bestUnsel
