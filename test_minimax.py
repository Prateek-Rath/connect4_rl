import numpy as np
from minimax import MiniMaxPlayer

# test minimax

my_minimax_player = MiniMaxPlayer()

x = np.array([
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,1,1,0,0]
])

y = x.copy()

# print(x.shape)
_, a = my_minimax_player.minimax(x, 2, 2, 2)

# print(my_minimax_player.score_position())
print(a)