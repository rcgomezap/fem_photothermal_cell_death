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

def run_mcx(mu_a,mu_s): # TODO: ACTUALIZARLA

    # load json file
    with open('mcx/mcx_base.json', 'r') as file:
        parameters_mc = json.load(file)

    # modify parameters
    parameters_mc["Session"]["Photons"] = 1e7
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

def fem_run_params(rt,mu_a,mu_s): # TODO: ACTUALIZAR RESULTS
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
    # subprocess.run(["pvbatch", "pvpospro.py"])
    # results = {
    #     "z0": pd.read_csv("postprocessing/z0.csv"),
    #     "z5": pd.read_csv("postprocessing/z5.csv"),
    #     "z25": pd.read_csv("postprocessing/z25.csv"),
    # }
    results = {}
    return results

def plot_result(result,label,color): #TODO: ACTUALIZAR
    plt.plot(result["z0"]["arc_length"],result["z0"]["f"],f"{color}-",label=label)
    plt.plot(result["z5"]["arc_length"],result["z5"]["f"],f"{color}--")
    plt.plot(result["z25"]["arc_length"],result["z25"]["f"],f"{color}-.")

def get_relative_error(reference,result): #TODO: ACTUALIZAR
    def average(result):
        return (result["z0"]["f"] + result["z5"]["f"] + result["z25"]["f"])/3
    relative_error = (average(result) - average(reference))/average(reference)*100
    return np.mean(relative_error.to_numpy())


# Validacion
# mu_a = 12100
# mu_s = 1

# Test
def run_constant_properties(mu_a,mu_s):
    # result_dp1 = fem_run_params("dp1",mu_a,mu_s)
    # result_mc = fem_run_params("mc",mu_a,mu_s)
    result_sda = fem_run_params("sda",mu_a,mu_s)

    # plt.figure()
    # plot_result(result_beer,"Beer-Lambert","r")
    # plot_result(result_dp1,"Delta-P1","b")
    # plot_result(result_mc,"Monte Carlo","g")
    # plot_result(result_sda,"SDA","k")
    # plt.legend()
    # plt.savefig(f"result_mua{mu_a}_mus{mu_s}.png",dpi=500)
    # plt.show()

def run_variable_properties(mu_ext,list_relations): #TODO: ACTUALIZAR

    def plot_errors(errors,color,label):
        plt.plot(list_relations,errors,color,label=label)


    mu_a = [mu_ext/(1+i) for i in list_relations]
    mu_s = [mu_ext/(1+1/i) for i in list_relations]

    error = {"relations": list_relations,
             "beer": [],
             "dp1": [],
             "mc": [],
             "sda": [],
             }

    for mu_ai,mu_si in zip(mu_a,mu_s):
        beer_i = fem_run_params("beer",mu_ai,mu_si)
        sda_i = fem_run_params("sda",mu_ai,mu_si)
        mc_i = fem_run_params("mc",mu_ai,mu_si)
        dp1_i = fem_run_params("dp1",mu_ai,mu_si)

        error["beer"].append(get_relative_error(mc_i,beer_i))
        error["sda"].append(get_relative_error(mc_i,sda_i))
        error["dp1"].append(get_relative_error(mc_i,dp1_i))

    with open(f"error_ext_{mu_ext}.json","w") as file:
        json.dump(error,file,indent=6)

    plt.figure()
    plot_errors(error["beer"],'r-o',"beer")
    plot_errors(error["sda"],'g-o',"sda")
    plot_errors(error["dp1"],'b-o',"dp1")
    plt.xscale("log")
    plt.xlabel("mu_s / mu_a")
    plt.ylabel("Error relativo (%)")
    plt.legend()
    plt.savefig(f"errors_ext_{mu_ext}.png",dpi=500)
    plt.show()
    

# CASO DE VALIDACION
mesh_convert()
run_constant_properties(mu_a=31,mu_s=289)
# run_variable_properties(mu_ext=300,list_relations=list(np.logspace(-2,2,num=10)))