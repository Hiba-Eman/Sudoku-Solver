import tkinter as tk
from tkinter import messagebox
import time

from solver import SudokuSolver

# Alternating background shades for 3x3 boxes (classic sudoku "zebra" look)
BOX_COLORS = ["#242424", "#2B2B2B"]

TRY_COLOR = "#FFD54F"
PLACE_COLOR = "#66BB6A"
BACKTRACK_COLOR = "#E53935"


class MainMenuFrame(tk.Frame):
    """Landing page - lets the user choose Play or Solve."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1E1E1E")
        self.controller = controller

        title = tk.Label(
            self, text="🧩 Sudoku Suite",
            bg="#1E1E1E", fg="white", font=("Segoe UI", 30, "bold")
        )
        title.pack(pady=(140, 10))

        subtitle = tk.Label(
            self, text="Solve. Play. Enjoy.",
            bg="#1E1E1E", fg="#8A8A8A", font=("Segoe UI", 12)
        )
        subtitle.pack(pady=(0, 70))

        play_button = tk.Button(
            self, text="🎮  Play Sudoku", width=24, height=2,
            bg="#4CAF50", fg="white", activebackground="#45A049",
            activeforeground="white", relief="flat",
            font=("Segoe UI", 13, "bold"),
            command=lambda: controller.show_frame("game")
        )
        play_button.pack(pady=12)

        solve_button = tk.Button(
            self, text="🤖  Solve Sudoku", width=24, height=2,
            bg="#1E88E5", fg="white", activebackground="#1976D2",
            activeforeground="white", relief="flat",
            font=("Segoe UI", 13, "bold"),
            command=lambda: controller.show_frame("solver")
        )
        solve_button.pack(pady=12)

        for button in (play_button, solve_button):
            button.bind("<Enter>", lambda e: e.widget.config(cursor="hand2"))

        footer = tk.Label(
            self, text="A polished desktop Sudoku experience",
            bg="#1E1E1E", fg="#555555", font=("Segoe UI", 9)
        )
        footer.pack(side="bottom", pady=25)

    def on_show(self):
        pass


class SolverFrame(tk.Frame):
    """Solver mode - manual entry + animated backtracking solve."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1E1E1E")
        self.controller = controller
        self.cells = []
        self.solving = False
        self.solver = None
        self.gen = None
        self.start_time = None

        validate = self.register(self.validate_input)
        self.validate = validate

        self.build_ui()

    def on_show(self):
        pass

    def build_ui(self):
        top = tk.Frame(self, bg="#1E1E1E")
        top.pack(fill="x", pady=(15, 0), padx=15)

        back_button = tk.Button(
            top, text="← Menu", bg="#333333", fg="white", relief="flat",
            font=("Segoe UI", 10, "bold"),
            command=lambda: self.controller.show_frame("menu")
        )
        back_button.pack(side="left")
        back_button.bind("<Enter>", lambda e: e.widget.config(cursor="hand2"))

        title = tk.Label(
            top, text="Solve Sudoku", bg="#1E1E1E", fg="white",
            font=("Segoe UI", 16, "bold")
        )
        title.pack(side="left", padx=20)

        self.create_grid()

        self.timer_label = tk.Label(
            self, text="", bg="#1E1E1E", fg="#4CAF50", font=("Segoe UI", 12, "bold")
        )
        self.timer_label.pack(pady=10)

    def create_grid(self):
        board = tk.Frame(self, bg="#1E1E1E")
        board.pack(pady=20)

        self.cells = []

        for row in range(9):
            current_row = []

            for col in range(9):
                box_index = (row // 3) * 3 + (col // 3)
                bg_color = BOX_COLORS[box_index % 2]

                cell = tk.Entry(
                    board, width=3, font=("Segoe UI", 20, "bold"),
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

                current_row.append(cell)

            self.cells.append(current_row)

        button_frame = tk.Frame(self, bg="#1E1E1E")
        button_frame.pack(pady=15)

        self.solve_button = tk.Button(
            button_frame, text="Solve", width=12, bg="#4CAF50", fg="white",
            activebackground="#45A049", activeforeground="white", relief="flat",
            font=("Segoe UI", 11, "bold"), command=self.solve
        )
        self.solve_button.grid(row=0, column=0, padx=10)

        self.clear_button = tk.Button(
            button_frame, text="Clear", width=12, bg="#E53935", fg="white",
            activebackground="#D32F2F", activeforeground="white", relief="flat",
            font=("Segoe UI", 11, "bold"), command=self.clear
        )
        self.clear_button.grid(row=0, column=1, padx=10)

        self.example_button = tk.Button(
            button_frame, text="Example", width=12, bg="#1E88E5", fg="white",
            activebackground="#1976D2", activeforeground="white", relief="flat",
            font=("Segoe UI", 11, "bold"), command=self.load_example
        )
        self.example_button.grid(row=0, column=2, padx=10)

        for button in (self.solve_button, self.clear_button, self.example_button):
            button.bind("<Enter>", self.on_enter)
            button.bind("<Leave>", self.on_leave)

    # ---------- board <-> grid helpers ----------

    def get_board(self):
        board = []
        for row in self.cells:
            current_row = []
            for cell in row:
                value = cell.get()
                current_row.append(int(value) if value != "" else 0)
            board.append(current_row)
        return board

    def display_board(self, board):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].delete(0, tk.END)
                if board[row][col] != 0:
                    self.cells[row][col].insert(0, str(board[row][col]))

    def reset_cell_color(self, row, col):
        box_index = (row // 3) * 3 + (col // 3)
        self.cells[row][col].config(bg=BOX_COLORS[box_index % 2], fg="white")

    # ---------- solving ----------

    def solve(self):
        if self.solving:
            return

        board = self.get_board()
        self.solver = SudokuSolver(board)

        if self.solver.find_empty() is None:
            messagebox.showinfo("Already Solved", "This board has no empty cells.")
            return

        self.solving = True
        self.set_controls_state("disabled")
        self.gen = self.solver.solve_animated()
        self.start_time = time.perf_counter()
        self.timer_label.config(text="Solving...")
        self.after(1, self.animate_step)

    def animate_step(self):
        try:
            # Process several algorithm steps per animation tick so the
            # visualization stays fast even on puzzles with many backtracks.
            for _ in range(6):
                action, row, col, value = next(self.gen)

                if action == "try":
                    self.cells[row][col].delete(0, tk.END)
                    self.cells[row][col].insert(0, str(value))
                    self.cells[row][col].config(bg=TRY_COLOR, fg="black")
                elif action == "place":
                    self.cells[row][col].config(bg=PLACE_COLOR, fg="white")
                elif action == "backtrack":
                    self.cells[row][col].delete(0, tk.END)
                    self.cells[row][col].config(bg=BACKTRACK_COLOR, fg="white")
                    self.after(50, lambda r=row, c=col: self.reset_cell_color(r, c))

            self.after(1, self.animate_step)

        except StopIteration as stop:
            solved = bool(stop.value)
            self.finish_solve(solved)

    def finish_solve(self, solved):
        self.solving = False
        self.set_controls_state("normal")
        elapsed = time.perf_counter() - self.start_time

        if solved:
            for row in range(9):
                for col in range(9):
                    self.reset_cell_color(row, col)
            self.timer_label.config(text=f"Solved in {elapsed:.2f} seconds")
        else:
            self.timer_label.config(text="")
            messagebox.showerror(
                "No Solution", "No solution exists for the given Sudoku puzzle."
            )

    def set_controls_state(self, state):
        for button in (self.solve_button, self.clear_button, self.example_button):
            button.config(state=state)

    # ---------- misc ----------

    def clear(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].delete(0, tk.END)
                self.reset_cell_color(row, col)
        self.timer_label.config(text="")

    def validate_input(self, value):
        if value == "":
            return True
        return value in "123456789" and len(value) == 1

    def on_enter(self, event):
        event.widget.config(cursor="hand2")

    def on_leave(self, event):
        event.widget.config(cursor="")

    def load_example(self):
        example = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
        self.clear()
        self.display_board(example)