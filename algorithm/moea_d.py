import numpy as np
import random
from SN_input.constant import Constants
from SN_input import cost_func
from .util_func import *


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


def run_moea_d(population, data):
    EP = []
    new_population = population
    size = Constants.size_population
    lamda = generate_lamda(size)
    z = [0.5, 10, 50]
    best = 0
    loop = Constants.loop
    loop_num = 1
    while loop_num < loop:
        coverage_cost = cost_func.coverage(new_population, data, size)
        max_comm_loss = cost_func.max_comm_loss(new_population, data, size)
        no_sensors_placed = cost_func.no_placed_sensors(new_population, data, size)
        rank = fast_non_dominated_sort(coverage_cost, max_comm_loss, no_sensors_placed, size)
        
        off_spring = generate_offspring(population, data, rank)
        off_coverage_cost = cost_func.coverage(off_spring, data, size)
        off_max_comm_loss = cost_func.max_comm_loss(off_spring, data, size)
        off_no_sensors_placed = cost_func.no_placed_sensors(off_spring, data, size)
        off_rank = fast_non_dominated_sort(off_coverage_cost, off_max_comm_loss, off_no_sensors_placed, size)
        for i in range(size):
            if(coverage_cost[i] > z[0]):
                z[0] = coverage_cost[i]
            if(max_comm_loss[i] < z[1]):
                z[1] = max_comm_loss[i]
            if(no_sensors_placed[i] < z[2]):
                z[2] = no_sensors_placed[i]
        for i in range(size):
            max_s = max(abs(lamda[i][0] * (coverage_cost[i] - z[0])), abs(lamda[i][1] * (max_comm_loss[i] - z[1])), abs(lamda[i][2] * (no_sensors_placed[i]-z[2])))
            max_off = max(abs(lamda[i][0] * (off_coverage_cost[i] - z[0])), abs(lamda[i][1] * (off_max_comm_loss[i] - z[1])), abs(lamda[i][2] * (off_no_sensors_placed[i]-z[2])))

            if (max_s < max_off):
                new_population[i] = off_spring[i]

        coverage_cost = cost_func.coverage(new_population, data, size)
        max_comm_loss = cost_func.max_comm_loss(new_population, data, size)
        no_sensors_placed = cost_func.no_placed_sensors(new_population, data, size)
        rank = fast_non_dominated_sort(coverage_cost, max_comm_loss, no_sensors_placed, size)
        p_best = find_bests(rank)
        # best = p_best[random.randint(0, len(p_best)-1)]
        
        loop_num += 1
    for i in range(len(p_best)):
        write_to_file("output/moea_d/converge_no-dem1_r25_1.out", coverage_cost[p_best[i]], max_comm_loss[p_best[i]], no_sensors_placed[p_best[i]])
    