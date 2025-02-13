import pygame
import numpy as np

# 定数設定
WIDTH, HEIGHT = 600, 600  # ウィンドウの幅と高さ
GRID_SIZE = 8  # オセロ盤のマス目の数
CELL_SIZE = WIDTH // GRID_SIZE  # 各マスのサイズ
GREEN = (34, 139, 34)  # ボードの背景色（緑）
WHITE = (255, 255, 255)  # 白石の色
BLACK = (0, 0, 0)  # 黒石の色
LINE_COLOR = (0, 0, 0)  # マス目の線の色

class Othello:
    def __init__(self):
        """ゲームの初期化処理を行う"""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # ゲームウィンドウを作成
        pygame.display.set_caption("Othello")  # ウィンドウのタイトルを設定
        
        # オセロの初期盤面を設定
        self.board = np.full((GRID_SIZE, GRID_SIZE), ' ')
        self.board[3, 3], self.board[4, 4] = 'O', 'O'
        self.board[3, 4], self.board[4, 3] = 'X', 'X'
        self.current_player = 'X'  # 最初のプレイヤーは黒
        self.running = True  # ゲームループのフラグ
    
    def draw_board(self):
        """オセロ盤と駒を描画する"""
        self.screen.fill(GREEN)  # 背景を緑色にする
        
        # マス目の線を描画
        for i in range(1, GRID_SIZE):
            pygame.draw.line(self.screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
        
        # 石を描画
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r, c] == 'X':
                    pygame.draw.circle(self.screen, BLACK, (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
                elif self.board[r, c] == 'O':
                    pygame.draw.circle(self.screen, WHITE, (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
        
        pygame.display.flip()  # 画面を更新
    
    def is_valid_move(self, row, col):
        """指定された位置が有効な手かを判定する"""
        if self.board[row, col] != ' ':
            return False  # 既に石がある場合は無効
        
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        opponent = 'O' if self.current_player == 'X' else 'X'
        valid = False
        
        # 8方向に駒をひっくり返せるか確認
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r, c] == opponent:
                while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    r += dr
                    c += dc
                    if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
                        break
                    if self.board[r, c] == ' ':
                        break
                    if self.board[r, c] == self.current_player:
                        valid = True
                        break
        return valid
    
    def flip_stones(self, row, col):
        """駒をひっくり返す処理"""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        opponent = 'O' if self.current_player == 'X' else 'X'
        
        for dr, dc in directions:
            stones_to_flip = []
            r, c = row + dr, col + dc
            while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r, c] == opponent:
                stones_to_flip.append((r, c))
                r += dr
                c += dc
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r, c] == self.current_player:
                for rr, cc in stones_to_flip:
                    self.board[rr, cc] = self.current_player
    
    def make_move(self, row, col):
        """駒を置き、ひっくり返し、手番を交代する"""
        if not self.is_valid_move(row, col):
            return False  # 無効な手なら何もしない
        
        self.board[row, col] = self.current_player  # 駒を置く
        self.flip_stones(row, col)  # 駒をひっくり返す
        self.current_player = 'O' if self.current_player == 'X' else 'X'  # 手番を交代
        return True
    
    def handle_click(self, pos):
        """マウスクリック時に処理を行う"""
        col, row = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
        if self.make_move(row, col):
            self.draw_board()  # 画面を更新
    
    def run(self):
        """ゲームのメインループ"""
        while self.running:
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False  # ゲーム終了
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)  # クリックされた場所に駒を置く
        pygame.quit()

if __name__ == "__main__":
    game = Othello()
    game.run()

