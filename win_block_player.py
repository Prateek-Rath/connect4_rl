# our model needs to learn not to miss wins and it must also learn to block when someone else is about to win
# shape rewards such that this objective is taken care of

# we can use the heuristic player to see if the opponent has a win or not and accordingly reward our foolish agent
import numpy as np
from copy import deepcopy
import random


class WinBlockPlayer():
    def __init__(self):
        self.board_width = 7
        self.board_height = 6
        pass

    def take_action(self, board, action, player):
        for r in range(self.board_height-1, -1, -1):
            if board[r][action] == 0:
                board[r][action] = player
                return board

    def undo_action(self, board, action, player):
        for r in range(0, self.board_height, 1):
            if board[r][action] == player:
                board[r][action] = 0
                return board

    def get_valid_moves(self, board):
        # returns the list of valid moves
        valid = []
        for c in range(0, self.board_width):
            if board[0][c] == 0:
                valid.append(c)
        return valid

    def check_game_done(self, board, player):
        # returns true if the game is over and player won
        if player == 1:
            check = '1 1 1 1'
        else:
            check = '2 2 2 2'

        # check vertically then horizontally
        for j in range(self.board_width):
            if check in np.array_str(board[:, j]):
                return True
        for i in range(self.board_height):
            if check in np.array_str(board[i, :]):
                return True

        # check left diagonal and right diagonal
        for k in range(0, self.board_height - 4 + 1):
            left_diagonal = np.array([board[k + d, d] for d in \
                            range(min(self.board_height - k, min(self.board_height, self.board_width)))])
            right_diagonal = np.array([board[d + k, self.board_width - d - 1] for d in \
                            range(min(self.board_height - k, min(self.board_height, self.board_width)))])
            if check in np.array_str(left_diagonal) or check in np.array_str(right_diagonal):
                return True
        for k in range(1, self.board_width - 4 + 1):
            left_diagonal = np.array([board[d, d + k] for d in \
                            range(min(self.board_width - k, min(self.board_height, self.board_width)))])
            right_diagonal = np.array([board[d, self.board_width - 1 - k - d] for d in \
                            range(min(self.board_width - k, min(self.board_height, self.board_width)))])
            if check in np.array_str(left_diagonal) or check in np.array_str(right_diagonal):
                return True
        return False

    def     check_win(self, board, player, action):
        # if doing action on board makes player win then return True
        # else return False
        temp_board = deepcopy(board)
        temp_board = self.take_action(temp_board, action, player)
        flag = self.check_game_done(temp_board, player)
        temp_board = self.undo_action(temp_board, action , player)
        return flag

    def get_bad_moves(self, board, player):
        # if opponent wins immidiately after your move, you suck
        opponent = 1 + (player%2)
        bad_moves = []
        for a in self.get_valid_moves(board):
            tempboard = deepcopy(board)
            self.take_action(tempboard, a, player)
            flag = False
            for b in self.get_valid_moves(tempboard):
                if self.check_win(tempboard, opponent, b):
                    flag = True
                    break
            self.undo_action(tempboard, a, player)
            if flag:
                bad_moves.append(a)
        return bad_moves

    def wb_player_move(self, board, player):
        opponent  = 1 + (player%2)
        # if we have a win, win
        # if they have a win, block
        # otherwise random

        winning_action_for_me = None

        tempboard = deepcopy(board)
        for a in self.get_valid_moves(tempboard):
            if self.check_win(tempboard, player, a):
                winning_action_for_me = a
                break
        if winning_action_for_me is not None:
            return a


        winning_action_for_them  = None
        for a in self.get_valid_moves(tempboard):
            if self.check_win(tempboard, opponent, a):
                winning_action_for_them = a
                break
        if winning_action_for_them is not None:
            return a
        

        a = random.choice(self.get_valid_moves(tempboard))
        return a
    
if __name__ == "__main__":
    x  = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 0, 0],
        ]
        
    )

    print(x)

    wb_player = WinBlockPlayer()
    a = wb_player.wb_player_move(x, 2)


    print('a is', a)