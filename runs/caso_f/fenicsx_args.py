import sys
sys.path.append('../../')
from FEM.bridge.run_fenicsx import mesh_convert
from FEM.bridge.run_fenicsx import run_simultation
import json
import numpy as np
import os

def clean_results():
    if os.path.exists('T_sol.npy'):
        os.remove('T_sol.npy')

def run(params):

    with open('fenicsx/parameters.json', 'w') as file:
        json.dump(params, file, indent=4)

    run_simultation()
    sol = np.load('T_sol.npy')
    clean_results()
    return sol


if __name__ == '__main__':
    mesh_convert()
