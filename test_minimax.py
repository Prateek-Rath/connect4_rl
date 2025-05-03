import numpy as np
from minimax import MiniMaxPlayer

# test minimax

my_minimax_player = MiniMaxPlayer()

x = np.array([
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,2,0,1,0,0,0],
    [0,1,0,1,2,0,2]
])


#    0  1  2  3  4  5  6
# 0                     
# 1                     
# 2                     
# 3           O         
# 4     X     O         
# 5     O     O  X     X
y = x.copy()

# print(x.shape)
_, a = my_minimax_player.minimax(x, 3, 2, 2)
# print([s for ])
x = np.array([
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,2,0,1,0,0,0],
    [2,1,0,1,2,0,2]
])
s = my_minimax_player.evaluate(x, 2)
print(s)


x = np.array([
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,2,0,1,0,0,0],
    [0,2,0,1,0,0,0],
    [0,1,0,1,2,0,2]
])
s = my_minimax_player.evaluate(x, 2)
print(s)

x = np.array([
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,2,0,1,0,0,0],
    [0,1,2,1,2,0,2]
])
s = my_minimax_player.evaluate(x, 2)
print(s)

x = np.array([
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,2,0,0,0],
    [0,0,0,1,0,0,0],
    [0,2,0,1,0,0,0],
    [0,1,0,1,2,0,2]
])
s = my_minimax_player.evaluate(x, 2)
print(s)

# print(my_minimax_player.score_position())
print(a)