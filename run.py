import sys

from SN_input.sn_input import Input
from SN_input.population import get_population
from SN_input import cost_func
from algorithm.util_func import *
from algorithm.mode import *
from algorithm.nsga_ii import *
from algorithm.moea_d import *


def run(data_file):
    data = Input.from_file(data_file)
    population = get_population(data)
    # for i in range(30):
    run_mode(population, data)
    run_nsga_ii(population, data)
    run_moea_d(population, data)

if __name__ == '__main__':
    run('SN_input/data/small_data/no-dem1_r25_1.in')
