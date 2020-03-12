import numpy as np
import random
from SN_input.constant import Constants
from SN_input.cost_func import CostFunc
from .util_func import fast_non_dominated_sort, write_to_file, crowding_distance_assignment


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

def run_nsga_ii(population, data, outfile):
    size = Constants.size_population
    max_num = Constants.max_num
    num_ss = data.num_of_sensors
    new_population = population
    cf = CostFunc(population, data, size)
    cost = []
    best = 0
    loop = Constants.loop
    num_loop = 0
    while num_loop < 1:
        # create population Q
        population = new_population
        cf.setPopulation(population)
        cost = cf.getCost()
        rank = fast_non_dominated_sort(cost)

        q_population = generate_offspring(population, data, rank)

        # # concatenate population
        total_population = np.concatenate((new_population, q_population))
        # # calculate objective
        cf.setPopulation(total_population)
        total_cost = cf.getCost()
        total_rank = fast_non_dominated_sort(total_cost)
        current_num = 0     # current number of individuals in new population
        new_population = []
        result = []
        # print(total_rank)
        # print(total_rank[-1])
        for i in range(1, total_rank[-1]):
            new_individual = []
            new_element_cost = []
            if current_num == size:
                break

            new_element = list(filter(lambda elem: elem[1] == i, enumerate(total_rank)))
            for elem in new_element:
                new_individual.append(total_population[elem[0]])
                new_element_cost.append(total_cost[elem[0]])

            if total_rank.count(i) + current_num <= size:
                new_population.extend(new_individual)
                if i == 1:
                    result = new_element_cost
            else:    
                extend_index = crowding_distance_assignment(new_element_cost, size-current_num)
                for i in extend_index:
                    new_population.append(new_individual[i])
                if i == 1:
                    for i in extend_index:
                        result.append(new_element_cost[i])

                break
        
        num_loop = num_loop + 1
        
    write_to_file(outfile, result)