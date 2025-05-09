from connect4env import connect_4
import numpy as np
from heuristic_player import HeuristicPlayer
from dqn import DQN
import torch

env = connect_4()
my_heur_player = HeuristicPlayer()


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
policy_net = DQN(7)

policy_net.load_state_dict(torch.load('./models/DQN_minimax_d2.pth', weights_only=True))

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
    state = env.get_board()
    b = int(input())
    # b = my_heur_player.heuristic_player_move(state, 2)
    env.make_move(b, 'p2')

    env.check_game_done('p2')

env.render()



# 0                     
# 1                     
# 2                     
# 3     X  X            
# 4     O  O  X         
# 5  X  O  O  O  X  