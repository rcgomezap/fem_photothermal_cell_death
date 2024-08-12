import ufl
from dolfinx import fem, io
from dolfinx.fem import Function, locate_dofs_topological, dirichletbc,Expression
from ufl import ds, dx, grad, inner, Measure

from mpi4py import MPI
from petsc4py.PETSc import ScalarType
from petsc4py import PETSc


def solve(V,msh,T,v,ds,dx,k,rho,c,w,Qmet,blood,Qs_func,h,bc,Ti,Tref,dt,tf,dir,coords,regions_bc,postprocess=True):
    print('Running Simulation...')
    x = ufl.SpatialCoordinate(msh)
    # Definicion de las ecuaciones
    T_old = Function(V)
    Qs=Function(V)
    # conv_bc = regions_bc['convection'][0]
    def get_forms():
        a = ((rho*c*T*v + dt*k*inner(grad(T), grad(v)))*x[0]*dx #laplaciano
            + dt*h*T*v*x[0]*ds #Condicion de convecccion natural
            + dt*T*blood.cp*blood.rho*w*v*x[0]*dx #Perfusion sanguinea
        )
        L = (rho*c*T_old*v*x[0]*dx
            + dt*inner(Qs, v)*x[0]*dx #Laser
            + dt*h*Tref*v*x[0]*ds #Condicion de convecccion natural
            + dt*blood.T*blood.cp*blood.rho*w*v*x[0]*dx#Perfusion sanguinea
            + dt*Qmet*v*x[0]*dx#Calor metabolico)
            )
        bilinear_form = fem.form(a)
        linear_form = fem.form(L)
        return bilinear_form,linear_form
    
    def create_systems(bilinear_form,linear_form):
        A = fem.petsc.assemble_matrix(bilinear_form, bcs=bc)
        A.assemble()
        b = fem.petsc.create_vector(linear_form)
        return A,b
    def get_solver(A):
        solver = PETSc.KSP().create(msh.comm)
        solver.setOperators(A)
        # solver.setType(PETSc.KSP.Type.PREONLY)  
        # solver.getPC().setType(PETSc.PC.Type.LU)
        solver.setType(PETSc.KSP.Type.BICG)
        solver.getPC().setType(PETSc.PC.Type.GAMG)
        return solver
    def transient_solver(b,bilinear_form,linear_form,bcs,solver,T_old,dt,tf,Qs):

        sol = []

        t = 0
        T_old.x.array[:] = Ti
        Tfem = fem.Function(V)
        Tfem.x.array[:] = Ti
        # Crear archivo XDMF y guardar condiciones iniciales
        xdmf = io.XDMFFile(msh.comm, f"{dir}/fenicsx/results/T.xdmf", "w")
        xdmf.write_mesh(msh)
        xdmf.write_function(T_old, t)

        num_steps = int(tf/dt) # numero de pasos de tiempo

        #create a txt file to store log
        for i in range(num_steps):
            # Avanzar en el tiempo
            # log = open(f"{dir}/fenicsx/log.txt", "a")
            # log.write(f"t = {t:.2f} / {tf:.2f} - Tmax = {Tfem.x.array.max()}\n")
            # log.close()
            sol.append((t,Tfem.copy()))
            t += dt

            # Ensamblar vector lineal
            Qs.interpolate(Expression(Qs_func(t), V.element.interpolation_points())) # Evaluar fuente de calor
            with b.localForm() as loc_b:
                loc_b.set(0)
            fem.petsc.assemble_vector(b, linear_form)

            # Aplicar condiciones de frontera
            fem.petsc.apply_lifting(b, [bilinear_form], [bcs])
            b.ghostUpdate(addv=PETSc.InsertMode.ADD_VALUES, mode=PETSc.ScatterMode.REVERSE)
            fem.petsc.set_bc(b, bcs)

            # Resolver sistema lineal
            solver.solve(b, Tfem.vector)
            # print(i)
            Tfem.x.scatter_forward()

            # Actualizar solucion anterior
            T_old.x.array[:] = Tfem.x.array

            # Guardar solucion en archivo XDMF
            if (i+1)*dt % 5 == 0:
                xdmf.write_function(Tfem, t)
                print(f"t = {t:.2f} / {tf:.2f}")
                print(f'Tmin = {Tfem.x.array.min()}')
                print(f'Tmax = {Tfem.x.array.max()}')
        return sol
    bilinear_form,linear_form = get_forms()
    A,b = create_systems(bilinear_form,linear_form)
    solver = get_solver(A)
    sol=transient_solver(b,bilinear_form,linear_form,bc,solver,T_old,dt,tf,Qs)

    return sol