from structure import instance, solution
from algorithms import grasp_timed, grasp_ts
import random


def executeInstance():
    path = "instances/MDG-a_2_n500_m50.txt"
    inst = instance.readInstance(path)

    random.seed(1)

    print("\n--- GRASP (alpha=0.1, time_limit=5s) ---")
    sol_grasp = grasp_timed.execute(
        inst,
        alpha=0.1,
        time_limit=5,
    )
    solution.printSolution(sol_grasp)

    print("\n--- GRASP+TS (alpha=0.9, tenure=10, time_limit=5s) ---")
    sol_ts = grasp_ts.execute(
        inst,
        alpha=0.9,
        time_limit=5,
        tabu_tenure=10,
        max_iter=5000,
    )
    solution.printSolution(sol_ts)


if __name__ == '__main__':
    executeInstance()
