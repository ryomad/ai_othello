import unittest
import numpy as np
from ai_othello import GameState

class TestGameState(unittest.TestCase):

    def setUp(self):
        """Set up a new GameState object for each test."""
        self.game_state = GameState()

    def test_initial_board(self):
        """Test the initial setup of the game board."""
        self.assertEqual(self.game_state.board.shape, (8, 8))
        self.assertEqual(self.game_state.board[3, 3], 'O')
        self.assertEqual(self.game_state.board[4, 4], 'O')
        self.assertEqual(self.game_state.board[3, 4], 'X')
        self.assertEqual(self.game_state.board[4, 3], 'X')
        self.assertEqual(np.sum(self.game_state.board != ' '), 4)
        self.assertEqual(self.game_state.current_player, 'X')
        self.assertFalse(self.game_state.game_over)

    def test_is_valid_move(self):
        """Test the move validation logic."""
        # Valid moves for 'X' at the start
        self.assertTrue(self.game_state.is_valid_move(2, 3, 'X'))
        self.assertTrue(self.game_state.is_valid_move(3, 2, 'X'))
        self.assertTrue(self.game_state.is_valid_move(4, 5, 'X'))
        self.assertTrue(self.game_state.is_valid_move(5, 4, 'X'))

        # Invalid move on an occupied cell
        self.assertFalse(self.game_state.is_valid_move(3, 3, 'X'))

        # Invalid move on an empty cell that doesn't flip anything
        self.assertFalse(self.game_state.is_valid_move(0, 0, 'X'))

    def test_make_move(self):
        """Test making a move."""
        self.game_state.make_move(2, 3)
        self.assertEqual(self.game_state.board[2, 3], 'X') # New piece
        self.assertEqual(self.game_state.board[3, 3], 'X') # Flipped piece
        self.assertEqual(self.game_state.current_player, 'O') # Player switched

    def test_switch_player(self):
        """Test the player switching logic."""
        self.game_state.switch_player()
        self.assertEqual(self.game_state.current_player, 'O')
        self.game_state.switch_player()
        self.assertEqual(self.game_state.current_player, 'X')

    def test_pass_turn(self):
        """Test if a turn is passed when no moves are available."""
        # Create a simple board state where 'X' has no moves but 'O' does.
        self.game_state.board = np.full((8, 8), 'O') # Board is all 'O'
        self.game_state.board[1, 1] = 'X'           # One 'X' piece
        self.game_state.board[0, 0] = ' '           # One empty square
        self.game_state.current_player = 'X'

        # Verify that 'X' has no valid moves.
        self.assertEqual(len(self.game_state.get_valid_moves('X')), 0)

        # Verify that 'O' has a valid move at (0,0).
        # This is because it can flank the 'X' at (1,1) with an existing 'O' at (2,2).
        self.assertTrue(self.game_state.is_valid_move(0, 0, 'O'))

        # Run the check logic. Since it's X's turn and X has no moves,
        # the turn should be passed to 'O'.
        self.game_state.check_for_game_over()
        self.assertEqual(self.game_state.current_player, 'O')
        self.assertFalse(self.game_state.game_over)

    def test_game_over(self):
        """Test the game over condition."""
        # Create a state where neither player has moves (e.g., full board)
        self.game_state.board = np.full((8, 8), 'X')
        self.game_state.board[0, 0] = 'O'
        self.game_state.current_player = 'X'

        self.assertEqual(len(self.game_state.get_valid_moves('X')), 0)
        self.assertEqual(len(self.game_state.get_valid_moves('O')), 0)

        self.game_state.check_for_game_over()
        self.assertTrue(self.game_state.game_over)

    def test_get_winner(self):
        """Test the winner detection logic."""
        self.game_state.board = np.full((8, 8), 'X')
        self.assertEqual(self.game_state.get_winner(), "Black (X)")

        self.game_state.board = np.full((8, 8), 'O')
        self.assertEqual(self.game_state.get_winner(), "White (O)")

        # Draw
        self.game_state.board = np.full((8, 8), 'X')
        # Set half the board to 'O'
        for i in range(32):
            self.game_state.board.flat[i] = 'O'
        self.assertEqual(self.game_state.get_winner(), "Draw")

if __name__ == '__main__':
    unittest.main()
