import numpy as np
import random
from SN_input.constant import Constants
from SN_input.cost_func import CostFunc
from .util_func import fast_non_dominated_sort, write_to_file, find_bests


def generate_offspring(population, data, rank):
    size = Constants.size_population
    no_sensors = data.num_of_sensors
    q_population = np.zeros((size, no_sensors))
    # binary selection
    for i in range(size):
        if(i < 3):
            candicate_1 = random.randint(i+1, i+5)
            candicate_2 = random.randint(i+1, i+5)
        elif (i > size - 3):
            candicate_1 = random.randint(i-5, i-1)
            candicate_2 = random.randint(i-5, i-1)
        else:
            candicate_1 = random.randint(i-2, i+2)
            candicate_2 = random.randint(i-2, i+2)

        if rank[candicate_1] < rank[candicate_2]:
            q_population[i] = population[candicate_2]
        else:
            q_population[i] = population[candicate_1]
    # uniform cross over
    for i in range(int(size / 2)):
        for j in range(no_sensors):
            if(random.random() < Constants.cross_over):
                temp = q_population[i][j]
                q_population[i][j] = q_population[size-i-1][j]
                q_population[size-i-1][j] = temp
    # random mutate
    for i in range(size):
        for j in range(no_sensors):
            if(random.random() < Constants.mutation):
                q_population[i][j] = (q_population[i][j] + 1) % 2

    return q_population


def generate_lamda(size):
    lamda = np.zeros((size, 3))
    dis = round(1.0/(1.1*size), 3)
    for i in range(1, size+1):
        lamda[i-1][0] = round(abs(1 - dis * i), 2)
        lamda[i-1][1] = round(abs(1 - dis * (i + 1)), 2)
        lamda[i-1][2] = round(abs(1 - dis * (i + 2)), 2)
    return lamda


def run_moea_d(population, data, outfile):
    EP = []
    new_population = population
    size = len(population)
    lamda = generate_lamda(size)
    z = [0.5, 10, 50]
    loop = 2
    loop_num = 1
    cf = CostFunc(population, data, size)
    cost = cf.getCost()
    rank = fast_non_dominated_sort(cost)
    while loop_num < loop:
        off_spring = generate_offspring(population, data, rank)
        cf.setPopulation(off_spring)
        off_cost = cf.getCost()
        # off_rank = fast_non_dominated_sort(off_cost)
        for i in range(size):
            if(cost[i].coverage > z[0]):
                z[0] = cost[i].coverage
            if(cost[i].loss < z[1]):
                z[1] = cost[i].loss
            if(cost[i].squantity < z[2]):
                z[2] = cost[i].squantity
        for i in range(size):
            max_s = max(abs(lamda[i][0] * (cost[i].coverage - z[0])), abs(lamda[i][1] * (cost[i].loss - z[1])), abs(lamda[i][2] * (cost[i].squantity - z[2])))
            max_off = max(abs(lamda[i][0] * (off_cost[i].coverage - z[0])), abs(lamda[i][1] * (off_cost[i].loss - z[1])), abs(lamda[i][2] * (off_cost[i].squantity-z[2])))

            if (max_s < max_off):
                new_population[i] = off_spring[i]

        cf.setPopulation(new_population)
        cost = cf.getCost()
        rank = fast_non_dominated_sort(cost)
        p_best = find_bests(rank)
        # best = p_best[random.randint(0, len(p_best)-1)]
        
        loop_num += 1
        if len(EP) == 0:
            for i in p_best:
                EP.append(cost[i])
        
        else:
            for i in p_best:
                for c in EP:
                    if (cost[i][0] >= c[0] and cost[i][1] <= c[1] and cost[i][2] <= c[2] and cost[i][0] > c[0] or cost[i][1] < c[1] or cost[i][2] < c[2]):
                        EP.append(cost[i])
                        del(c)
    write_to_file(outfile, EP)
    