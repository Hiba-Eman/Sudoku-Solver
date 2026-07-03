import tkinter as tk
from tkinter import messagebox

from generator import SudokuGenerator

BOX_COLORS = ["#242424", "#2B2B2B"]
WRONG_COLOR = "#5C2323"
LOCKED_BG = "#3A3A3A"
LOCKED_FG = "#BBBBBB"


class GameFrame(tk.Frame):
    """Play mode - generated puzzle, difficulty levels, checking, win detection."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1E1E1E")
        self.controller = controller

        self.cells = []
        self.locked = [[False] * 9 for _ in range(9)]
        self.puzzle = None
        self.solution = None

        self.difficulty = tk.StringVar(value="medium")
        self.elapsed = 0
        self.timer_running = False
        self.started = False

        validate = self.register(self.validate_input)
        self.validate = validate

        self.build_ui()

    def on_show(self):
        if not self.started:
            self.new_game()
            self.started = True
        elif not self.timer_running:
            self.timer_running = True
            self.update_timer()

    # ---------- UI construction ----------

    def build_ui(self):
        top = tk.Frame(self, bg="#1E1E1E")
        top.pack(fill="x", pady=(15, 0), padx=15)

        back_button = tk.Button(
            top, text="← Menu", bg="#333333", fg="white", relief="flat",
            font=("Segoe UI", 10, "bold"), command=self.go_back
        )
        back_button.pack(side="left")
        back_button.bind("<Enter>", lambda e: e.widget.config(cursor="hand2"))

        title = tk.Label(
            top, text="Play Sudoku", bg="#1E1E1E", fg="white",
            font=("Segoe UI", 16, "bold")
        )
        title.pack(side="left", padx=20)

        self.timer_label = tk.Label(
            top, text="00:00", bg="#1E1E1E", fg="#4CAF50",
            font=("Segoe UI", 14, "bold")
        )
        self.timer_label.pack(side="right")

        diff_frame = tk.Frame(self, bg="#1E1E1E")
        diff_frame.pack(pady=12)

        for level in ("easy", "medium", "hard"):
            radio = tk.Radiobutton(
                diff_frame, text=level.capitalize(), variable=self.difficulty,
                value=level, bg="#1E1E1E", fg="white", selectcolor="#2B2B2B",
                activebackground="#1E1E1E", activeforeground="white",
                font=("Segoe UI", 10)
            )
            radio.pack(side="left", padx=10)

        self.board_frame = tk.Frame(self, bg="#1E1E1E")
        self.board_frame.pack(pady=10)
        self.create_grid()

        button_frame = tk.Frame(self, bg="#1E1E1E")
        button_frame.pack(pady=15)

        new_game_button = tk.Button(
            button_frame, text="New Game", width=12, bg="#1E88E5", fg="white",
            activebackground="#1976D2", activeforeground="white", relief="flat",
            font=("Segoe UI", 11, "bold"), command=self.new_game
        )
        new_game_button.grid(row=0, column=0, padx=10)

        check_button = tk.Button(
            button_frame, text="Check", width=12, bg="#4CAF50", fg="white",
            activebackground="#45A049", activeforeground="white", relief="flat",
            font=("Segoe UI", 11, "bold"), command=self.check_solution
        )
        check_button.grid(row=0, column=1, padx=10)

        for button in (new_game_button, check_button):
            button.bind("<Enter>", lambda e: e.widget.config(cursor="hand2"))

        self.status_label = tk.Label(
            self, text="", bg="#1E1E1E", fg="white", font=("Segoe UI", 11)
        )
        self.status_label.pack(pady=5)

    def create_grid(self):
        self.cells = []

        for row in range(9):
            current_row = []

            for col in range(9):
                box_index = (row // 3) * 3 + (col // 3)
                bg_color = BOX_COLORS[box_index % 2]

                cell = tk.Entry(
                    self.board_frame, width=3, font=("Segoe UI", 20, "bold"),
                    justify="center", bg=bg_color, fg="white",
                    insertbackground="white", relief="flat", bd=0,
                    highlightthickness=1, highlightbackground="#555555",
                    highlightcolor="#4CAF50", validate="key",
                    validatecommand=(self.validate, "%P")
                )

                cell.grid(
                    row=row, column=col,
                    padx=(6 if col % 3 == 0 else 1, 1),
                    pady=(6 if row % 3 == 0 else 1, 1),
                    ipadx=4, ipady=6
                )

                cell.bind("<KeyRelease>", lambda e, r=row, c=col: self.on_cell_edit())

                current_row.append(cell)

            self.cells.append(current_row)

    # ---------- game lifecycle ----------

    def new_game(self):
        generator = SudokuGenerator()
        self.puzzle, self.solution = generator.generate_puzzle(self.difficulty.get())
        self.locked = [[self.puzzle[r][c] != 0 for c in range(9)] for r in range(9)]

        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]
                box_index = (row // 3) * 3 + (col // 3)
                base_bg = BOX_COLORS[box_index % 2]

                cell.config(state="normal")
                cell.delete(0, tk.END)

                value = self.puzzle[row][col]
                if value != 0:
                    cell.insert(0, str(value))
                    cell.config(
                        state="disabled",
                        disabledbackground=LOCKED_BG,
                        disabledforeground=LOCKED_FG,
                    )
                else:
                    cell.config(bg=base_bg, fg="white")

        self.status_label.config(text="")
        self.elapsed = 0
        self.timer_running = True
        self.update_timer()

    def go_back(self):
        self.timer_running = False
        self.controller.show_frame("menu")

    # ---------- timer ----------

    def update_timer(self):
        if not self.timer_running:
            return

        minutes, seconds = divmod(self.elapsed, 60)
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        self.elapsed += 1
        self.after(1000, self.update_timer)

    # ---------- board helpers ----------

    def get_board(self):
        board = []
        for row in self.cells:
            current_row = []
            for cell in row:
                value = cell.get()
                current_row.append(int(value) if value != "" else 0)
            board.append(current_row)
        return board

    def reset_cell_color(self, row, col):
        box_index = (row // 3) * 3 + (col // 3)
        self.cells[row][col].config(bg=BOX_COLORS[box_index % 2])

    def validate_input(self, value):
        if value == "":
            return True
        return value in "123456789" and len(value) == 1

    # ---------- checking / winning ----------

    def check_solution(self):
        board = self.get_board()
        complete = True
        all_correct = True

        for row in range(9):
            for col in range(9):
                if self.locked[row][col]:
                    continue

                value = board[row][col]

                if value == 0:
                    complete = False
                    self.reset_cell_color(row, col)
                    continue

                if value == self.solution[row][col]:
                    self.reset_cell_color(row, col)
                else:
                    self.cells[row][col].config(bg=WRONG_COLOR)
                    all_correct = False

        if not complete:
            self.status_label.config(
                text="Keep going — the board isn't full yet.", fg="#FFC107"
            )
            return

        if all_correct:
            self.declare_win()
        else:
            self.status_label.config(
                text="Some cells are incorrect — they're highlighted in red.",
                fg="#E53935"
            )

    def on_cell_edit(self):
        board = self.get_board()

        for row in range(9):
            for col in range(9):
                if not self.locked[row][col] and board[row][col] == 0:
                    return  # board not full yet, nothing to check

        if board == self.solution:
            self.declare_win()

    def declare_win(self):
        if not self.timer_running:
            return

        self.timer_running = False
        final_time = self.timer_label["text"]
        self.status_label.config(
            text=" Congratulations! You solved the puzzle!", fg="#4CAF50"
        )
        messagebox.showinfo(
            "You Win!",
            f" Congratulations!\n\nYou solved the puzzle in {final_time}!"
        )