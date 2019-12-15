import numpy as np
import random
from SN_input.constant import Constants
from SN_input import cost_func
from .util_func import *

def mode_reproduction(population, data, p_best):
    no_sensors = data.num_of_sensors
    size = Constants.size_population
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

def run_mode(population, data):
    size = Constants.size_population
    num_ss = data.num_of_sensors
    new_population = np.zeros((size, num_ss))
    coverage_cost = cost_func.coverage(population, data, size)
    max_comm_loss = cost_func.max_comm_loss(population, data, size)
    no_sensors_placed = cost_func.no_placed_sensors(population, data, size)
    rank = fast_non_dominated_sort(coverage_cost, max_comm_loss, no_sensors_placed, size)
    p_best = find_bests(rank)
    best = p_best[random.randint(0, len(p_best)-1)]
    loop = Constants.loop
    i = 0
    while i < loop:
        new_population = mode_reproduction(population, data, p_best)
        coverage_cost = cost_func.coverage(population, data, size)
        max_comm_loss = cost_func.max_comm_loss(new_population, data, size)
        no_sensors_placed = cost_func.no_placed_sensors(new_population, data, size)
        rank = fast_non_dominated_sort(coverage_cost, max_comm_loss, no_sensors_placed, size)
        p_best = find_bests(rank)
        best = p_best[random.randint(0, len(p_best)-1)]
        i = i + 1
        # write_to_file("output/mode/converge_no-dem1_r25_1.out", coverage_cost[best], max_comm_loss[best], no_sensors_placed[best])    
    for i in range(len(p_best)):
        write_to_file("output/mode/converge_no-dem1_r25_1.out", coverage_cost[p_best[i]], max_comm_loss[p_best[i]], no_sensors_placed[p_best[i]])
    