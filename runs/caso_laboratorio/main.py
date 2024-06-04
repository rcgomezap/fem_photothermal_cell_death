from fenicsx_args import run
import matplotlib.pyplot as plt

sol = run(alpha=150)

plt.plot(sol[:,0], sol[:,1], label='T')
plt.show()

