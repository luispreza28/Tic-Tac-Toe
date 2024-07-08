class Game:
    def __init__(self, id):
        self.id = id
        self.board = [None] * 9
        self.ready = False
        self.current_player = 0
        self.game_over = False
        self.winner = None
        self.p1Went = False
        self.p2Went = False

    def play(self, move, player):
        if player == self.current_player and self.board[move] is None and not self.game_over:
            self.board[move] = player
            self.p1Went = True if player == 0 else self.p1Went
            self.p2Went = True if player == 1 else self.p2Went

        if self.check_winner():
            self.winner = player
            self.game_over = True
        else:
            self.current_player = 1 - self.current_player

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]

        for combo in winning_combinations:
            if self.board[combo[0]] is not None and self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]:
                return True

        return False

    def reset(self):
        self.board = [None] * 9
        self.current_player = 0
        self.game_over = False
        self.winner = None
        self.p1Went = False
        self.p2Went = False

    def get_state(self):
        return {
            "board": self.board,
            "current_player": self.current_player,
            "game_over": self.game_over,
            "winner": self.winner,
            "p1Went": self.p1Went,
            "p2Went": self.p2Went
        }

    def connected(self):
        return self.ready
