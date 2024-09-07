import numpy as np
import matplotlib.pyplot as plt

tau = [0,5,10,20,50,100]



# data0 = np.loadtxt("res_tau/tau0.csv",skiprows=1,delimiter=",")

for i in tau:
    data = np.loadtxt(f"res_tau/tau{i}.csv",skiprows=1,delimiter=",")
    plt.plot(data[:,0],data[:,1], label=f'tau = {i}')
plt.legend()
plt.title("Efecto del lag")
plt.xlabel("Tiempo")
plt.ylabel("Temperatura")
plt.savefig("tau.png", dpi=500)