import tkinter as tk

from gui import MainMenuFrame, SolverFrame
from game import GameFrame


class SudokuSuiteApp(tk.Tk):
    """Root window that hosts and switches between the app's pages."""

    WIDTH = 650
    HEIGHT = 800

    def __init__(self):
        super().__init__()

        self.title("Sudoku Suite")
        self.configure(bg="#1E1E1E")
        self.resizable(False, False)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.center_window()

        container = tk.Frame(self, bg="#1E1E1E")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for name, FrameClass in (
            ("menu", MainMenuFrame),
            ("solver", SolverFrame),
            ("game", GameFrame),
        ):
            frame = FrameClass(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("menu")

    def center_window(self):
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (self.WIDTH // 2)
        y = (screen_height // 2) - (self.HEIGHT // 2)

        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

        if hasattr(frame, "on_show"):
            frame.on_show()


if __name__ == "__main__":
    app = SudokuSuiteApp()
    app.mainloop()