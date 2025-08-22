import pygame
import numpy as np
import random
import time

# --- Constants ---
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
GREEN = (34, 139, 34)  # Board background color
WHITE = (255, 255, 255) # White piece color
BLACK = (0, 0, 0)      # Black piece color
LINE_COLOR = (0, 0, 0) # Grid line color

class GameState:
    """
    Manages the internal state of the Othello game.
    """
    def __init__(self):
        """Initializes the game state."""
        self.board = np.full((GRID_SIZE, GRID_SIZE), ' ')
        self.board[3, 3], self.board[4, 4] = 'O', 'O'  # White
        self.board[3, 4], self.board[4, 3] = 'X', 'X'  # Black
        self.current_player = 'X'  # Black starts
        self.game_over = False

    def is_valid_move(self, row, col, player):
        """Checks if a move is valid for the given player."""
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and self.board[row, col] == ' '):
            return False

        opponent = 'O' if player == 'X' else 'X'
        
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            r, c = row + dr, col + dc
            # Check if there is an opponent's stone in the adjacent cell
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r, c] == opponent:
                # Move further in this direction
                r, c = r + dr, c + dc
                while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    if self.board[r, c] == ' ':
                        break  # No friendly stone found, invalid direction
                    if self.board[r, c] == player:
                        return True  # Found a friendly stone, the move is valid
                    r, c = r + dr, c + dc
        return False

    def get_valid_moves(self, player):
        """Gets all valid moves for the given player."""
        valid_moves = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.is_valid_move(r, c, player):
                    valid_moves.append((r, c))
        return valid_moves

    def flip_stones(self, row, col, player):
        """Flips the opponent's stones."""
        opponent = 'O' if player == 'X' else 'X'
        
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            stones_to_flip = []
            r, c = row + dr, col + dc

            # Find a line of opponent's stones
            while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r, c] == opponent:
                stones_to_flip.append((r, c))
                r += dr
                c += dc

            # If the line ends with the player's stone, flip the stones in between
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r, c] == player:
                for r_flip, c_flip in stones_to_flip:
                    self.board[r_flip, c_flip] = player

    def make_move(self, row, col):
        """Makes a move on the board and switches player."""
        if not self.is_valid_move(row, col, self.current_player):
            return False
        
        self.board[row, col] = self.current_player
        self.flip_stones(row, col, self.current_player)
        self.switch_player()
        return True

    def switch_player(self):
        """Switches the current player."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_for_game_over(self):
        """Checks if the game has ended."""
        # If the current player has no valid moves
        if not self.get_valid_moves(self.current_player):
            opponent = 'O' if self.current_player == 'X' else 'X'
            # If the opponent also has no valid moves, the game is over.
            if not self.get_valid_moves(opponent):
                self.game_over = True
            else:
                # Otherwise, pass the turn to the opponent.
                self.switch_player()
    
    def get_score(self):
        """Calculates and returns the score."""
        score_X = np.sum(self.board == 'X')
        score_O = np.sum(self.board == 'O')
        return score_X, score_O

    def get_winner(self):
        """Determines the winner of the game."""
        score_X, score_O = self.get_score()
        if score_X > score_O:
            return "Black (X)"
        elif score_O > score_X:
            return "White (O)"
        else:
            return "Draw"

class OthelloGUI:
    """
    Manages the graphical user interface for the Othello game.
    """
    def __init__(self):
        """Initializes the GUI."""
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + 50)) # Extra space for text
        pygame.display.set_caption("Othello")
        self.game_state = GameState()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.ai_opponent = True  # Enable AI opponent
        self.ai_player = 'O'     # AI plays as White

    def draw_board(self):
        """Draws the Othello board, pieces, and game information."""
        self.screen.fill(GREEN)

        # Draw grid lines
        for i in range(1, GRID_SIZE):
            pygame.draw.line(self.screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)

        # Draw pieces
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.game_state.board[r, c] == 'X':
                    pygame.draw.circle(self.screen, BLACK, (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
                elif self.game_state.board[r, c] == 'O':
                    pygame.draw.circle(self.screen, WHITE, (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

        # Draw score and turn information
        score_X, score_O = self.game_state.get_score()
        score_text = f"Black (X): {score_X}  White (O): {score_O}"
        score_surface = self.font.render(score_text, True, BLACK)
        self.screen.blit(score_surface, (10, HEIGHT + 10))

        turn_text = f"Turn: {'Black (X)' if self.game_state.current_player == 'X' else 'White (O)'}"
        turn_surface = self.font.render(turn_text, True, BLACK)
        self.screen.blit(turn_surface, (WIDTH - 180, HEIGHT + 10))

        # Draw game over message if applicable
        if self.game_state.game_over:
            winner_text = f"Game Over! Winner: {self.game_state.get_winner()}"
            winner_surface = self.font.render(winner_text, True, (200, 0, 0))
            winner_rect = winner_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            self.screen.blit(winner_surface, winner_rect)

        pygame.display.flip()

    def handle_click(self, pos):
        """Handles a mouse click event."""
        if self.game_state.game_over:
            return

        col, row = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            if self.game_state.make_move(row, col):
                self.game_state.check_for_game_over()
                self.draw_board()

    def run(self):
        """The main game loop."""
        while self.running:
            # Handle AI turn
            if self.ai_opponent and self.game_state.current_player == self.ai_player and not self.game_state.game_over:
                pygame.time.wait(500)  # Pause for half a second to make AI move visible
                valid_moves = self.game_state.get_valid_moves(self.game_state.current_player)
                if valid_moves:
                    move = random.choice(valid_moves)
                    self.game_state.make_move(move[0], move[1])
                    self.game_state.check_for_game_over()

            self.draw_board()

            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_state.game_over:
                    # Only allow clicks if it's not the AI's turn
                    if not (self.ai_opponent and self.game_state.current_player == self.ai_player):
                        self.handle_click(event.pos)

            # Check for passes or game over condition
            if not self.game_state.game_over:
                self.game_state.check_for_game_over()

        pygame.quit()

if __name__ == "__main__":
    game_gui = OthelloGUI()
    game_gui.run()
