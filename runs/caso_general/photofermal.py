#!/usr/bin/python3
from FEM.bridge.run_fenicsx import mesh_convert
from FEM.bridge.run_fenicsx import run_simultation
# import json
import sys
# import numpy as np
# import os
args = sys.argv


if __name__ == '__main__':
    
#     # run_simultation()
#     ruta_script = os.path.realpath(__file__)
# # Obtén el directorio en el que se encuentra el script
#     directorio_script = os.path.dirname(ruta_script)
#     directorio_actual = os.getcwd()
#     root = os.path.dirname(os.path.realpath(__file__))[:-17]
#     print(root)
#     mesh_convert(root, directorio_script)


#     print("Ruta absoluta del script:", ruta_script)
#     print("Directorio del script:", directorio_script)
#     print("Directorio actual:", directorio_actual

    if len(args) < 2:
        print('Argumento no válido')
        sys.exit(1)


    if args[1] == 'mesh_convert':
        mesh_convert()
    elif args[1] == 'run':
        run_simultation()
    else:
        print('Argumento no válido')
        sys.exit(1)
    
