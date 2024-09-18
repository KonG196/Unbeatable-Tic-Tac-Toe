#include <vector>
#include <string>

#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

class TicTacToe {
private:
    std::vector<std::vector<char>> board;
    std::string current_player;
    std::string player1_name;
    std::string player2_name;

public:
    TicTacToe();
    void printBoard() const;
    std::vector<std::pair<int, int>> getAvailableMoves() const;
    void makeMove(int row, int col, char marker);
    bool hasWon(const std::string& player);
    bool isBoardFull();
    void switchPlayers();
    void play();
};

extern "C" {
    DLL_EXPORT TicTacToe* TicTacToe_new();
    DLL_EXPORT void TicTacToe_delete(TicTacToe* tictactoe);
    DLL_EXPORT void TicTacToe_play(TicTacToe* tictactoe);
}
