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
from scipy.interpolate import interp1d

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
    parameters_mc["Session"]["Photons"] = 1e8
    # parameters_mc["Domain"]["Media"][2]["mua"] = mu_a/1000
    # parameters_mc["Domain"]["Media"][2]["mus"] = mu_s/1000
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

def fem_run_params(rt,bioheat,tau_q,tau_T,mu_a,mu_s, results_type = "depth"): # TODO: ACTUALIZAR RESULTS
    parameters_fencisx = {
        "rt": rt,
        "bioheat_model": bioheat,
        "mu_a":  mu_a,
        "mu_s": mu_s,
        "tau_q": tau_q,
        "tau_T": tau_T
    }
    # if rt == "mc":
        # run_mcx(mu_a,mu_s)
    with open('fenicsx/parameters.json', 'w') as file:
        json.dump(parameters_fencisx, file, indent=4)
    run_simultation()
    
    # Run postprocessing
    if results_type ==  "regions":
        subprocess.run(["pvbatch", "pvpospro_average_Tf.py"])
    else:
        subprocess.run(["pvbatch", "pvpospro_transient.py"])
    results = pd.read_csv("postprocessing/data.csv")
    return results

def plot_result(result,label,color):
    plt.plot(result["arc_length"],result["f"],f"{color}",label=label)

def plot_result_transient(result,label,color):
    plt.plot(result["Time"],result["avg(f)"],f"{color}",label=label)

def get_relative_error(reference,result): #TODO: ACTUALIZAR
    def average(result):
        return (result["z0"]["f"] + result["z5"]["f"] + result["z25"]["f"])/3
    relative_error = (average(result) - average(reference))/average(reference)*100
    return np.mean(relative_error.to_numpy())


# Validacion
# mu_a = 12100
# mu_s = 1

# Test

def run_validation_case_dpl():
    mu_a = 31
    mu_s = 289 

    tau_q = 45
    tau_T = 25

    RESULTS_TYPE = "transient"

    result_mc = fem_run_params("mc","DPL",tau_q=0,tau_T=0,mu_a=mu_a,mu_s=mu_s,results_type=RESULTS_TYPE)
    result_mc_DPL = fem_run_params("mc","DPL",tau_q=tau_q,tau_T=tau_T,mu_a=mu_a,mu_s=mu_s,results_type=RESULTS_TYPE)
    lopes_mc = np.loadtxt("lopes_data/mc.csv",delimiter=",")
    lopes_experimental = np.loadtxt("lopes_data/experimental.csv",delimiter=",")
    # lopes_diffusion = np.loadtxt("lopes_data/diffusion.csv",delimiter=",")

    plt.figure()
    plt.plot(lopes_experimental[:,0],lopes_experimental[:,1], "k--",label="Lopes et. al: Experimental")
    # plt.plot(lopes_diffusion[:,0],lopes_diffusion[:,1], "b--",label="Lopes et. al: diffusion")
    plt.plot(lopes_mc[:,0],lopes_mc[:,1], "r--",label="Lopes et. al")
    plot_result_transient(result_mc,"FEniCSx Fourier","r")
    plot_result_transient(result_mc_DPL,"FEniCSx DPL","g")
    plt.legend()
    plt.savefig("postprocessing/plots/validation_dpl.png",dpi=500)
    plt.show()

    # res

# CASO DE VALIDACION
run_validation_case_dpl()
# run_concentration_study_case()


# mesh_convert()
# run_constant_properties(mu_a=3,mu_s=289)
# run_constant_properties(mu_a=2,mu_s=176)
# run_constant_properties(mu_a=0.1,mu_s=10000)
# run_variable_properties(mu_ext=300,list_relations=list(np.logspace(-2,2,num=10)))