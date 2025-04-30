import numpy as np
from minimax import MiniMaxPlayer

# test minimax

my_minimax_player = MiniMaxPlayer()

x = np.array([
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,2,2,2,0],
    [0,0,0,1,1,1,2]
])
print(x.shape)
my_minimax_player.minimax(x, 2, 1, 1)