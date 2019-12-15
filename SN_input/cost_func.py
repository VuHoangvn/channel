import numpy as np
import math
from .constant import Constants
from .point import distance


def coverage(population, data, size):
    m = data.num_of_relays
    k = Constants.k_coverage
    elem_cover = np.zeros((size, m))
    ss_cover = data.sensor_coverage
    for s in range(size):
        for i in range(m):
            for j in range(data.num_of_sensors):
                if population[s][j] == 1 and ss_cover[i][j] == 1:
                    elem_cover[s][i] += 1

    sum_ss_cover = [0] * size
    for s in range(size):
        for i in range(m):
            if(elem_cover[s][i] >= k):
                sum_ss_cover[s] += 1.0/m
            else:
                sum_ss_cover[s] += float(elem_cover[s][i]) / (k*m)
    return sum_ss_cover


def max_comm_loss(population, data, size):
    no_sensors = data.num_of_sensors
    max = [-99999] * size
    loss_matrix = data.comm_loss_matrix
    for s in range(size):
        for i in range(no_sensors):
            for j in range(i+1, no_sensors):
                if population[s][i] == 1 and population[s][j] == 1 and loss_matrix[i][j] > max[s]:
                    max[s] = loss_matrix[i][j]

    return max


def no_placed_sensors(population, data, size):
    no_sensors = [99999] * size
    for s in range(size):
        no_sensors[s] = np.count_nonzero(population[s] == 1.0)
    return no_sensors