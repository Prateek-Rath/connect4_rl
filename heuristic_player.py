import numpy as np

class HeuristicPlayer():
    def __init__(self):
        pass

    def get_valid_moves(self, board):
        valid = []
        for c in range(0, 7):
            if board[0][c] == 0:
                valid.append(c)
        return valid
    
    def form_double_open_3s(self, board, player):
        r = -1
        for a in self.get_valid_moves(board):
            for i in range(5,-1,-1):
                if board[i][a] == 0:
                    r = i
                    break
            
            board[r][a] = player
            # see the impact of the move

            # horizontal
            horlen = 0
            for c in range(a-1, -1, -1):
                if board[r][c] == player:
                    horlen+=1
                else:
                    break
            for c in range(a+1, 7, 1):
                if board[r][c] == player:
                    horlen +=1
                else:
                    break
    

    def check_open_3s(self, board, player):
        if player == 'p1':
            player = 1
        elif player == 'p2':
            pllayer = 2
        """Check for open 3s for the given player and return the list of columns that need to be blocked."""
        opponent = 2 if player == 1 else 1
        open_3s = []

        for row in range(6):
            for col in range(7):
                if board[row, col] != 0:
                    continue  # skip non-empty cells
                # Check horizontal, vertical, diagonal patterns for open 3s
                for direction in [(0, 1), (1, 0), (1, 1), (1, -1)]:  # Right, Down, Diagonal Down, Diagonal Up
                    pattern = [board[row + i*direction[0], col + i*direction[1]] if 0 <= row + i*direction[0] < 6 and 0 <= col + i*direction[1] < 7 else None for i in range(3)]
                    if pattern.count(opponent) == 2 and pattern.count(0) == 1:
                        open_3s.append((row, col))
        return open_3s
    
    def check_immediate_win(self, board, player):
        """Check if the player can win in the next move."""
        for col in range(7):
            row = self.get_next_open_row(board, col)
            if row is not None:
                temp_board = board.copy()
                temp_board[row, col] = player
                if self.check_win(temp_board, player):
                    return col
        return None


    def check_open_2s(self, board, player):
        """Check for open 2s for the given player."""
        open_2s = []
        
        for row in range(6):
            for col in range(7):
                if board[row, col] != 0:
                    continue
                # Check horizontal, vertical, diagonal patterns for open 2s
                for direction in [(0, 1), (1, 0), (1, 1), (1, -1)]:  # Right, Down, Diagonal Down, Diagonal Up
                    pattern = [board[row + i*direction[0], col + i*direction[1]] if 0 <= row + i*direction[0] < 6 and 0 <= col + i*direction[1] < 7 else None for i in range(2)]
                    if pattern.count(player) == 1 and pattern.count(0) == 1:
                        open_2s.append((row, col))
        return open_2s


    def evaluate_move(self, board, move, player):
        """Evaluate a move based on proximity to the center and whether it forms open 3s or 2s."""
        col = move
        center_bias = abs(col - 3)  # Columns closer to 3 (center) have higher priority
        return center_bias


    def heuristic_player_move(self, board, player):
        """Heuristic player move logic."""
        # check if you yourself have a win
        winning_col = self.check_immediate_win(board, player)
        if winning_col is not None:
            return winning_col


        # Step 1: Block opponent's open wins
        opponent = 1 + (player%2)
        winning_col = self.check_immediate_win(board, opponent)
        if winning_col is not None:
            return winning_col

        # Step 2: Try to form double open 3s for yourself
        

        # Step 3: Try to form open 2s for yourself
        open_2s = self.check_open_2s(board, player)
        if open_2s:
            # Prioritize open 2s closer to the center
            best_move = min(open_2s, key=lambda x: self.evaluate_move(board, x[1], player))
            return best_move[1]

        # Step 4: If no 2s or 3s, choose the best column closer to center
        valid_moves = [col for col in range(7) if board[0, col] == 0]  # Get valid moves
        best_move = min(valid_moves, key=lambda col: self.evaluate_move(board, col, player))
        return best_move


