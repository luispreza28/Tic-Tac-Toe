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

    def evaluate(self, board):
        score = 0

        for row in board:
            if row.count('O') == 3:
                score += 10
            elif row.count('X') == 3:
                score -= 10

        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col]:
                if board[0][col] == 'O':
                    score += 10
                elif board[0][col] == 'X':
                    score -= 10

        if board[0][0] == board[1][1] == board[2][2]:
            if board[0][0] == 'O':
                score += 10
            elif board[0][0] == 'X':
                score -= 10

        if board[0][2] == board[1][1] == board[2][0]:
            if board[0][2] == 'O':
                score += 10
            elif board[0][2] == 'X':
                score -= 10

        if score == 0 and not any('' in row for row in board):
            return 0

        return score

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        score = self.evaluate(board)

        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if not any('' in row for row in board):
            return 0

        if is_maximizing:
            max_eval = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'O'
                        eval = self.minimax(board, depth + 1, False, alpha, beta)
                        board[i][j] = ''
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'X'
                        eval = self.minimax(board, depth + 1, True, alpha, beta)
                        board[i][j] = ''
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def find_best_move(self, board):
        best_eval = -float('inf')
        best_move = (-1, -1)

        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    eval = self.minimax(board, 0, False, -float('inf'), float('inf'))
                    board[i][j] = ''
                    if eval > best_eval:
                        best_eval = eval
                        best_move = (i, j)
        return best_move
