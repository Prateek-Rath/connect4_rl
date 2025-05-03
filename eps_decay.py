import matplotlib.pyplot as plt
import numpy as np
# epilson decay graph
EPS_START = 0.93
EPS_END = 0.05
EPS_DECAY = 700

steps_done = np.arange(5000)
eps = EPS_END + (EPS_START - EPS_END) * np.exp(-1 * steps_done / EPS_DECAY) # at the end, there is near 0 exploration

if __name__ == "__main__":
    plt.plot(steps_done, eps)
    plt.title('Epsilon decay graph')
    plt.xlabel('Episode no.')
    plt.ylabel('Epsilon')
    plt.show()
    plt.close()