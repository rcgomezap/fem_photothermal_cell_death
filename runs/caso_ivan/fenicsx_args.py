import sys
sys.path.append('../../')
from FEM.bridge.run_fenicsx import mesh_convert
from FEM.bridge.run_fenicsx import run_simultation
import json
import numpy as np

def run(column,sheet):
    params = {
        "column": column,
        "sheet": sheet
    }
    with open('fenicsx/parameters.json', 'w') as file:
        json.dump(params, file)

    run_simultation()

    sol = np.load('T_prom.npy')
    return sol
