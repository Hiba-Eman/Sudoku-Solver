# 🧩 Sudoku Suite

A Sudoku app for your computer, made with Python. You can either **play** Sudoku or have the computer **solve** a puzzle for you.

## What can it do?

### 🎮 Play Sudoku
- The app creates a brand new puzzle for you every time.
- Choose how hard you want it: **Easy**, **Medium**, or **Hard**.
- The starting numbers (clues) are locked so you can't accidentally change them.
- You get **3 chances**. If you type a wrong number, it turns red and counts as a mistake. Make 3 mistakes and it's game over — just hit **New Game** to try again.
- A timer keeps track of how long you take.
- Finish the puzzle correctly and you'll get a "You Win!" message with your time.
- There's also a **Check** button if you want to see which cells are wrong at any point.

### 🤖 Solve Sudoku
- Type in any Sudoku puzzle yourself (or click **Example** to load one).
- Click **Solve** and the app instantly fills in the answer.
- It also shows you how long it took to solve.

## How to run it

You need Python installed on your computer (Python 3). No extra downloads or setup needed — the app only uses tools that already come with Python.

1. Download or clone this project.
2. Open a terminal in the project folder.
3. Run this command:

```bash
python main.py
```

That's it — the app window will open.

## What's inside the project

| File | What it does |
|---|---|
| `main.py` | Starts the app and switches between screens |
| `gui.py` | The main menu and the "Solve" screen |
| `game.py` | The "Play" screen (the game itself) |
| `solver.py` | The logic that solves a Sudoku puzzle |
| `generator.py` | Creates new random puzzles |

## Built with

- Python 3
- Tkinter (comes built into Python — no need to install anything extra)

## Ideas for the future

- Puzzles that are guaranteed to have only one correct answer
- A hint button
- Saving your best times

## License

This project is free to use under the MIT License — see the `LICENSE` file for details.
