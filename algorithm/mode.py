from .util_func import fast_non_dominated_sort, write_to_file, find_bests
from SN_input.constant import Constants
from SN_input.cost_func import CostFunc
import numpy as np
import random

def mode_reproduction(population, data, p_best):
    no_sensors = data.num_of_sensors
    size = len(population)
    pg = Constants.pg
    pm = Constants.pm
    pp = Constants.pp
    new_population = np.zeros((size, no_sensors))
    a = pg + pm
    b = pg + pm + pp
    for i in range(size):
        for j in range(no_sensors):
            rand = random.random()
            if rand <= pg:
                new_population[i][j] = population[i][j]
            elif rand > pg and rand <= a:
                r = random.randint(0, len(p_best)-1)
                new_population[i][j] = population[p_best[r]][j]
            elif rand > a and rand <= b:
                r = random.randint(0, size-1)
                new_population[i][j] = population[r][j]
            elif rand > b:
                r = -1
                while 1:
                    r = random.randint(0, size-1)
                    if r != i:
                        break
                new_population[i][j] = population[r][j]
    return new_population

def run_mode(population, data, outfile):
    size = len(population)
    num_ss = data.num_of_sensors
    new_population = np.zeros((size, num_ss))
    cf = CostFunc(population, data, size)
    cost = cf.getCost()

    rank = fast_non_dominated_sort(cost)
    p_best = find_bests(rank)
    best = p_best[random.randint(0, len(p_best)-1)]
    loop = Constants.loop
    i = 0
    result = []
    while i < 1:
        result = []
        new_population = mode_reproduction(population, data, p_best)
        cf.setPopulation(new_population)
        cost = cf.getCost()
        rank = fast_non_dominated_sort(cost)
        p_best = find_bests(rank)
        for i in p_best:
            result.append(cost[i])
        i = i + 1

    for i in range(len(p_best)):
        write_to_file(outfile, result)
    