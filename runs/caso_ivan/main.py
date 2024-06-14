from fenicsx_args import run
import matplotlib.pyplot as plt

column = 10
sheet = 'Total conc. (gr.ml-1) -40 mV'

sol = run(column,sheet)

print(sol.shape)
