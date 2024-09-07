import json



regions_bc = {
        # 'dirichlet': [],
        'convection_1': [5],
        'convection_2': [6],
        }

parmeters = {"k": 0.5,
             "rho": 1000,
             "c": 4186,
             "w": 0,
             "alpha": 50,
             "mu_s": 0,
             "Qmet": 0,
             "g": 0.9,
             "tf": 900,
             "regions_bc": regions_bc,
             "T_dirichlet": 37,
             "blood_T": 37,
             "blood_rho": 1090,
             "blood_cp": 4200,
             "I0": 1e4,
             "sigma": 0.00062505,
             "ymax": 7.8e-3, #m
             "h": 0,
             "t_irradiation": 900,
             "dt": 1,
             "Ti": 37,
             "Tref": 0
             }

with open('fenicsx/parameters.json', 'w') as file:
    json.dump(parmeters, file)