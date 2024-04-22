import numpy as np
def write_max_temperature(T):
    np.savetxt('results/postprocessing/max_temperature.txt', [T.x.array.max()])

def write_max_temperature_position(T, coords):
    arg = np.argmax(T.x.array)
    np.savetxt('results/postprocessing/max_temperature_position.txt', [np.array(coords[arg])])