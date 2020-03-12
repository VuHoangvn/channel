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
    for i in range(1):
        print(f"[INFO] running round_{i}...")
        # nsga_ii_out = f'output/refactor/nsga_ii/{i}.out'
        # mode_out = f'output/refactor/mode/{i}.out'
        moead_out = f'output/refactor/moead/{i}.out'
        
        # print("[INFO] running nsga_ii...") 
        # run_nsga_ii(population, data, nsga_ii_out)
        # print("[INFO] running mode...")
        # run_mode(population, data, mode_out)
        print("[INFO] running moea_d...")
        run_moea_d(population, data, moead_out)

if __name__ == '__main__':
    run('SN_input/data/small_data/no-dem1_r25_1.in')
