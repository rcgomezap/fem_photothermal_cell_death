import subprocess as su
import os
dir1 = os.path.dirname(os.path.realpath(__file__))[:-11]


def clean_results(dir): # Limpia los resultados
    su.run("rm -rf FEM/fenicsx/results/*", shell=True)

def run_simultation(dir): # Genera la malla y corre la simulación
    dir = os.path.relpath(dir, dir1)
    # print(dir)
    # clean_results()
    # su.run(f"docker run --rm -i -v $(pwd):/root dolfinx_v0.6.0:rc bash -c 'gmsh mesh/msh_lopes.geo -3 -nt 12 -cpu -o mesh/msh/tumor_geometry.msh' | tee log_gmsh.txt", shell=True)
    su.run(f"docker run --rm -i -v {dir1}:/root dolfinx_v0.6.0:rc bash -c 'python3 FEM/fenicsx/mesh/mesh_convert.py'", shell=True)
    su.run(f"docker run --rm -it -v {dir1}:/root dolfinx_v0.6.0:rc bash -c 'python3 {dir}/fenicsx/fenicsx_main.py {dir}' | tee log_fenicsx.txt", shell=True)
# save_results(f"factor_{list_factor[i]}")

# run_simultation("runs/validacion_soni")
# print("Hello World")




