import sys
sys.path.append('../../')
from FEM.bridge.run_fenicsx import mesh_convert
from FEM.bridge.run_fenicsx import run_simultation
import json
import numpy as np
import os

def clean_results():
    if os.path.exists('coords_sol.npy'):
        os.remove('coords_sol.npy')


def run(column,sheet):
    clean_results()
    params = {
        "column": column,
        "sheet": sheet
    }
    with open('fenicsx/parameters.json', 'w') as file:
        json.dump(params, file)

    run_simultation()

    sol = np.load('coords_sol.npy')
    return sol
