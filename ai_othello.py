import pygame
import numpy as np
import random
import time

# --- 定数 ---
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
GREEN = (34, 139, 34)  # ボードの背景色
WHITE = (255, 255, 255) # 白石の色
BLACK = (0, 0, 0)      # 黒石の色
LINE_COLOR = (0, 0, 0) # 罫線の色

class GameState:
    """
    オセロゲームの内部状態を管理します。
    """
    def __init__(self):
        """ゲーム状態を初期化します。"""
        self.board = np.full((GRID_SIZE, GRID_SIZE), ' ')
        self.board[3, 3], self.board[4, 4] = 'O', 'O'  # 白
        self.board[3, 4], self.board[4, 3] = 'X', 'X'  # 黒
        self.current_player = 'X'  # 黒から開始
        self.game_over = False

    def is_valid_move(self, row, col, player):
        """指定された手番のプレイヤーにとって、その手が有効かどうかを判定します。"""
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and self.board[row, col] == ' '):
            return False

        opponent = 'O' if player == 'X' else 'X'
        
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            r, c = row + dr, col + dc
            # 隣接するマスに相手の石があるか確認
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r, c] == opponent:
                # その方向にさらに進む
                r, c = r + dr, c + dc
                while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    if self.board[r, c] == ' ':
                        break  # 自分の石が見つからなかったので、この方向は無効
                    if self.board[r, c] == player:
                        return True  # 自分の石が見つかったので、この手は有効
                    r, c = r + dr, c + dc
        return False

    def get_valid_moves(self, player):
        """指定されたプレイヤーの全ての有効な手を取得します。"""
        valid_moves = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.is_valid_move(r, c, player):
                    valid_moves.append((r, c))
        return valid_moves

    def flip_stones(self, row, col, player):
        """相手の石をひっくり返します。"""
        opponent = 'O' if player == 'X' else 'X'
        
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            stones_to_flip = []
            r, c = row + dr, col + dc

            # 相手の石の列を探す
            while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r, c] == opponent:
                stones_to_flip.append((r, c))
                r += dr
                c += dc

            # 列の終点が自分の石であれば、間の石をひっくり返す
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r, c] == player:
                for r_flip, c_flip in stones_to_flip:
                    self.board[r_flip, c_flip] = player

    def make_move(self, row, col):
        """盤面に石を置き、プレイヤーを交代します。"""
        if not self.is_valid_move(row, col, self.current_player):
            return False
        
        self.board[row, col] = self.current_player
        self.flip_stones(row, col, self.current_player)
        self.switch_player()
        return True

    def switch_player(self):
        """現在のプレイヤーを交代します。"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_for_game_over(self):
        """ゲームが終了したかどうかをチェックします。"""
        # 現在のプレイヤーに有効な手がない場合
        if not self.get_valid_moves(self.current_player):
            opponent = 'O' if self.current_player == 'X' else 'X'
            # 相手プレイヤーにも有効な手がない場合、ゲーム終了
            if not self.get_valid_moves(opponent):
                self.game_over = True
            else:
                # そうでなければ、相手にターンを渡す（パス）
                self.switch_player()
    
    def get_score(self):
        """スコアを計算して返します。"""
        score_X = np.sum(self.board == 'X')
        score_O = np.sum(self.board == 'O')
        return score_X, score_O

    def get_winner(self):
        """ゲームの勝者を判定します。"""
        score_X, score_O = self.get_score()
        if score_X > score_O:
            return "黒 (X)"
        elif score_O > score_X:
            return "白 (O)"
        else:
            return "引き分け"

class OthelloGUI:
    """
    オセロゲームのグラフィカルユーザーインターフェースを管理します。
    """
    def __init__(self):
        """GUIを初期化します。"""
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + 50)) # テキスト表示用の追加スペース
        pygame.display.set_caption("オセロ")
        self.game_state = GameState()
        self.running = True
        # 日本語表示に対応したフォントを、カンマ区切りで優先順位順に指定
        jp_font_names = "ipaexg, ipaexgothic, ipagothic, ms-gothic, meiryo, sans-serif"
        self.font = pygame.font.SysFont(jp_font_names, 24)
        self.small_font = pygame.font.SysFont(jp_font_names, 18)
        self.ai_opponent = True  # AI対戦相手を有効にする
        self.ai_player = 'O'     # AIは白石を担当

    def draw_board(self):
        """オセロの盤面、石、およびゲーム情報を描画します。"""
        self.screen.fill(GREEN)

        # 罫線を描画
        for i in range(1, GRID_SIZE):
            pygame.draw.line(self.screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)

        # 石を描画
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.game_state.board[r, c] == 'X':
                    pygame.draw.circle(self.screen, BLACK, (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
                elif self.game_state.board[r, c] == 'O':
                    pygame.draw.circle(self.screen, WHITE, (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

        # スコアと手番情報を描画
        score_X, score_O = self.game_state.get_score()
        score_text = f"黒 (X): {score_X}  白 (O): {score_O}"
        score_surface = self.font.render(score_text, True, BLACK)
        self.screen.blit(score_surface, (10, HEIGHT + 10))

        turn_text = f"手番: {'黒 (X)' if self.game_state.current_player == 'X' else '白 (O)'}"
        turn_surface = self.font.render(turn_text, True, BLACK)
        self.screen.blit(turn_surface, (WIDTH - 180, HEIGHT + 10))

        # ゲーム終了時にはメッセージを描画
        if self.game_state.game_over:
            winner_text = f"ゲーム終了！ 勝者: {self.game_state.get_winner()}"
            winner_surface = self.font.render(winner_text, True, (200, 0, 0))
            winner_rect = winner_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            self.screen.blit(winner_surface, winner_rect)

        pygame.display.flip()

    def handle_click(self, pos):
        """マウスクリックイベントを処理します。"""
        if self.game_state.game_over:
            return

        col, row = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            if self.game_state.make_move(row, col):
                self.game_state.check_for_game_over()
                self.draw_board()

    def run(self):
        """メインのゲームループ。"""
        while self.running:
            # AIのターンを処理
            if self.ai_opponent and self.game_state.current_player == self.ai_player and not self.game_state.game_over:
                pygame.time.wait(500)  # AIの手が視認できるように0.5秒待機
                valid_moves = self.game_state.get_valid_moves(self.game_state.current_player)
                if valid_moves:
                    move = random.choice(valid_moves)
                    self.game_state.make_move(move[0], move[1])
                    self.game_state.check_for_game_over()

            self.draw_board()

            # イベントをチェック
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_state.game_over:
                    # AIのターンでなければクリックを許可
                    if not (self.ai_opponent and self.game_state.current_player == self.ai_player):
                        self.handle_click(event.pos)

            # パスやゲーム終了の条件をチェック
            if not self.game_state.game_over:
                self.game_state.check_for_game_over()

        pygame.quit()

if __name__ == "__main__":
    game_gui = OthelloGUI()
    game_gui.run()
