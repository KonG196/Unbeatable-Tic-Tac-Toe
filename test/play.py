import tkinter as tk

from PIL import Image, ImageTk
import ctypes

import check_win
import comp

# Завантаження бібліотеки C++
game_lib = ctypes.CDLL("C:\\Users\\maks0\\My Drive\\KURSOVA1KURS2SEM\\test\\main.dll")  # Вкажіть шлях до файлу бібліотеки

# Оголошення типів аргументів та поверненого значення
game_lib.createGame.restype = ctypes.c_void_p
game_lib.createGame.argtypes = []

game_lib.makeMove.restype = ctypes.c_bool
game_lib.makeMove.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_char]

game_lib.checkWin.restype = ctypes.c_bool
game_lib.checkWin.argtypes = [ctypes.c_void_p, ctypes.c_char]

game_lib.isBoardFull.restype = ctypes.c_bool
game_lib.isBoardFull.argtypes = [ctypes.c_void_p]

game_lib.deleteGame.argtypes = [ctypes.c_void_p]

class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Хрестики-нолики")
        self.window.geometry("807x651")

        self.background_image = ImageTk.PhotoImage(Image.open("C:\\Users\\maks0\\My Drive\\KURSOVA1KURS2SEM\\test\\pretty_bg2.png"))
        self.background_label = tk.Label(self.window, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.win_bool = False
        self.current_player = b'X'
        self.player_score = {b'X': 0, b'O': 0}

        self.game_label = tk.Label(self.window, text="Хрестики-нолики", font=("Comic Sans MS", 26, "bold", "italic"),
                                   bg="white", fg="#ff8628")
        self.game_label.pack(pady=0)

        self.score_label = tk.Label(self.window, text="Рахунок\n X - 0\t\tO - 0",
                                    font=("Comic Sans MS", 14, "bold", "italic"), fg="#6d6d6d", bg="white")
        self.score_label.pack(pady=10)

        self.info_label = tk.Label(self.window, text=" ", font=("Comic Sans MS", 14, "bold", "italic"), bg="white",
                                   fg="#6d6d6d")
        self.info_label.pack(pady=5)



        self.game_mode = tk.StringVar()
        self.game_mode.set("PvC")

        self.game = ctypes.c_void_p(game_lib.createGame())

        self.button_frame = tk.Frame(self.window, bg="white")  # Контейнер для кнопок сітки
        self.button_frame.pack()

        self.buttons = []

        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.button_frame, text=" ", width=3, height=1,
                                   command=lambda state=tk.NORMAL, row=i, col=j: self.on_button_click(row, col),
                                   font=("Comic Sans MS", 36, "bold", "italic", "roman"), borderwidth=0)
                button.grid(row=i, column=j, padx=2, pady=2)
                row.append(button)
            self.buttons.append(row)

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ", state=tk.NORMAL, bg="#ff8628")

        self.game_mode_switcher = tk.Button(self.window, text="Гра проти ШІ", width=11, height=1, borderwidth=0,
                                            bg="white", fg="#88dc00", font=("Comic Sans MS", 18, "bold", "italic", "roman"),
                                            command=self.PvAI_switch)
        self.game_mode_switcher.pack(pady=10, side="left")

        self.game_mode_switcher = tk.Button(self.window, text="Гра проти\nдругого гравця", width=12, height=2, borderwidth=0,
                                           bg="white", fg="#88dc00", font=("Comic Sans MS", 18, "bold", "italic", "roman"),
                                             command=self.PvP_switch)
        self.game_mode_switcher.pack(pady=10, side="right")

        self.reset_button = tk.Button(self.window, text="Очистити", command=self.reset_board, bg="white", fg="#ff8628",
                                      font=("Comic Sans MS", 16, "bold", "italic", "roman"), borderwidth=0)
        self.reset_button.pack(pady=10, side="bottom")

        # Центруємо вікно
        self.window.eval('tk::PlaceWindow . center')
        self.current_player = b'X'
        self.ai_move()
        self.window.mainloop()

    def on_button_click(self, row, col):
        if game_lib.makeMove(self.game, row, col, self.current_player):
            self.buttons[row][col].config(text=self.current_player.decode(), state=tk.DISABLED, fg="black")

            self.check_game_result()
            self.switch_players()
            if self.game_mode.get() == "PvC":
                self.ai_move()
            elif self.win_bool is False:
                self.info_label.config(text="Гравець " + self.current_player.decode() + ", зробіть свій хід.",
                                        bg="white", fg="#6d6d6d")

    def PvAI_switch(self):
        self.game_mode.set("PvC")
        self.player_score[b'O'] = 0;    self.player_score[b'X'] = 0; self.update_score_label()
        self.reset_board()

    def PvP_switch(self):
        self.game_mode.set("PvP")
        self.player_score[b'X'] = 0;    self.player_score[b'O'] = 0; self.update_score_label()
        self.reset_board()

    def switch_players(self):
        if self.current_player == b'X':
            self.current_player = b'O'
        else:
            self.current_player = b'X'

    def ai_move(self):
        self.info_label.config(text="ШІ робить хід...", bg="white", fg="#6d6d6d")
        self.info_label.after(500, self.make_computer_move)

    def make_computer_move(self):
        available_moves = []
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["state"] != tk.DISABLED:
                    available_moves.append((i, j))
        if available_moves:
            row, col = self.smart_comp_move(self.current_player.decode())
            if game_lib.makeMove(self.game, row, col, self.current_player):
                self.buttons[row][col].config(text=self.current_player.decode(), state=tk.DISABLED)
                self.check_game_result()
                self.switch_players()
            if self.win_bool is not True:
                self.info_label.config(text="Гравець, зробіть свій хід.", bg="white", fg="#88dc00")


    def smart_comp_move(self, player):
        game = check_win.TicTacToeGame()
        game.board = [[self.buttons[i][j]['text'] for j in range(3)] for i in range(3)]
        comp_player = comp.SmartComputerPlayer(player)
        move = comp_player.get_move(game)
        return move[0], move[1]


    def check_game_result(self):

        row1 = ctypes.c_int();   col1 = ctypes.c_int()
        row2 = ctypes.c_int();   col2 = ctypes.c_int()
        row3 = ctypes.c_int();   col3 = ctypes.c_int()

        if game_lib.checkWin(self.game, b'X'):

            game_lib.getWinningCombination(self.game, ctypes.byref(row1), ctypes.byref(col1), ctypes.byref(row2),
                                           ctypes.byref(col2), ctypes.byref(row3), ctypes.byref(col3))

            self.highlight_winning_combination(row1.value, col1.value, row2.value, col2.value, row3.value, col3.value)
            self.disable_buttons()
            self.player_score[b'X'] += 1
            self.update_score_label()
            if self.game_mode.get() == "PvC":
                self.info_label.config(text="Поразка! ШІ виграв!", bg="white", fg="#a0332b", font=("Comic Sans MS", 16, "bold", "italic"))
            else:
                self.info_label.config(text="Перемога! Гравець X виграв!", fg="#88dc00")
            self.win_bool = True
        elif game_lib.checkWin(self.game, b'O'):
            game_lib.getWinningCombination(self.game, ctypes.byref(row1), ctypes.byref(col1), ctypes.byref(row2),
                                           ctypes.byref(col2), ctypes.byref(row3), ctypes.byref(col3))
            self.highlight_winning_combination(row1.value, col1.value, row2.value, col2.value, row3.value, col3.value)
            self.disable_buttons()
            self.player_score[b'O'] += 1
            self.update_score_label()
            self.info_label.config(text="Перемога! Гравець O виграв!", bg="white", fg="#88dc00",
                                   font=("Comic Sans MS", 16, "bold", "italic"))
            self.win_bool = True
        elif game_lib.isBoardFull(self.game):
            self.disable_buttons()
            self.update_score_label()
            self.info_label.config(text="Нічия!", bg="white", fg="grey",
                                   font=("Comic Sans MS", 16, "bold", "italic"))
            self.win_bool = True

    def highlight_winning_combination(self, row1, col1, row2, col2, row3, col3):
        if self.game_mode.get() == "PvC":
            self.buttons[row1][col1].config(bg="#a0332b")
            self.buttons[row2][col2].config(bg="#a0332b")
            self.buttons[row3][col3].config(bg="#a0332b")
        else:
            self.buttons[row1][col1].config(bg="#88dc00")
            self.buttons[row2][col2].config(bg="#88dc00")
            self.buttons[row3][col3].config(bg="#88dc00")


    def disable_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.DISABLED)

    def update_score_label(self):
        score_text = f"Рахунок\n X - {self.player_score[b'X']}\t\tO - {self.player_score[b'O']}"
        self.score_label.config(text=score_text)

    def reset_board(self):
        game_lib.deleteGame(self.game)
        self.game = ctypes.c_void_p(game_lib.createGame())

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ", state=tk.NORMAL, bg="#ff8628")
        self.current_player = b'X'
        self.info_label.config(text=" ", font=("Comic Sans MS", 14, "bold", "italic"), fg="#6d6d6d", bg="white")
        self.win_bool = False
        if self.game_mode.get() == "PvC":
            self.ai_move()
        else:
            self.info_label.config(text="Гравець " + self.current_player.decode() + ", зробіть свій хід.",
                                   bg="white", fg="#6d6d6d")

if __name__ == "__main__":
    tic_tac_toe = TicTacToeGUI()


#

