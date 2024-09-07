from dolfinx.fem import Function
from scipy.interpolate import LinearNDInterpolator
from scipy.integrate import solve_ivp
import numpy as np
def get_max_y(coords, boundary_dofs,V):
    MaxY = Function(V)
    boundary_dofs_coords = coords[boundary_dofs]
    x = boundary_dofs_coords[:,0]
    y = boundary_dofs_coords[:,1]
    z = boundary_dofs_coords[:,2]
    interp = LinearNDInterpolator(list(zip(x, z)), y, fill_value=0)
    MaxY.x.array[:] = interp(coords[:,0],coords[:,2])
    return MaxY

def get_fluence_rate_gaussian(power,radius,r):
    return 2*power/(np.pi*radius**2)*np.exp(-2*r**2/radius**2)


def get_fluence_rate_flat(power,radius,r):

    A = np.pi*radius**2
    fr_c = power/A
    if r < radius-1e-5:
        return fr_c
    return 0


def collimated(V,coords,MaxY,mu_a,mu_s,g,power,laser_radius,laser_type):
    print('Calculating Collimated Radiation')
    phic = Function(V)

    mut_ast = Function(V)
    mus_ast = Function(V)

    print('Calculating Optical Properties for Collimated Radiation')
    mus_ast.x.array[:] = mu_s.x.array[:]*(1-g.x.array[:]**2)
    mut_ast.x.array[:] = mu_a.x.array[:]+mus_ast.x.array[:]

    print('Interpolating Optical Properties for Collimated Radiation')
    interp_mut_ast = LinearNDInterpolator(list(zip(coords[:,0],coords[:,1])), mut_ast.x.array[:], fill_value=0)

    def filter_laser_dofs(coords,radius):
        print('Filtering laser dofs')
        laser_dofs = []
        for i in range(len(coords)):
            if coords[i,0]**2+coords[i,2]**2 < radius**2:
                laser_dofs.append(i)
        return laser_dofs


    def dphicdy(x,y,maxy,phi):
        y_global = maxy - y
        return -interp_mut_ast(x,y_global)*phi
    
    def calculate_phic(x):
        num_quadratures = len(x[0,:])
        print(f'Starting loop for collimated radiation calculation with {num_quadratures} quadratures')
        phic_ = np.zeros(len(x[0,:]))
        for i in range(num_quadratures):
            xi,zi = x[0,i],x[2,i]
            yf = MaxY - x[1,i]

            f = lambda y,phi: dphicdy(xi,y,MaxY,phi)
            if laser_type == "flat":
                fluence_rate = get_fluence_rate_flat(power,laser_radius,np.sqrt(xi**2+zi**2))
            else:
                fluence_rate = get_fluence_rate_gaussian(power,laser_radius,np.sqrt(x**2+zi**2))

            if yf != 0:
                sol = solve_ivp(f, [0, yf], [fluence_rate], method='RK45',t_eval=[yf])
                phic_[i] = sol.y[0,0]
            else:
                phic_[i] = fluence_rate
            if i%1000 == 0:
                print(f'Calculating Collimated Radiation: {i*100/num_quadratures} %')
        # phic.x.array[:]*=fluence_rate
        return phic_


    phic = Function(V)
    phic.interpolate(calculate_phic)
    return phic
