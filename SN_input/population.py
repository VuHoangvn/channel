from SN_input.sn_input import Input
from SN_input.constant import Constants
import numpy as np
import random


# class Initialize:
#     def __init__(self, data_file, size):
#         self.data = Input.from_file(data_file)
#         # num of sensors will be initially set
#         self.Y = int(self.data.num_of_sensors * 0.75)
#         # num of coverage
#         self.k = 3
#         self.size = size

def get_population(data):
    size = Constants.size_population
    num_ss = data.num_of_sensors
    Y = int(num_ss * Constants.set_sensor_rate)
    population = np.zeros((size, num_ss))
    for sn in range(size):
        i = Y
        while i > 0:
            rd = random.randint(0, num_ss-1)
            if population[sn][rd] == 0:
                population[sn][rd] = 1
                i -= 1
    return population