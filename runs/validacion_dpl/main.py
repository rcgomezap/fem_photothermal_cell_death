from fenicsx_args import run
import matplotlib.pyplot as plt

sol = run(conc=300,tf=1800)
# plt.plot(sol[:,0], sol[:,1], label='T')
# plt.show()

