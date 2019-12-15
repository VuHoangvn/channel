import numpy as np
import random
from SN_input.constant import Constants
from SN_input import cost_func
from .util_func import *


def generate_offspring(population, data, rank):
    no_sensors = data.num_of_sensors
    size = Constants.size_population

    q_population = np.zeros((size, no_sensors))
    # binary selection
    for i in range(size):
        candicate_1 = random.randint(0, size - 1)
        candicate_2 = random.randint(0, size - 1)
        if rank[candicate_1] < rank[candicate_2]:
            q_population[i] = population[candicate_2]
        else:
            q_population[i] = population[candicate_1]
    # uniform cross over
    for i in range(int(size / 2)):
        for j in range(no_sensors):
            if(random.random() < Constants.cross_over):
                temp = q_population[i][j]
                q_population[i][j] = q_population[size-1][j]
                q_population[size-1][j] = temp
    # random mutate
    for i in range(size):
        for j in range(no_sensors):
            if(random.random() < Constants.mutation):
                q_population[i][j] = (q_population[i][j] + 1) % 2

    return q_population

def run_nsga_ii(population, data):
    size = Constants.size_population
    max_num = Constants.max_num
    num_ss = data.num_of_sensors
    new_population = population
    best = 0
    loop = Constants.loop
    num_loop = 0
    while num_loop < loop:
        # create population Q
        coverage_cost = cost_func.coverage(new_population, data, size)
        max_comm_loss = cost_func.max_comm_loss(new_population, data, size)
        no_sensors_placed = cost_func.no_placed_sensors(new_population, data, size)
        rank = fast_non_dominated_sort(coverage_cost, max_comm_loss, no_sensors_placed, size)
        q_population = generate_offspring(population, data, rank)

        # concatenate population
        total_population = np.concatenate((new_population, q_population))
        # calculate objective
        coverage_cost = cost_func.coverage(total_population, data, 2* size)
        max_comm_loss = cost_func.max_comm_loss(total_population, data, 2 * size)
        no_sensors_placed = cost_func.no_placed_sensors(total_population, data, 2 * size)
        rank = fast_non_dominated_sort(coverage_cost, max_comm_loss, no_sensors_placed, 2 * size)

        sort_min_sensors = []
        sort_max_communicate_loss = []
        sort_coverage_cost = []
        sort_rank = []
        for i in range(2 * size):
            sort_min_sensors.append((i, no_sensors_placed[i]))
            sort_max_communicate_loss.append((i, max_comm_loss[i]))
            sort_coverage_cost.append((i, coverage_cost[i]))
            sort_rank.append((i, rank[i]))
        sort_min_sensors.sort(key=sortSecond)
        sort_max_communicate_loss.sort(key=sortSecond)
        sort_coverage_cost.sort(key=sortSecond)
        sort_rank.sort(key=sortSecond)

        # calculate distance
        I = [0] * 2 * size
        I[sort_min_sensors[0][0]] = max_num
        I[sort_min_sensors[2*size-1][0]] = max_num
        I[sort_max_communicate_loss[0][0]] = max_num
        I[sort_max_communicate_loss[2*size-1][0]] = max_num
        I[sort_coverage_cost[0][0]] = max_num
        I[sort_coverage_cost[2*size-1][0]] = max_num

        normalize_k = sort_coverage_cost[2 * size-1][1]-sort_coverage_cost[0][1]
        normalize_max_comm_loss = sort_max_communicate_loss[2 * size-1][1]-sort_max_communicate_loss[0][0]
        normalize_min_sensors = sort_min_sensors[2 * size-1][1] - sort_min_sensors[0][1]
        for i in range(1, size - 1):
            I[sort_coverage_cost[i][0]] = I[sort_coverage_cost[i][0]] + (sort_coverage_cost[i+1][1] - sort_coverage_cost[i-1][1])/normalize_k
            I[sort_max_communicate_loss[i][0]] = I[sort_max_communicate_loss[i][0]] + (sort_max_communicate_loss[i+1][1] - sort_max_communicate_loss[i-1][1])/normalize_max_comm_loss
            I[sort_min_sensors[i][0]] = I[sort_min_sensors[i][0]] + (sort_min_sensors[i+1][1]-sort_min_sensors[i-1][1])/normalize_min_sensors

        sort_to_produce = []

        new_population = []
        for r in range(1, rank[2*size]+1):
            temp = []
            for i in range(2*size):
                if(sort_rank[i][1] == r):
                    temp.append((sort_rank[i][0], sort_rank[i][1], I[i]))
            temp.sort(key=sortThird, reverse=True)
            sort_to_produce = sort_to_produce + temp
        # print(len(sort_to_produce))
        for i in range(size):
            new_population.append(total_population[sort_to_produce[i][0]])

        # population = new_population
        best = sort_to_produce[0][0]
        
        num_loop = num_loop + 1
    write_to_file("output/nsga_ii/converge_no-dem1_r25_1.out", coverage_cost[best], max_comm_loss[best], no_sensors_placed[best])