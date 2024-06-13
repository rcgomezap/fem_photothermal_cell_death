import sys
sys.path.append('../../')
from FEM.bridge.run_fenicsx import mesh_convert
from FEM.bridge.run_fenicsx import run_simultation
import json
import numpy as np

def run(conc,tf):

    alpha = 9.40260 + 0.1799 * conc
    params = {
        "alpha": alpha,
        "tf": tf
    }
    with open('fenicsx/parameters.json', 'w') as file:
        json.dump(params, file)

    run_simultation()

    sol = np.load('T_prom.npy')
    return sol
