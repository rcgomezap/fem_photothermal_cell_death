import subprocess as su
import os
root = os.path.dirname(os.path.realpath(__file__))[:-11]
dir = os.getcwd()
dir = os.path.relpath(dir, root)

def clean_results(dir): # Limpia los resultados
    su.run("rm -rf FEM/fenicsx/results/*", shell=True)

def run_simultation(): # Genera la malla y corre la simulación
    # su.run(f"docker run --rm -i -v $(pwd):/root dolfinx_v0.6.0:rc bash -c 'gmsh mesh/msh_lopes.geo -3 -nt 12 -cpu -o mesh/msh/tumor_geometry.msh' | tee log_gmsh.txt", shell=True)
    su.run(f"docker run --rm -i -v {root}:/root dolfinx_v0.6.0:rc bash -c 'python3 FEM/fenicsx/mesh/mesh_convert.py'", shell=True)
    su.run(f"docker run --rm -it -v {root}:/root dolfinx_v0.6.0:rc bash -c 'python3 {dir}/fenicsx/fenicsx_main.py {dir}' | tee log_fenicsx.txt", shell=True)

# run_simultation("runs/validacion_soni")
# print("Hello World")




