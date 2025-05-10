import argparse
import torch
import numpy as np
import random
import math

from connect4env import connect_4
from dqn import DQN
from eps_decay import EPS_START, EPS_END, EPS_DECAY
from minimax import MiniMaxPlayer
from heuristic_player import HeuristicPlayer
from win_block_player import WinBlockPlayer

# Argument parser
parser = argparse.ArgumentParser(description="Evaluate DQN agent against different opponents.")
parser.add_argument("--opponent", type=str, choices=["random", "wb", "minimax1", "heuristic"], required=True,
                    help="Choose opponent: random, wb, minimax, or heuristic")



parser.add_argument("--episodes", type=int, default=1, help="Number of evaluation episodes")
args = parser.parse_args()


if args.opponent == "random":
    model_path = "./models/DQN_random_kaggle.pth"
elif args.opponent == "wb":
    model_path = "./models/DQN_wb_kaggle0.3.pth"
elif args.opponent == "minimax1":
    model_path = "./models/DQN_wb_kaggle0.3.pth"
elif args.opponent == "heuristic":
    model_path = "./models/DQN_heuristic.pth"
else:
    model_path = "./models/DQN_wb_kaggle0.3.pth"
# Setup
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
policy_net = DQN(7).to(device)
policy_net.load_state_dict(torch.load(model_path, map_location=device))

# Instantiate environment and players
env = connect_4()
my_minimax_player = MiniMaxPlayer()
my_heur_player = HeuristicPlayer()
my_wb_player = WinBlockPlayer()

# Action selection function
def select_action(state, available_actions, steps_done=None, training=False, net=policy_net):
    state = torch.tensor(state, dtype=torch.float, device=device).unsqueeze(dim=0).unsqueeze(dim=0)
    epsilon = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1 * steps_done / EPS_DECAY) if training else 0
    if epsilon > eps_threshold:
        with torch.no_grad():
            r_actions = net(state)[0, :]
            state_action_values = [r_actions[action] for action in available_actions]
            return available_actions[np.argmax(state_action_values)]
    else:
        return random.choice(available_actions)

# Main evaluation loop
wins = 0
losses = 0
for _ in range(args.episodes):
    env.reset()
    while not env.isDone:
        state = env.get_board()
        a1 = select_action(state, env.get_available_actions(), 0, training=False)
        _, reward_p1 = env.make_move(a1, 'p1')
        if env.isDone:
            if reward_p1 == env.reward['win']:
                wins += 1
            else:
                losses += 1
            env.render()
            break
        env.render()
        state = env.get_board()
        if args.opponent == "random":
            a2 = random.choice(env.get_available_actions())
        elif args.opponent == "wb":
            a2 = my_wb_player.wb_player_move(state, 2)
        elif args.opponent == "minimax":
            _, a2 = my_minimax_player.minimax(state, 1, 2, 2)
        elif args.opponent == "heuristic":
            a2 = my_heur_player.heuristic_player_move(state, 2)

        _, reward_p2 = env.make_move(a2, 'p2')
        if env.isDone:
            losses += 1
            env.render()
            break
        env.render()
# Report
print(f"Win rate against {args.opponent} opponent: {wins / (wins + losses):.2f}")
