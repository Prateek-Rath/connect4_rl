# minimax related stuff
import numpy as np
import random
import copy

class Player:
    def __init__(self):
        pass
    def play(self, state):
        pass


class MiniMaxPlayer(Player):
    def __init__(self):
        super().__init__()
        self.ROWS = 6
        self.COLS = 7
        self.CONNECT = 4
        self.WIN_REWARD = 10000
        self.BOTH_OPEN_THREE = 100
        self.SINGLE_OPEN_THREE = 20
        self.BOTH_OPEN_TWO = 40
        self.SINGLE_OPEN_TWO = 10
        self.CLOSED = 0
        self.not_sure = -3

   # Returns best score,best action for player
    def minimax(self, state, depth, player, maximizing_player):
        winner = self.check_winner(state)
        if winner == maximizing_player:
            return (np.iinfo(np.int32).max, None)
        elif winner == 1+(maximizing_player%2):
            return (np.iinfo(np.int64).min, None)
        elif self.is_draw(state):
              return (0, None)
        elif depth == 0:
            # print('reached 0 depth in ')
            # print('evaluation is', self.evaluate(state, player))
            # print(state)
            return (self.evaluate(state, player), None)
            # return (self.not_sure, random.choice(self.valid_moves(state)))
    
        if player == maximizing_player:
            max_eval = np.iinfo(np.int64).min
            best_actions = []
            for col in self.valid_moves(state):
                next_state = self.make_move(state, col, player)
                eval_score, _ = self.minimax(next_state, depth - 1, 1+(player%2), maximizing_player)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_actions = []
                    best_actions.append(col)
                elif eval_score == max_eval:
                    max_eval = eval_score
                    best_actions.append(col)
            if len(best_actions) == 0:
            #   print('random action by minimax, hopeless')
            #   print(state)
              best_action = random.choice(self.valid_moves(state))
              return (max_eval, best_action)
            elif len(best_actions) == 1:
            #   print('only the best', best_actions[0])
            #   print(state)
              return max_eval, best_actions[0]
            
            # print('random action by minimax no worries', best_actions)
            # print(state)

            return (max_eval, random.choice(best_actions)) # fix here should return a random action
        else:
            min_eval = np.iinfo(np.int32).max
            best_actions = []
            for col in self.valid_moves(state):
                next_state = self.make_move(state, col, player)
                eval_score, _ = self.minimax(next_state, depth - 1, 1+(player % 2), maximizing_player)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_actions = []
                    best_actions.append(col)
                elif eval_score == min_eval:
                    min_eval = eval_score
                    best_actions.append(col)
            if len(best_actions) == 0:
              best_action = random.choice(self.valid_moves(state))
            #   print('random action by minimax')
              return (min_eval, best_action)
            elif len(best_actions) == 1:
              return min_eval, best_actions[0]
            return (min_eval, random.choice(best_actions)) # fix here, returns a random action

    def valid_moves(self, state):
      state_2d = state.reshape(self.ROWS, self.COLS)  # Reshape to 2D
      return [c for c in range(self.COLS) if state_2d[0][c] == 0]  # Check top row

    def make_move(self, state, col, player):
        """Return new state after placing player's piece in the specified column."""
        new_state = state.copy().reshape(self.ROWS, self.COLS)  # Reshape to 2D
        for row in reversed(range(self.ROWS)):
            if new_state[row][col] == 0:
                new_state[row][col] = player
                break  # Fixed indentation
        return new_state

    def is_draw(self, state):
        """Check if the board is full (draw condition)."""
        state_2d = state.reshape(self.ROWS, self.COLS)
        return all(state_2d[0][c] != 0 for c in range(self.COLS))  # All top row occupied

    def check_winner(self, state):
        """Check if there's a winner (4 in a row horizontally, vertically, or diagonally)."""
        state_2d = state.reshape(self.ROWS, self.COLS)

        # Horizontal check
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if (state_2d[row][col] != 0 and
                    state_2d[row][col] == state_2d[row][col+1] ==
                    state_2d[row][col+2] == state_2d[row][col+3]):
                    return state_2d[row][col]

        # Vertical check
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if (state_2d[row][col] != 0 and
                    state_2d[row][col] == state_2d[row+1][col] ==
                    state_2d[row+2][col] == state_2d[row+3][col]):
                    return state_2d[row][col]

        # Diagonal (positive slope) check
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if (state_2d[row][col] != 0 and
                    state_2d[row][col] == state_2d[row+1][col+1] ==
                    state_2d[row+2][col+2] == state_2d[row+3][col+3]):
                    return state_2d[row][col]

        # Diagonal (negative slope) check
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                if (state_2d[row][col] != 0 and
                    state_2d[row][col] == state_2d[row-1][col+1] ==
                    state_2d[row-2][col+2] == state_2d[row-3][col+3]):
                    return state_2d[row][col]

        return None  # No winner found

    def evaluate(self, state, player):
        # simplify
        # opponent = 1 + (player%2)
        # if(self.check_winner(state) == player):
        #     return self.WIN_REWARD
        # elif (self.check_winner(state) == opponent):
        #     return -1*self.WIN_REWARD
        # else:
        #     return 0
        #simply end
        return self.score_position(state, player) - self.score_position(state, 1+(player % 2))

    def score_position(self, state, player):
        score = 0

        # Score center column
        center_array = [state[r][self.COLS // 2] for r in range(self.ROWS)]
        score += center_array.count(player) * 3

        # Score horizontal
        for row in range(self.ROWS):
            row_array = state[row]
            for col in range(self.COLS - 3):
                left = np.array([row_array[col-1] if col-1 >= 0 else (1+(player%2))])
                middle = row_array[col:col + self.CONNECT].flatten()
                right = np.array([row_array[col+self.CONNECT] if col+self.CONNECT < self.COLS else 1 + (player%2)])
                window = np.hstack([left, middle, right])
                score += self.evaluate_window(window, player)

        # Score vertical
        for col in range(self.COLS):
            col_array = np.array([state[r][col] for r in range(self.ROWS)])
            for row in range(self.ROWS - 3):
                left = np.array([col_array[row-1] if row-1 >= 0 else 1 + (player%2)])
                middle = col_array[row:row + self.CONNECT].flatten()
                right = np.array([col_array[row+self.CONNECT] if row+self.CONNECT < self.ROWS else 1 + (player%2)])
                window = np.hstack([left, middle, right])
                score += self.evaluate_window(window, player)

        # Score positive diagonal
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                left = np.array([state[row - 1][col - 1] if row - 1 >= 0 and col - 1 >= 0 else 1 + (player%2)])
                middle = np.array([state[row + i][col + i] for i in range(self.CONNECT)])
                right = np.array([state[row + self.CONNECT][col + self.CONNECT] if row + self.CONNECT < self.ROWS and col + self.CONNECT < self.COLS else 1 + (player%2)])
                window = np.hstack([left, middle, right])
                score += self.evaluate_window(window, player)

        # Score negative diagonal
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                left = np.array([state[row + 1][col - 1] if row + 1 < self.ROWS and col - 1 >= 0 else 1 + (player%2)])
                middle = np.array([state[row - i][col + i] for i in range(self.CONNECT)])
                right = np.array([state[row - self.CONNECT][col + self.CONNECT] if row - self.CONNECT >= 0 and col + self.CONNECT < self.COLS else 1 + (player%2)])
                window = np.hstack([left, middle, right])
                score += self.evaluate_window(window, player)

        return score

    def evaluate_window(self, window6, player):
        try:
          assert(len(window6)==6)
        except:
          print(window6)
        opponent = 1 + (player%2)  # Toggle between player 1 and 2

        # Immediate block: opponent has 4 in a row
        if np.count_nonzero(window6 == opponent) == 4:
            return 0

        # Winning condition: player has 4 in a row in the middle of the window
        if np.count_nonzero(window6[1:5] == player) == 4:
            return self.WIN_REWARD
        

        # Detect open/closed three-in-a-row
        for i in range(1, 3):
            if window6[1 + i] == player and window6[2 + i] == player and window6[3 + i] == player:
                left = window6[i - 1]
                right = window6[i + 3]
                if left == 0 and right == 0:
                    return self.BOTH_OPEN_THREE
                elif left == opponent and right == opponent:
                    return self.CLOSED
                else:
                    return self.SINGLE_OPEN_THREE

        # Detect open/closed two-in-a-row
        for i in range(1, 4):
            if window6[1 + i] == player and window6[2 + i] == player:
                left = window6[i - 1]
                right = window6[i + 2]
                if left == 0 and right == 0:
                    return self.BOTH_OPEN_TWO
                elif left == opponent and right == opponent:
                    return self.CLOSED
                else:
                    return self.SINGLE_OPEN_TWO  # <- changed this to match two-in-a-row logic

        return self.CLOSED

