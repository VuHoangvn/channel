import numpy as np
import math
from .constant import Constants
from .point import distance
from collections import namedtuple

Cost = namedtuple('Cost', ['coverage', 'loss', 'squantity'])

class CostFunc:
    def __init__(self, population, data, size):
        self.population = population
        self.data = data
        self.size = len(population)

    def setPopulation(self, population):
        self.population = population
        self.size = len(population)

    def calc_coverage(self):
        m = self.data.num_of_relays
        k = Constants.k_coverage
        elem_cover = np.zeros((self.size, m))
        ss_cover = self.data.sensor_coverage
        for s in range(self.size):
            for i in range(m):
                for j in range(self.data.num_of_sensors):
                    if self.population[s][j] == 1 and ss_cover[i][j] == 1:
                        elem_cover[s][i] += 1

        sum_ss_cover = [0] * self.size
        for s in range(self.size):
            for i in range(m):
                if(elem_cover[s][i] >= k):
                    sum_ss_cover[s] += 1.0/m
                else:
                    sum_ss_cover[s] += float(elem_cover[s][i]) / (k*m)
        
        return sum_ss_cover

    def calc_max_comm_loss(self):
        no_sensors = self.data.num_of_sensors
        max = [-99999] * self.size
        loss_matrix = self.data.comm_loss_matrix
        for s in range(self.size):
            for i in range(no_sensors):
                for j in range(i+1, no_sensors):
                    if self.population[s][i] == 1 and self.population[s][j] == 1 and loss_matrix[i][j] > max[s]:
                        max[s] = loss_matrix[i][j]

        return max


    def calc_no_placed_sensors(self):
        no_sensors = [99999] * self.size
        for s in range(self.size):
            no_sensors[s] = np.count_nonzero(self.population[s] == 1.0)

        return no_sensors        

    def getCost(self):
        coverage = self.calc_coverage()
        loss = self.calc_max_comm_loss()
        squantity = self.calc_no_placed_sensors()

        return [Cost(c, l, s) for c, l, s in zip(coverage, loss, squantity)]
