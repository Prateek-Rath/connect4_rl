import numpy as np
from copy import deepcopy
import random

class HeuristicPlayer():
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
    
    def check_win(self, board, player, action):
        # if doing action on board makes player win then return True
        # else return False
        temp_board = deepcopy(board)
        temp_board = self.take_action(temp_board, action, player)
        flag = self.check_game_done(temp_board, player)
        temp_board = self.undo_action(temp_board, action , player)
        return flag
    
    def form_double_trick(self, board, player, action):
        # if doing the action forms a double trick, return true o/w false

        #do the action
        temp_board = deepcopy(board)
        temp_board = self.take_action(temp_board, action, player)

        # now check if there are two different wins
        count = 0
        for a in self.get_valid_moves(temp_board):
            if self.check_win(temp_board, player, a):
                count += 1
        if count >= 2:
            return True
        else:
            return False
        
    def open3count(self, board, player, action):
        # return the number of open3s formed when player does action on board
        tempboard = deepcopy(board)
        tempboard = self.take_action(tempboard, action, player)
        bidirections = [[(0,1), (0,-1)], [(-1, 1), (1, -1)], [(-1,-1), (1,1)], [(-1,0), (1, 0)]]
        for i in range(0, self.board_height):
            if tempboard[i][action] == player:
                r = i
                break
        
        # so now at (r, action the move has been done)
        open3 = 0
        
        for bidirection in bidirections:
            # print('bidirection is', bidirection)
            count = 1
            # there are two ends per bidirection
            ends  = []
            for idx, direction in enumerate(bidirection):
                # print('direction is', direction)
                x,y = r,action
                x,y = x+direction[0],y+direction[1]
                while x < self.board_height and x >=0 and y < self.board_width and y >= 0:
                    # print('checking', x, y)
                    # print('it contains', tempboard[x][y])
                    if tempboard[x][y] == player:
                        count += 1
                    else:
                        if tempboard[x][y] == 0:
                            ends.append((x,y))
                        break
                    x,y = x+direction[0],y+direction[1]
                if count == 3:
                    open3 += len(ends)
            # print('count is', count)

        tempboard = self.undo_action(tempboard, action, player)
        return open3
    
    def open2count(self, board, player, action):
        # return the number of open2s formed when player does action on board
        tempboard = deepcopy(board)
        tempboard = self.take_action(tempboard, action, player)
        bidirections = [[(0,1), (0,-1)], [(-1, 1), (1, -1)], [(-1,-1), (1,1)], [(-1,0), (1, 0)]]
        for i in range(0, self.board_height):
            if tempboard[i][action] == player:
                r = i
                break
        
        # so now at (r, action the move has been done)
        open2 = 0
        
        for bidirection in bidirections:
            # print('bidirection is', bidirection)
            count = 1
            # there are two ends per bidirection
            ends  = []
            for idx, direction in enumerate(bidirection):
                # print('direction is', direction)
                x,y = r,action
                x,y = x+direction[0],y+direction[1]
                while x < self.board_height and x >=0 and y < self.board_width and y >= 0:
                    # print('checking', x, y)
                    # print('it contains', tempboard[x][y])
                    if tempboard[x][y] == player:
                        count += 1
                    else:
                        if tempboard[x][y] == 0:
                            ends.append((x,y))
                        break
                    x,y = x+direction[0],y+direction[1]
                if count == 2:
                    open2 += len(ends)
            # print('count is', count)

        tempboard = self.undo_action(tempboard, action, player)
        return open2
    
    def open1count(self, board, player, action):
        # return the number of open1s formed when player does action on board
        tempboard = deepcopy(board)
        tempboard = self.take_action(tempboard, action, player)
        bidirections = [[(0,1), (0,-1)], [(-1, 1), (1, -1)], [(-1,-1), (1,1)], [(-1,0), (1, 0)]]
        for i in range(0, self.board_height):
            if tempboard[i][action] == player:
                r = i
                break
        
        # so now at (r, action the move has been done)
        open1 = 0
        
        for bidirection in bidirections:
            print('bidirection is', bidirection)
            count = 1
            # there are two ends per bidirection
            ends  = []
            for idx, direction in enumerate(bidirection):
                # print('direction is', direction)
                x,y = r,action
                x,y = x+direction[0],y+direction[1]
                while x < self.board_height and x >=0 and y < self.board_width and y >= 0:
                    # print('checking', x, y)
                    # print('it contains', tempboard[x][y])
                    if tempboard[x][y] == player:
                        count += 1
                    else:
                        if tempboard[x][y] == 0:
                            ends.append((x,y))
                        break
                    x,y = x+direction[0],y+direction[1]
                if count == 1:
                    open1 += len(ends)
            # print('count is', count)

        tempboard = self.undo_action(tempboard, action, player)
        return open1

    def heuristic_player_move(self, board, player):
        """Heuristic player move logic."""
        opponent = 1 + (player%2)

        # if np.count_nonzero(board == 0) == 42:
        #     return 3 # the centre to start with

        # check if you yourself have a win
        for a in self.get_valid_moves(board):
            if self.check_win(board, player, a):
                print('doing winning action')
                return a

        # block opponent's open wins
        for a in self.get_valid_moves(board):
            if self.check_win(board, opponent, a):
                print('doing blocking action')
                return a
         
        bad_moves = []
        
        # try to form double trick for yourself
        
        for a in self.get_valid_moves(board):
            if self.form_double_trick(board, player, a):
                print('doing x2 action')
                return a

        # try to form multiple open 3s for yourself
        
        most3s_action = None
        most3s = 0
        for a in self.get_valid_moves(board):
            # we need the number of open 3s it forms
            if self.open3count(board, player, a) > most3s:
                most3s_action = a
                most3s = self.open3count(board, player, a)
        if most3s_action is not None:
            print('doing 3s action')
            return most3s_action
        
        
        # try to form multiple open 2s for yourself
        
        most2s_action = None
        most2s = 0
        for a in self.get_valid_moves(board):
            # we need the number of open 3s it forms
            if self.open2count(board, player, a) > most2s:
                most2s_action = a
                most2s = self.open2count(board, player, a)
        if most2s_action is not None:
            print('doing 2s action')
            return most2s_action
        
        # try to form open 1s for yourself
        # this means choose central cells on move 1...
        
        most1s_action = None
        most1s = 0
        for a in self.get_valid_moves(board):
            # we need the number of open 3s it forms
            if self.open2count(board, player, a) > most2s:
                most1s_action = a
                most1s = self.open2count(board, player, a)
        if most1s_action is not None:
            print('doing 1s action')
            return most1s_action
        
        print('doing random action')
        return random.choice(self.get_valid_moves(board))
        

x = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
)

trick2test = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 1, 1, 1, 0],
        [0, 0, 1, 2, 1, 2, 0],
        [0, 0, 2, 2, 2, 2, 0],
    ]
)

x = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 1, 1, 1, 0],
        [2, 0, 1, 2, 1, 2, 0],
        [2, 0, 2, 1, 2, 2, 0],
    ]
)


open3test = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 1, 1, 1, 0],
        [0, 0, 1, 2, 1, 2, 0],
        [0, 0, 2, 2, 2, 2, 0],
    ]
)

my_heur_player = HeuristicPlayer()


# y = my_heur_player.take_action(x, 6, 1)
# y = my_heur_player.undo_action(y, 6, 1)
# print('a is ', y)

# win = my_heur_player.check_win(x, 1, 4)
# print('win is', win)


# trick2 = my_heur_player.form_double_trick(trick2test, 1, 4)
# print('trick2 is',  trick2)

# open3 = my_heur_player.open3count(open3test, 1, 4)
# print('open3 is', open3)

x = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
)

a = my_heur_player.heuristic_player_move(x,1)
print('a is ', a)