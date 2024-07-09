import random

class AIEnemy:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self,board):
        moves = self.available_moves(board)
        if moves:
            return random.choice(moves)
        else:
            return None

    def available_moves(self, board):
        moves = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == '':
                    moves.append((row, col))
        return moves