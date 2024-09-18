class TicTacToeGame:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.winning_combination = []

    def check_win(self, player):
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                self.winning_combination = [(i, 0), (i, 1), (i, 2)]
                return True

        # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                self.winning_combination = [(0, i), (1, i), (2, i)]
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            self.winning_combination = [(0, 0), (1, 1), (2, 2)]
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            self.winning_combination = [(0, 2), (1, 1), (2, 0)]
            return True

        return False