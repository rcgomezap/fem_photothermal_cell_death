from fenicsx_args import run
import matplotlib.pyplot as plt
import numpy as np

column = 10
sheet = 'Total conc. (gr.ml-1) 40 mV'

dt = 10

sol = run(column,sheet)
np.save(f"caso0.npy",sol)
# plt.plot(sol[0,2:])
# plt.show()
# print(sol.shape)
