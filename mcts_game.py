from ConnectState import ConnectState
from mcts import MCTS


def play():
    state = ConnectState()
    print('do you want to play first')
    x = input()
    mcts = MCTS(state)

    if x == 'y':
        pass
    else:
        mcts.search(100)
        num_rollouts, run_time = mcts.statistics()
        print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
        move = mcts.best_move()

        print("MCTS chose move: ", move)

        state.move(move)
        mcts.move(move)

    
    while not state.game_over():
        print("Current state:")
        state.print()

        user_move = int(input("Enter a move: "))
        while user_move not in state.get_legal_moves():
            print("Illegal move")
            user_move = int(input("Enter a move: "))

        state.move(user_move)
        mcts.move(user_move)

        state.print()

        if state.game_over():
            print("Player one won!")
            break

        print("Thinking...")

        mcts.search(8)
        num_rollouts, run_time = mcts.statistics()
        print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
        move = mcts.best_move()

        print("MCTS chose move: ", move)

        state.move(move)
        mcts.move(move)

        if state.game_over():
            print("Player two won!")
            break


play()
