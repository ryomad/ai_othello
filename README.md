# AI Othello

A simple Othello (Reversi) game built with Python and Pygame. You can play against a basic AI opponent.

## Features

- Graphical user interface using Pygame.
- Play as Black against a computer-controlled White player.
- The AI selects a random valid move.
- Score tracking and game-over detection.
- Automatic pass-turn logic.

## Requirements

- Python 3
- `pygame`
- `numpy`

## Installation

1.  Clone the repository to your local machine.

2.  Install the required packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

## How to Play

Run the main script from your terminal:

```bash
python ai_othello.py
```

The game window will open. You play as Black ('X'). Click on a valid square to make your move. The AI (White, 'O') will automatically make its move after yours. The game ends when neither player can make a move, and the winner will be displayed.