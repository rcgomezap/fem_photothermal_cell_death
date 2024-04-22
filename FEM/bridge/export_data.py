import numpy as np
def export_T(T):
    T = T.x.array
    np.save("FEM/bridge/data/T", T)
