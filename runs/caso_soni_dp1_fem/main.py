# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 09:56:34 2024

@author: Roberto Gomez
"""
import numpy as np
import json
import subprocess
import os
import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append('../../')
from FEM.bridge.run_fenicsx import run_simultation,mesh_convert

# CONST
mcx_path = "/home/rc/AUR/MCXStudio/MCXSuite/mcx/bin/mcx"

def run_mcx(mu_a,mu_s):

    # load json file
    with open('mcx/mcx_base.json', 'r') as file:
        parameters_mc = json.load(file)

    # modify parameters
    parameters_mc["Session"]["Photons"] = 1e8
    parameters_mc["Domain"]["Media"][3]["mua"] = mu_a/1000
    parameters_mc["Domain"]["Media"][3]["mus"] = mu_s/1000
    # save json file
    with open('mcx/mcx.json', 'w') as file:
        json.dump(parameters_mc, file, indent=4)

    # run mcx
    os.chdir("mcx")
    process = subprocess.Popen([mcx_path, "-f", "mcx.json","-D","P","-F", "nii","|","tee"])
    process.wait()
    os.chdir("..")

def fem_run_params(rt,mu_a,mu_s):
    parameters_fencisx = {
        "rt": rt,
        "mu_a":  mu_a,
        "mu_s": mu_s
    }
    if rt == "mc":
        run_mcx(mu_a,mu_s)
    with open('fenicsx/parameters.json', 'w') as file:
        json.dump(parameters_fencisx, file, indent=4)
    run_simultation()
    
    # Run postprocessing
    subprocess.run(["pvbatch", "pvpospro.py"])
    results = {
        "z0": pd.read_csv("postprocessing/z0.csv"),
        "z5": pd.read_csv("postprocessing/z5.csv"),
        "z25": pd.read_csv("postprocessing/z25.csv"),
    }
    return results

def plot_result(result,label,color):
    plt.plot(result["z0"]["arc_length"],result["z0"]["f"],f"{color}-",label=label)
    plt.plot(result["z5"]["arc_length"],result["z5"]["f"],f"{color}--")
    plt.plot(result["z25"]["arc_length"],result["z25"]["f"],f"{color}-.")


# Validacion
# mu_a = 12100
# mu_s = 1

# Test
mu_a = 300
mu_s = 300

result_beer = fem_run_params("beer",mu_a,mu_s)
result_dp1 = fem_run_params("dp1",mu_a,mu_s)
result_mc = fem_run_params("mc",mu_a,mu_s)

plt.figure()
plot_result(result_beer,"Beer-Lambert","r")
plot_result(result_dp1,"Delta-P1","b")
plot_result(result_mc,"Monte Carlo","g")
plt.legend()
plt.savefig(f"result_mua{mu_a}_mus{mu_s}.png",dpi=500)
plt.show()