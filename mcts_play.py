# mcts demo
from mcts import MCTS
from connect4env import connect_4
import random

mcts = MCTS()
search_time = 8

mcts.search(search_time)


wins = 0
losses = 0
def demo():
    state = connect_4()
    # print('do you want to play first')
    # x = input()
    x = 'n'
    mcts = MCTS(state)
    player = None
    player = 'p1'
    mcts.search(search_time)
    num_rollouts, run_time = mcts.statistics()
    print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
    move = mcts.best_move()

    print("MCTS chose move: ", move)

    state.make_move(move, 'p1' if player == 'p2' else 'p2')
    mcts.move(move)

    state.render()
    
    while not state.isDone:
        print("Current state:")
        state.render()

        # user_move = int(input("Enter a move: "))
        # while user_move not in state.get_available_actions():
        #     print("Illegal move")
        #     user_move = int(input("Enter a move: "))
        # print('user_move is', user_move)
        user_move  = random.choice(state.get_available_actions())
        state.make_move(user_move, player)
        mcts.move(user_move)

        state.render()
        if state.isDone:
            print("Player one won!")
            break

        print("Thinking...")

        mcts.search(search_time)
        num_rollouts, run_time = mcts.statistics()
        print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
        move = mcts.best_move()

        print("MCTS chose move: ", move)

        state.make_move(move, 'p1' if player == 'p2' else 'p2')
        mcts.move(move)

        state.render()
        if state.isDone:
            print("Player two won!")
            break


demo()
