from connect4env import connect_4
import numpy as np
from heuristic_player import HeuristicPlayer

env = connect_4()
my_heur_player = HeuristicPlayer()

while not env.isDone:
    env.render()
    state = env.get_board()
    a = my_heur_player.heuristic_player_move(state, 1)
    env.make_move(a, 'p1')

    env.check_game_done('p1')
    if env.isDone:
        break

    env.render()
    b = int(input())
    env.make_move(b, 'p2')

    env.check_game_done('p2')



# 0                     
# 1                     
# 2                     
# 3     X  X            
# 4     O  O  X         
# 5  X  O  O  O  X  