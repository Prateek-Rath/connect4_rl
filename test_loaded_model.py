from connect4env import connect_4
import torch
import numpy as np
from dqn import DQN
import os
import random
from eps_decay import EPS_START, EPS_END, EPS_DECAY
import math
from minimax import MiniMaxPlayer
from heuristic_player import HeuristicPlayer
from win_block_player import WinBlockPlayer


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

policy_net = DQN(7).to(device)
policy_net.load_state_dict(torch.load('./models/DQN_minimaxd1_kaggle.pth', weights_only=True))


policy_net = DQN(7).to(device)
policy_net.load_state_dict(torch.load('./models/DQN_wb_kaggle0.3.pth', weights_only=True, map_location=device))

policy_net.load_state_dict(torch.load('./models/DQN_wb_home.pth', weights_only=True, map_location=device))



# policy_net.load_state_dict(torch.load('./models/DQN_wb_kaggle5000.pth', weights_only=True, map_location=device))

x = np.array(
    [[0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 2, 0, 0],
    [0, 0, 1, 1, 1, 2, 0],
    ]
)

my_minimax_player = MiniMaxPlayer() 
my_heur_player = HeuristicPlayer()
my_wb_player = WinBlockPlayer()


def select_action(state, available_actions, steps_done=None, training=True, net=policy_net):
    # batch and color channel
    state = torch.tensor(state, dtype=torch.float, device=device).unsqueeze(dim=0).unsqueeze(dim=0)
    epsilon = random.random()
    if training:
        eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1 * steps_done / EPS_DECAY)
    else:
        eps_threshold = 0
    
    # follow epsilon-greedy policy
    if epsilon > eps_threshold:
        with torch.no_grad():
            # action recommendations from policy net
            r_actions = net(state)[0, :]
            state_action_values = [r_actions[action] for action in available_actions]
            argmax_action = np.argmax(state_action_values)
            greedy_action = available_actions[argmax_action]
            # print('q values are')
            # print(state_action_values)
            # print('so we choose', greedy_action)
            return greedy_action
    else:
        print('random choice?')
        return random.choice(available_actions)

env = connect_4()
env.reset()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


num_episodes = 100
wins=0
losses = 0

for episode in range(num_episodes):
    env.reset()
    while not env.isDone:
        
        # print('agent moved')
        state = env.get_board()
        with torch.no_grad():
            a1 = select_action(state, env.get_available_actions(), 0, False)
            # a1 = random.choice(env.get_available_actions())
        state_p1_, reward_p1 = env.make_move(a1, 'p1')
        # env.render()

        # env.check_game_done('p1')
        if env.isDone and reward_p1 == env.reward['win']:
            wins += 1
            break

        # print('player moved')
        
        state = env.get_board()
        # a2 = random.choice(env.get_available_actions())
        # a2= my_heur_player.heuristic_player_move(state, 2)
        # _, a2 = my_minimax_player.minimax(state, 1, 2, 2)
        a2 = my_wb_player.wb_player_move(state, 2)
        # a2 = int(input())
        # a2 = random.choice(env.get_available_actions())
        # print('a2 is', a2)
        # input()
        state_p2_, reward_p2 = env.make_move(a2, 'p2')
        # env.render()

        # env.check_game_done('p2')

        if env.isDone:
            losses += 1

        state_p1 = state_p2_

print('win rate is', wins/(wins+losses))