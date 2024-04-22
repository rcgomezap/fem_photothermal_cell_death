import subprocess as su


def clean_results(): # Limpia los resultados
    su.run("rm -rf FEM/fenicsx/results/*", shell=True)

def run_simultation(): # Genera la malla y corre la simulación
    # clean_results()
    # su.run(f"docker run --rm -i -v $(pwd):/root dolfinx_v0.6.0:rc bash -c 'gmsh mesh/msh_lopes.geo -3 -nt 12 -cpu -o mesh/msh/tumor_geometry.msh' | tee log_gmsh.txt", shell=True)
    su.run(f"docker run --rm -i -v $(pwd):/root dolfinx_v0.6.0:rc bash -c 'python3 FEM/fenicsx/mesh/mesh_convert.py'", shell=True)
    su.run(f"docker run --rm -it -v $(pwd):/root dolfinx_v0.6.0:rc bash -c 'python3 FEM/fenicsx/main.py' | tee log_fenicsx.txt", shell=True)
# save_results(f"factor_{list_factor[i]}")

run_simultation()




