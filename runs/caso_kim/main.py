from fenicsx_args import run

regionProperties = {
    'epidermis': {'k': 0.59, 'rho': 1000, 'c': 4200, 'w': 0, 'Qmet': 0, 'mu_a': 1, 'mu_s':1, 'g':0.9, 'kf_bar': 1, 'kb': 1, 'Tk': 1},
    'p-dermis': {'k': 0.59, 'rho': 1000, 'c': 4200, 'w': 0, 'Qmet': 0, 'mu_a': 1, 'mu_s':1, 'g':0.9, 'kf_bar': 1, 'kb': 1, 'Tk': 1},
    'r-dermis': {'k': 0.59, 'rho': 1000, 'c': 4200, 'w': 0, 'Qmet': 0, 'mu_a': 1, 'mu_s':1, 'g':0.9, 'kf_bar': 1, 'kb': 1, 'Tk': 1},
    'fat': {'k': 0.59, 'rho': 1000, 'c': 4200, 'w': 0, 'Qmet': 0, 'mu_a': 1, 'mu_s':1, 'g':0.9, 'kf_bar': 1, 'kb': 1, 'Tk': 1},
    'tumorNP': {'k': 0.59, 'rho': 1000, 'c': 4200, 'w': 0, 'Qmet': 0, 'mu_a': 1000, 'mu_s':1, 'g':0.9, 'kf_bar': 1, 'kb': 1, 'Tk': 1},
}

bloodProperties = {
    'T': 37,
    'rho': 1000,
    'c': 4200
}

numericalParameters = {
    'dt': 1,
    'tf': 1000,
    'tau_q': 0,
    'tau_T': 0
}

initialConditions = {
    'T': 0
}

boundaryParameters = {
    'ambientTemperature': 0,
    'h': 5
}

laserProperties = {
    'type': 'gaussian', # OR 'flat'
    'power': 1, #W
    'radius': 4e-3, # radius if flat, else waist
    'irradiationTime': 500 #s
}


fenicsxParams = {
    'regionProperties': regionProperties,
    'bloodProperties': bloodProperties,
    'laserProperties': laserProperties,
    'initialConditions': initialConditions,
    'boundaryParameters': boundaryParameters,
    'numericalParameters': numericalParameters,
}

sol = run(fenicsxParams)