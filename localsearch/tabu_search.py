# ------------------------- #
# TABU SEARCH RAFA-APPROVED #
# ------------------------- #
import copy
import csv
import time
import random
from structure import solution


def improve(
    sol,
    tabu_tenure=10,
    max_iter=5000,
    time_limit=30,
    evolution_csv_path=None,
    convergence_log=None,
    algorithm_name="GRASP+TS",
    convergence_start_time=None,
    convergence_best_objective=None,
):
    start = time.time()
    convergence_start_time = convergence_start_time if convergence_start_time is not None else start
    convergence_best = convergence_best_objective if convergence_best_objective is not None else sol['of']
    best_sol = copy.deepcopy(sol)
    
    # Listas FIFO para Control Bidireccional (como en las diapositivas)
    tabu_out = []  # Nodos que han salido -> Prohibido que vuelvan a entrar
    tabu_in = []   # Nodos que han entrado -> Prohibido que vuelvan a salir
    
    iter_no_improve = 0
    evolution_rows = [] if evolution_csv_path is not None else None
    iteration_number = 0

    while iter_no_improve < max_iter:
        if time.time() - start >= time_limit:
            break

        v_out, of_var_out, v_in, of_var_in = selectInterchange(sol, tabu_out, tabu_in, best_sol['of'])
        if v_out == -1:
            break

        previous_of = sol['of']
        solution.removeFromSolution(sol, v_out, of_var_out)
        solution.addToSolution(sol, v_in, of_var_in)
        iteration_number += 1
        
        # Actualizamos la memoria a corto plazo
        tabu_out.append(v_out)
        tabu_in.append(v_in)
        
        # Tenencia Dinámica para evitar ciclos deterministas
        current_tenure = random.randint(tabu_tenure, int(tabu_tenure * 1.5))
        
        # Ajustamos las listas FIFO al tamaño dinámico actual
        while len(tabu_out) > current_tenure:
            tabu_out.pop(0)
            tabu_in.pop(0)

        if sol['of'] > best_sol['of']:
            best_sol = copy.deepcopy(sol)
            iter_no_improve = 0
        else:
            iter_no_improve += 1

        if convergence_log is not None and sol['of'] > convergence_best:
            convergence_best = sol['of']
            convergence_log.append({
                "Algorithm": algorithm_name,
                "Elapsed_Time": round(time.time() - convergence_start_time, 6),
                "Best_Objective": round(convergence_best, 2),
            })

        if evolution_rows is not None:
            evolution_rows.append({
                "iteration_number": iteration_number,
                "current_solution_objective": round(sol['of'], 2),
                "global_best_objective": round(best_sol['of'], 2),
                "was_worsening_move": sol['of'] < previous_of,
            })

    sol['sol'] = best_sol['sol']
    sol['of'] = best_sol['of']
    sol['instance'] = best_sol['instance']

    if evolution_csv_path is not None:
        with open(evolution_csv_path, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "iteration_number",
                    "current_solution_objective",
                    "global_best_objective",
                    "was_worsening_move",
                ],
            )
            writer.writeheader()
            writer.writerows(evolution_rows)


def selectInterchange(sol, tabu_out, tabu_in, best_of):
    n = sol['instance']['n']
    best_delta = None
    best_v_out = -1
    best_v_in = -1
    best_of_var_out = 0
    best_of_var_in = 0

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

            # Control Bidireccional Legible:
            # - ¿El nodo que quiero meter acaba de salir?
            # - ¿El nodo que quiero sacar acaba de entrar?
            is_tabu = (v_in in tabu_out) or (v_out in tabu_in)

            if is_tabu:
                # Criterio de Aspiración
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

    if asp_delta is not None and (best_delta is None or asp_delta > best_delta):
        return asp_v_out, asp_of_var_out, asp_v_in, asp_of_var_in

    return best_v_out, best_of_var_out, best_v_in, best_of_var_in
