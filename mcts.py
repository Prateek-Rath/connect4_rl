import random
import time
import math
from copy import deepcopy
import numpy as np
from connect4env import connect_4
# mcts adapted to this current environment
import random
import time
import math
from copy import deepcopy


# hyper params
class GameMeta:
    PLAYERS = {'none': 0, 'one': 1, 'two': 2}
    OUTCOMES = {'none': 0, 'one': 1, 'two': 2, 'draw': 3}
    INF = float('inf')
    ROWS = 6
    COLS = 7


class MCTSMeta:
    EXPLORATION = math.sqrt(2)



class Node:
    def __init__(self, move, parent):
        self.move = move
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.children = {}
        self.outcome = GameMeta.PLAYERS['none']

    def add_children(self, children: dict) -> None:
        for child in children:
            self.children[child.move] = child

    def value(self, explore: float = MCTSMeta.EXPLORATION):
        if self.N == 0:
            return 0 if explore == 0 else GameMeta.INF
        else:
            return self.Q / self.N + explore * math.sqrt(math.log(self.parent.N) / self.N)


class MCTS:
    def __init__(self, state=connect_4()):
        self.root_state = deepcopy(state)
        self.root = Node(None, None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0

    def select_node(self) -> tuple:
        node = self.root
        state = deepcopy(self.root_state)
        player = None
        if np.count_nonzero(state.board_state == 0)%2 == 0:
            player = 'p1'
        else:
            player = 'p2'
        while len(node.children) != 0:
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_value]

            node = random.choice(max_nodes)
            state.make_move(node.move, player)

            if node.N == 0:
                return node, state

        if self.expand(node, state):
            node = random.choice(list(node.children.values()))
            state.make_move(node.move, player)

        return node, state

    def expand(self, parent: Node, state: connect_4) -> bool:
        state.check_game_done('p1')
        state.check_game_done('p2')
        if state.isDone:
            return False

        children = [Node(move, parent) for move in state.get_available_actions()]
        parent.add_children(children)

        return True

    def roll_out(self, state: connect_4) -> int:
        while not state.isDone:
            player = None
            if np.count_nonzero(self.root_state.board_state == 0)%2 == 0:
                player = 'p1'
            else:
                player = 'p2'
            state.make_move(random.choice(state.get_available_actions()), player)
            state.check_game_done('p1')
            state.check_game_done('p2')

        # return state.get_outcome()
        # return draw win or loss or nothing based on the situtation
        r1 = state.check_game_done('p1')
        r2 = state.check_game_done('p2')

        if r1 == state.reward['win']:
            return GameMeta.OUTCOMES['one']
        elif r2 == state.reward['win']:
            return GameMeta.OUTCOMES['two']
        elif r1 == state.reward['draw']:
            return GameMeta.OUTCOMES['draw']
        elif r2 == state.reward['draw']:
            return GameMeta.OUTCOMES['draw']
        else:
            return 0

    def back_propagate(self, node: Node, turn: int, outcome: int) -> None:

        # For the current player, not the next player
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            if outcome == GameMeta.OUTCOMES['draw']:
                reward = 0
            else:
                reward = 1 - reward

    def search(self, time_limit: int):
        start_time = time.process_time()

        num_rollouts = 0
        while time.process_time() - start_time < time_limit:
            node, state = self.select_node()
            outcome = self.roll_out(state)
            self.back_propagate(node, state.turn, outcome)
            num_rollouts += 1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

    def best_move(self):
        if self.root_state.isDone:
            return -1

        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        best_child = random.choice(max_nodes)

        return best_child.move

    def move(self, move):
        player = None
        if np.count_nonzero(self.root_state.board_state == 0)%2 == 0:
            player = 'p1'
        else:
            player = 'p2'
        if move in self.root.children:
            self.root_state.make_move(move, player)
            self.root = self.root.children[move]
            return

        self.root_state.make_move(move, player)
        self.root = Node(None, None)

    def statistics(self) -> tuple:
        return self.num_rollouts, self.run_time

