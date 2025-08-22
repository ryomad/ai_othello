import unittest
import numpy as np
from ai_othello import GameState

class TestGameState(unittest.TestCase):

    def setUp(self):
        """各テストの前に新しいGameStateオブジェクトをセットアップします。"""
        self.game_state = GameState()

    def test_initial_board(self):
        """ゲームボードの初期設定をテストします。"""
        self.assertEqual(self.game_state.board.shape, (8, 8))
        self.assertEqual(self.game_state.board[3, 3], 'O')
        self.assertEqual(self.game_state.board[4, 4], 'O')
        self.assertEqual(self.game_state.board[3, 4], 'X')
        self.assertEqual(self.game_state.board[4, 3], 'X')
        self.assertEqual(np.sum(self.game_state.board != ' '), 4)
        self.assertEqual(self.game_state.current_player, 'X')
        self.assertFalse(self.game_state.game_over)

    def test_is_valid_move(self):
        """手の検証ロジックをテストします。"""
        # 開始時の'X'の有効な手
        self.assertTrue(self.game_state.is_valid_move(2, 3, 'X'))
        self.assertTrue(self.game_state.is_valid_move(3, 2, 'X'))
        self.assertTrue(self.game_state.is_valid_move(4, 5, 'X'))
        self.assertTrue(self.game_state.is_valid_move(5, 4, 'X'))

        # 石が既に置かれているセルへの無効な手
        self.assertFalse(self.game_state.is_valid_move(3, 3, 'X'))

        # 何もひっくり返せない空のセルへの無効な手
        self.assertFalse(self.game_state.is_valid_move(0, 0, 'X'))

    def test_make_move(self):
        """着手処理をテストします。"""
        self.game_state.make_move(2, 3)
        self.assertEqual(self.game_state.board[2, 3], 'X') # 新しい石
        self.assertEqual(self.game_state.board[3, 3], 'X') # ひっくり返された石
        self.assertEqual(self.game_state.current_player, 'O') # プレイヤー交代

    def test_switch_player(self):
        """プレイヤー交代のロジックをテストします。"""
        self.game_state.switch_player()
        self.assertEqual(self.game_state.current_player, 'O')
        self.game_state.switch_player()
        self.assertEqual(self.game_state.current_player, 'X')

    def test_pass_turn(self):
        """有効な手がない場合にターンがパスされるかをテストします。"""
        # 'X'には手がなく、'O'には手がある簡単な盤面を作成
        self.game_state.board = np.full((8, 8), 'O') # 盤面はすべて'O'
        self.game_state.board[1, 1] = 'X'           # 'X'の石を1つ
        self.game_state.board[0, 0] = ' '           # 空きマスを1つ
        self.game_state.current_player = 'X'

        # 'X'に有効な手がないことを確認
        self.assertEqual(len(self.game_state.get_valid_moves('X')), 0)

        # 'O'が(0,0)に有効な手を持つことを確認
        # (2,2)の'O'で(1,1)の'X'を挟めるため
        self.assertTrue(self.game_state.is_valid_move(0, 0, 'O'))

        # チェックロジックを実行。Xのターンで手がないため、'O'にターンが渡されるはず
        self.game_state.check_for_game_over()
        self.assertEqual(self.game_state.current_player, 'O')
        self.assertFalse(self.game_state.game_over)

    def test_game_over(self):
        """ゲーム終了条件をテストします。"""
        # どちらのプレイヤーも手がない状態を作成（例：盤面が埋まっている）
        self.game_state.board = np.full((8, 8), 'X')
        self.game_state.board[0, 0] = 'O'
        self.game_state.current_player = 'X'

        self.assertEqual(len(self.game_state.get_valid_moves('X')), 0)
        self.assertEqual(len(self.game_state.get_valid_moves('O')), 0)

        self.game_state.check_for_game_over()
        self.assertTrue(self.game_state.game_over)

    def test_get_winner(self):
        """勝者判定ロジックをテストします。"""
        self.game_state.board = np.full((8, 8), 'X')
        self.assertEqual(self.game_state.get_winner(), "黒 (X)")

        self.game_state.board = np.full((8, 8), 'O')
        self.assertEqual(self.game_state.get_winner(), "白 (O)")

        # 引き分け
        self.game_state.board = np.full((8, 8), 'X')
        # 盤面の半分を'O'に設定
        for i in range(32):
            self.game_state.board.flat[i] = 'O'
        self.assertEqual(self.game_state.get_winner(), "引き分け")

if __name__ == '__main__':
    unittest.main()
