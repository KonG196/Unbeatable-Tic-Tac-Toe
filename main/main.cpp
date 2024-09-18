#include <iostream>

using namespace std;

class Game {
private:
    char board[3][3];
    char currentPlayer;
public:
    Game() {
        initializeBoard();
        currentPlayer = 'X';
    }

    void initializeBoard(){
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                board[i][j] = ' ';
            }
        }
    }



    char switchPlayer(char currentPlayer) {
        if (currentPlayer == 'X') {
            currentPlayer = 'O';
        }else {
            currentPlayer = 'X';
        }
        return currentPlayer;
    }

    char getCurrentPlayer() {
        return currentPlayer;
    }

    bool checkWin(char player, int& row1, int& col1, int& row2, int& col2, int& row3, int& col3) {
        // ѕерев≥рка перемоги по р€дках, стовпц€х та д≥агонал€х
        for (int i = 0; i < 3; ++i) {
            if (board[i][0] == player && board[i][1] == player && board[i][2] == player) {
                row1 = i;
                col1 = 0;
                row2 = i;
                col2 = 1;
                row3 = i;
                col3 = 2;
                return true;
            }
            if (board[0][i] == player && board[1][i] == player && board[2][i] == player) {
                row1 = 0;
                col1 = i;
                row2 = 1;
                col2 = i;
                row3 = 2;
                col3 = i;
                return true;
            }
        }
        if (board[0][0] == player && board[1][1] == player && board[2][2] == player) {
            row1 = 0;
            col1 = 0;
            row2 = 1;
            col2 = 1;
            row3 = 2;
            col3 = 2;
            return true;
        }
        if (board[0][2] == player && board[1][1] == player && board[2][0] == player) {
            row1 = 0;
            col1 = 2;
            row2 = 1;
            col2 = 1;
            row3 = 2;
            col3 = 0;
            return true;
        }
        return false;
    }

    bool makeMove(int row, int col, char player) {
        // ѕерев≥рка на правильн≥сть ходу
        if (board[row][col] != ' ') {
            return false;
        }else{
        board[row][col] = player;
        return true;
        }
    }



    bool isBoardFull() {
        // ѕерев≥рка, чи заповнена дошка
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                if (board[i][j] == ' ') {
                    return false;
                }
            }
        }
        return true;
    }


};

extern "C" {
Game* createGame() {
    return new Game();
}

bool makeMove(Game* game, int row, int col, char player) {
    return game->makeMove(row, col, player);
}

bool checkWin(Game* game, char player) {
    int row1, col1, row2, col2, row3, col3;
    return game->checkWin(player, row1, col1, row2, col2, row3, col3);
}

bool isBoardFull(Game* game) {
    return game->isBoardFull();
}

void deleteGame(Game* game) {
    delete game;
}

char switchPlayer(Game* game, char currentPlayer) {
    return game->switchPlayer(currentPlayer);
}

void getWinningCombination(Game* game, int& row1, int& col1, int& row2, int& col2, int& row3, int& col3) {
    char player = 'X';
    if (game->checkWin(player, row1, col1, row2, col2, row3, col3)) {
        return;
    }
    player = 'O';
    if (game->checkWin(player, row1, col1, row2, col2, row3, col3)) {
        return;
    }
    row1 = -1;
    col1 = -1;
    row2 = -1;
    col2 = -1;
    row3 = -1;
    col3 = -1;
}
}
