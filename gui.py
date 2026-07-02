import tkinter as tk
from tkinter import messagebox
from solver import SudokuSolver
import time

class SudokuGUI:

    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Sudoku Solver")
        self.root.geometry("650x750")
        self.root.configure(bg="#1E1E1E")
        self.root.resizable(False, False)
        self.center_window()

        validate = self.root.register(self.validate_input)
        self.validate = validate

        self.cells = []
        self.create_grid()

        self.timer_label = tk.Label(
            self.root,
            text="",
            bg="#1E1E1E",
            fg="white",
            font=("Arial", 12)
        )

        self.timer_label.pack(pady=10) 


    def center_window(self):

        self.root.update_idletasks()

        width = 650
        height = 750

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_grid(self):

        board = tk.Frame(
            self.root,
            bg="#1E1E1E"
        )

        board.pack(pady=30)

        for row in range(9):

            current_row = []

            for col in range(9):

                cell = tk.Entry(
                    board,
                    width=3,
                    font=("Segoe UI", 20, "bold"),
                    justify="center",
                    bg="#2B2B2B",
                    fg="white",
                    insertbackground="white",
                    relief="flat",
                    bd=0,
                    highlightthickness=1,
                    highlightbackground="#555555",
                    highlightcolor="#4CAF50",
                    validate="key",
                    validatecommand=(self.validate, "%P")
                )

                cell.grid(
                    row=row,
                    column=col,
                    padx=(4 if col % 3 == 0 else 1),
                    pady=(4 if row % 3 == 0 else 1),
                    ipadx=4,
                    ipady=6
                )

                current_row.append(cell)

            self.cells.append(current_row)

        button_frame = tk.Frame(
            self.root,
            bg="#1E1E1E"
        )

        button_frame.pack(pady=20)

        solve_button = tk.Button(
            button_frame,
            text="Solve",
            width=12,
            bg="#4CAF50",
            fg="white",
            activebackground="#45A049",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            command=self.solve
        )
        solve_button.bind("<Enter>", self.on_enter)
        solve_button.bind("<Leave>", self.on_leave)
        solve_button.grid(row=0, column=0, padx=10)

        clear_button = tk.Button(
            button_frame,
            text="Clear",
            width=12,
            bg="#E53935",
            fg="white",
            activebackground="#D32F2F",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            command=self.clear
        )
        clear_button.bind("<Enter>", self.on_enter)
        clear_button.bind("<Leave>", self.on_leave)
        clear_button.grid(row=0, column=1, padx=10)

        example_button = tk.Button(
            button_frame,
            text="Example",
            width=12,
            bg="#1E88E5",
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            command=self.load_example
        )
        example_button.bind("<Enter>", self.on_enter)
        example_button.bind("<Leave>", self.on_leave)
        example_button.grid(row=0, column=2, padx=10)

        print(len(self.cells))
    
    def get_board(self):

        board = []

        for row in self.cells:

            current_row = []

            for cell in row:

                value = cell.get()

                if value == "":
                    current_row.append(0)
                else:
                    try:
                        current_row.append(int(value))
                    except ValueError:
                        current_row.append(0)

            board.append(current_row)

        return board
    
    def display_board(self, board):

        for row in range(9):
            for col in range(9):

                self.cells[row][col].delete(0, tk.END)

                if board[row][col] != 0:
                    self.cells[row][col].insert(0, str(board[row][col]))
        
    def solve(self):
        start_time = time.perf_counter()

        board = self.get_board()

        solver = SudokuSolver(board)

        if solver.solve():
            self.display_board(board)
        else:
            messagebox.showerror(
                "No Solution",
                "No solution exists for the given Sudoku puzzle."
            )

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        self.timer_label.config(
            text=f"Elapsed time: {elapsed_time:.4f} seconds"
        )


    def clear(self):
        for row in self.cells:
            for cell in row:
                cell.delete(0, tk.END)

    def validate_input(self, value):
        if value == "":
            return True

        if value in "123456789" and len(value) == 1:
            return True

        return False
    
    def on_enter(self, event):
        event.widget.config(cursor="hand2")


    def on_leave(self, event):
        event.widget.config(cursor="")


    def load_example(self):
        example = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
        ]

        self.display_board(example)