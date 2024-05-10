import numpy as np
def export_T(T,dir):
    T = T.x.array
    np.save(f"{dir}/T", T)
