from structure import instance, solution
from algorithms import grasp
import random


def executeInstance():
    path = "instances/MDG-a_2_n500_m50.txt"
    inst = instance.readInstance(path)

    for tenure in [5, 10, 15, 20]:
        random.seed(1)
        print(f"\n--- tabu_tenure={tenure} ---")
        sol, iters = grasp.execute(
            inst,
            alpha       = -1,
            tabu_tenure = tenure,
            max_iter    = 500,
            iters       = 10,
        )
        print(f"Completed {iters} GRASP iterations")
        print("BEST SOLUTION:")
        solution.printSolution(sol)


if __name__ == '__main__':
    executeInstance()