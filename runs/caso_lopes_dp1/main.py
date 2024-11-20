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
    parameters_mc["Session"]["Photons"] = 1e7
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

def fem_run_params(rt,mu_a,mu_s, results_type = "depth"): # TODO: ACTUALIZAR RESULTS
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
def run_constant_properties(mu_a,mu_s):
    # result_dp1 = fem_run_params("dp1",mu_a,mu_s)
    # result_mc = fem_run_params("mc",mu_a,mu_s,results_type="transient")
    result_sda = fem_run_params("sda",mu_a,mu_s,results_type="regions")

    plt.figure()
    # plot_result(result_beer,"Beer-Lambert","r")
    # plot_result(result_dp1,"Delta-P1","b")
    # plot_result_transient(result_mc,"Monte Carlo","g")
    # plot_result_transient(result_sda,"SDA","k")
    plt.legend()
    # plt.savefig(f"result_mua{mu_a}_mus{mu_s}.png",dpi=500)
    plt.show()

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

def run_validation_case():
    mu_a = 31
    mu_s = 289 

    RESULTS_TYPE = "transient"

    result_mc = fem_run_params("mc",mu_a,mu_s,results_type=RESULTS_TYPE)
    result_dp1 = fem_run_params("dp1",mu_a,mu_s,results_type=RESULTS_TYPE)
    result_sda = fem_run_params("sda",mu_a,mu_s,results_type=RESULTS_TYPE)
    lopes_mc = np.loadtxt("lopes_data/mc.csv",delimiter=",")
    lopes_experimental = np.loadtxt("lopes_data/experimental.csv",delimiter=",")
    lopes_diffusion = np.loadtxt("lopes_data/diffusion.csv",delimiter=",")

    plt.figure()
    plt.plot(lopes_experimental[:,0],lopes_experimental[:,1], "k--",label="Lopes et. al: Experimental")
    plt.plot(lopes_diffusion[:,0],lopes_diffusion[:,1], "b--",label="Lopes et. al: SDA")
    plt.plot(lopes_mc[:,0],lopes_mc[:,1], "r--",label="Lopes et. al: MC")
    plot_result_transient(result_mc,"MC","r")
    plot_result_transient(result_sda,"SDA","b")
    plot_result_transient(result_dp1,r"$\delta P1$","g")
    plt.legend()
    plt.savefig("postprocessing/plots/validation.png",dpi=500)
    plt.show()

    # res

def run_concentration_study_case():

    RESULTS_TYPE = "regions"

    def plot_errors(error_dict,filename):
        plt.figure()
        plt.plot(concentrations*100,error_dict["gnp_region"]["dp1"], "g-o",label=r"$\delta P1$")
        plt.plot(concentrations*100,error_dict["gnp_region"]["sda"], "b-o",label="SDA")
        plt.plot(concentrations*100,error_dict["agar_region"]["dp1"], "g-v")
        plt.plot(concentrations*100,error_dict["agar_region"]["sda"], "b-v")
        plt.xlabel("Concentration of GNPs (%)")
        plt.ylabel("Relative Error (%)")
        plt.legend()
        plt.savefig(f"postprocessing/plots/{filename}.png",dpi=500)
        plt.show()
    
    def get_errors(reference,result):
        return (result.iloc[0] - reference.iloc[0])/reference.iloc[0]*100

    agar = {"mu_s": 176.,
            "mu_a": 2.}
    gnp = {"mu_s": 289.,
            "mu_a": 31.}
    
    concentrations = np.linspace(0,2,21)
    mu_s_interpolator = interp1d([0,1],[agar["mu_s"],gnp["mu_s"]],fill_value="extrapolate") # type: ignore
    mu_a_interpolator = interp1d([0,1],[agar["mu_a"],gnp["mu_a"]],fill_value="extrapolate") # type: ignore
    mu_a_values = mu_a_interpolator(concentrations)
    mu_s_values = mu_s_interpolator(concentrations)
    print(concentrations)

    errors = {"agar_region": 
              {"dp1": [],
               "sda": []},
               "gnp_region": 
               {"dp1": [],
                "sda": []}}
    
    log = open("log_concentration.txt","w")
    log.close()

    for i in range(len(concentrations)):
        result_mc = fem_run_params("mc",mu_a_values[i],mu_s_values[i],results_type=RESULTS_TYPE)
        result_dp1 = fem_run_params("dp1",mu_a_values[i],mu_s_values[i],results_type=RESULTS_TYPE)
        result_sda = fem_run_params("sda",mu_a_values[i],mu_s_values[i],results_type=RESULTS_TYPE)
        
        errors["agar_region"]["dp1"].append(get_errors(result_mc["average_agar"],result_dp1["average_agar"]))
        errors["agar_region"]["sda"].append(get_errors(result_mc["average_agar"],result_sda["average_agar"]))

        errors["gnp_region"]["dp1"].append(get_errors(result_mc["average_gnp"],result_dp1["average_gnp"]))
        errors["gnp_region"]["sda"].append(get_errors(result_mc["average_gnp"],result_sda["average_gnp"]))
        
        log = open("log_concentration.txt","a")
        log.write(f"{(i+1)/len(concentrations)*100} %\n")
        log.close()

    # log.close()
    
    with open("postprocessing/error_concentrations.json","w") as file:
        json.dump(errors,file,indent=6)

    plot_errors(errors,"regions_error")

# CASO DE VALIDACION
# run_validation_case()
run_concentration_study_case()


# mesh_convert()
# run_constant_properties(mu_a=3,mu_s=289)
# run_constant_properties(mu_a=2,mu_s=176)
# run_constant_properties(mu_a=0.1,mu_s=10000)
# run_variable_properties(mu_ext=300,list_relations=list(np.logspace(-2,2,num=10)))