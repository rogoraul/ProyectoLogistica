import random
from algorithms import grasp_timed, grasp_ts
from structure import instance, solution


def executeInstance():
    path = "instances/MDG-a_2_n500_m50.txt"
    inst = instance.readInstance(path)
    sol = grasp_timed.execute(inst, 0.1, 5)
    print("\nGRASP:")
    solution.printSolution(sol)
    sol = grasp_ts.execute(inst, 0.9, 5, 10, 5000)
    print("\nGRASP+TS:")
    solution.printSolution(sol)


if __name__ == '__main__':
    random.seed(1)
    executeInstance()
