from fenicsx_args import run
import matplotlib.pyplot as plt

column = 10
sheet = 'Total conc. (gr.ml-1) -40 mV'

dt = 10

sol = run(column,sheet)
plt.plot(sol[0,2:])
plt.show()
print(sol.shape)
