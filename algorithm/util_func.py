import numpy as np
from SN_input.constant import Constants
from SN_input import cost_func

def fast_non_dominated_sort(coverage_cost, max_comm_loss, no_placed_sensors, size):
    Sp = np.empty(size, dtype=np.object)
    F = np.empty(size + 1, dtype=np.object)
    for i in range(size):
        Sp[i] = []
        F[i] = []
    Np = [0] * size
    rank = [0] * (size+1)

    for i in range(size):
        for j in range(i+1, size):
            if(coverage_cost[i] > coverage_cost[j] and max_comm_loss[i] < max_comm_loss[j]) and no_placed_sensors[i] < no_placed_sensors[j]:
                Sp[i].append(j)
            else:
                if(coverage_cost[i] <= coverage_cost[j] and max_comm_loss[i] >= max_comm_loss[j]) and no_placed_sensors[i] >= no_placed_sensors[j]:
                    Sp[j].append(i)
                    Np[i] += 1
    for i in range(size):
        if Np[i] == 0:
            rank[i] = 1
            F[1].append(i)

    i = 1
    while F[i] != None and F[i] != []:
        Q = []
        for x in F[i]:
            for z in Sp[x]:
                Np[z] -= 1
                if Np[z] == 0:
                    rank[z] = i+1
                    Q.append(z)
        i += 1
        F[i] = Q
    rank[size] = i-1
    return rank


def find_bests(rank):
    size = Constants.size_population
    p_best = []
    for i in range(size):
        if rank[i] == 1:
            p_best.append(i)
    return p_best

def sortSecond(val):
    return val[1]


def sortThird(val):
    return val[2]

def write_to_file(filename, coverage_cost, max_comm_loss, no_placed_sensors):
    f = open(filename, "a")
    f.write("{}     {}      {}\n".format(coverage_cost, max_comm_loss, no_placed_sensors))
    f.close()