from fenicsx_args import run
import matplotlib.pyplot as plt

sol = run(alpha=100)

plt.plot(sol[:,0], sol[:,1], label='T')
plt.show()
print(sol[:,1].max())

