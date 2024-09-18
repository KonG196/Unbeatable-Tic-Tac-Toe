import random

class SmartComputerPlayer:
    def __init__(self, player):
        self.player = player

    def get_move(self, game):
        # Check if computer can win in the next move
        for row in range(3):
            for col in range(3):
                if game.board[row][col] == ' ':
                    game.board[row][col] = self.player
                    if game.check_win(self.player):
                        return row, col
                    game.board[row][col] = ' '

        # Check if opponent can win in the next move and block them
        opponent = 'O' if self.player == 'X' else 'X'
        for row in range(3):
            for col in range(3):
                if game.board[row][col] == ' ':
                    game.board[row][col] = opponent
                    if game.check_win(opponent):
                        return row, col
                    game.board[row][col] = ' '

        # Choose a random move
        available_moves = []
        for row in range(3):
            for col in range(3):
                if game.board[row][col] == ' ':
                    available_moves.append((row, col))

        if available_moves:
            return random.choice(available_moves)
        else:
            return None