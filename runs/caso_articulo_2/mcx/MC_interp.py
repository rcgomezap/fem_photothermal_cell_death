import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator

def MC_interp(list_cells,dir):
    # carga de la imagen
    img = nib.load(f"{dir}/mcx/base/caso_Gnyawali.nii")
    list_cells = list_cells[:2,:]
    print(f"list cells size: {len(list_cells[0])}")
    print(f"xmax: {np.max(list_cells[0])}")
    # img = nib.load('caso_Lopes.nii')
    imgdata = img.get_fdata()
    print(imgdata.shape)
    slice = imgdata[299,:,:,0]*1000**2 #slice 300 (centro)

    L = 60
    H = 30
    dx = 0.1 #mm #voxel size

    plt.imshow(slice.T, cmap='hot')
    plt.show()

    X = np.arange(dx,len(slice[:,0])*dx+dx,dx)
    Y = np.arange(dx,len(slice[0,:])*dx+dx,dx)

    # X = np.linspace(dx/2, L-dx/2, len(slice[:,0]))
    # Y = np.linspace(dx/2, H-dx/2, len(slice[0,:]))

    # X = np.arange(0,len(slice[:,0]))*dx+dx/2
    # Y = np.arange(0,len(slice[0,:]))*dx+dx/2
    # # print(Y.max())
    # X -= L-dx
    X -= L/2

    #plot xx,yy, slice 3D plot
    # fig, ax = plt.subplots(1, 1)
    # ax = fig.add_subplot(111, projection='3d')
    XX, YY = np.meshgrid(X, Y, indexing='ij')
    plt.pcolormesh(XX,YY, slice, cmap='turbo')
    plt.xlim(-30,30)
    plt.colorbar()
    plt.show()

    interp = RegularGridInterpolator((X, Y), slice,
                                    bounds_error=False, fill_value=None, method='linear') 
    
    # dofs_coords[:,1] = dofs_coords[:,1].max() - dofs_coords[:,1] #invertir eje y
    interpolated = interp(list_cells.T*1000) #m -> mm
    # interpolated = interp(dofs_coords) #m -> mm

    # return interpolated*1000**2 # 1/mm2 -> 1/m2
    return interpolated

# print(MC_interp(np.array([2.899999999999999800e-02*1000,-4.768551618023827842e-20])))

if __name__ == "__main__":
    print(MC_interp(np.array([[-21,29],[21,29]])))

    L = 30*1e-3
    N=100
    x1 = np.linspace(-L,0,N)
    x2 = np.linspace(0,L,N)
    y = 20*1e-3*np.ones(N)

    xd1 = np.flip(MC_interp(np.array([x1,y]).T))
    xd2 = MC_interp(np.array([x2,y]).T)


    plt.plot(x1+L,xd1, label='Left')
    plt.plot(x2,xd2, label='Right')
    plt.title('Symmetric test')
    plt.legend()
    plt.show()