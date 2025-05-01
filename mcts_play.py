# mcts demo
from mcts import MCTS
from connect4env import connect_4

mcts = MCTS()


def demo():
    state = connect_4()
    print('do you want to play first')
    x = input()
    mcts = MCTS(state)
    player = None
    if x == 'y':
        player = 'p1'
        pass
    else:
        mcts.search(30)
        num_rollouts, run_time = mcts.statistics()
        print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
        move = mcts.best_move()
        player = 'p2'
        print("MCTS chose move: ", move)

        state.make_move(move, player)
        mcts.move(move)

    
    while not state.isDone:
        print("Current state:")
        state.render()

        user_move = int(input("Enter a move: "))
        while user_move not in state.get_available_actions():
            print("Illegal move")
            user_move = int(input("Enter a move: "))
        print('user_move is', user_move)
        state.make_move(user_move, player)
        mcts.move(user_move)

        state.render()
        state.check_game_done('p1')
        state.check_game_done('p2')
        if state.isDone:
            print("Player one won!")
            break

        print("Thinking...")

        mcts.search(8)
        num_rollouts, run_time = mcts.statistics()
        print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
        move = mcts.best_move()

        print("MCTS chose move: ", move)

        state.make_move(move, 'p2' if player == 'p1' else 'p1')
        mcts.move(move)

        state.render()
        state.check_game_done('p1')
        state.check_game_done('p2')
        if state.isDone:
            print("Player two won!")
            break


demo()
