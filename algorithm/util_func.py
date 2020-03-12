import numpy as np
from SN_input.constant import Constants
from SN_input import cost_func

MAX_NUM = 1e6

def fast_non_dominated_sort(cost):
    size = len(cost)
    Sp = np.empty(size, dtype=np.object)
    F = np.empty(size + 1, dtype=np.object)
    for i in range(size):
        Sp[i] = []
        F[i] = []
    Np = [0] * size
    rank = [0] * (size+1)

    for i in range(size):
        for j in range(i+1, size):
            if(cost[i].coverage > cost[j].coverage and cost[i].loss < cost[j].loss) and cost[i].squantity < cost[j].squantity:
                Sp[i].append(j)
            else:
                if(cost[i].coverage <= cost[j].coverage and cost[i].loss >= cost[j].loss) and cost[i].squantity >= cost[j].squantity:
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
    rank[size] = i
    return rank

def crowding_distance_assignment(cost, size):
    l = len(cost)
    I = [0] * l
    coverage_sort = sorted(range(l), key=lambda k: cost[k][0])
    loss_sort = sorted(range(l), key=lambda k: cost[k][1])
    squantity_sort = sorted(range(l), key=lambda k: cost[k][2])

    I[coverage_sort[0]] = MAX_NUM    
    I[coverage_sort[-1]] = MAX_NUM
    I[loss_sort[0]] = MAX_NUM    
    I[loss_sort[-1]] = MAX_NUM
    I[squantity_sort[0]] = MAX_NUM
    I[squantity_sort[-1]] = MAX_NUM

    normalize_coverage = cost[coverage_sort[-1]][0] - cost[coverage_sort[0]][0]
    normalize_loss = cost[loss_sort[-1]][1] - cost[loss_sort[0]][1]
    normalize_squantity = cost[squantity_sort[-1]][2] - cost[squantity_sort[0]][2]

    for i in range(1, l-1):
        I[coverage_sort[i]] += (cost[coverage_sort[i+1]][0] - cost[coverage_sort[i-1]][0]) / normalize_coverage
        I[loss_sort[i]] += (cost[loss_sort[i+1]][1] - cost[loss_sort[i-1]][1]) / normalize_loss
        I[squantity_sort[i]] += (cost[squantity_sort[i+1]][2] - cost[squantity_sort[i-1]][2]) / normalize_squantity
    
    dist_sort = sorted(range(l), key=lambda k: I[k])
    extend_index = []
    for k in dist_sort:
        extend_index.append(k)
    
    return extend_index



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

def write_to_file(filename, cost):
    f = open(filename, "w")
    for i in range(len(cost)):
        f.write("{}     {}      {}\n".format(cost[i].coverage, cost[i].loss, cost[i].squantity))
    f.close()

