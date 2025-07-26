import sys
from math import cos, sin, pi, radians
import random
import pygame
from pygame import gfxdraw
from pygame import time

class UI:
    def __init__(self, board_size: int):
        self.board_size = board_size
        assert 1 < self.board_size <= 26

        self.clock = time.Clock()
        self.hex_radius = 20
        self.x_offset, self.y_offset = 60, 60
        self.text_offset = 45
        self.screen = pygame.display.set_mode(
            (self.x_offset + (2 * self.hex_radius) * self.board_size + self.hex_radius * self.board_size,
             round(self.y_offset + (1.75 * self.hex_radius) * self.board_size)))
        pygame.display.set_caption("hex")
        # 加载并设置窗口图标
        icon = pygame.image.load("hexhex.png")  # 替换为你的图标文件路径
        pygame.display.set_icon(icon)
        # Colors
        self.red = (222, 29, 47)
        self.blue = (0, 121, 251)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)
        self.black = (40, 40, 40)
        self.gray = (70, 70, 70)
        self.bg = (249, 224, 167)

        # Players
        self.BLACK_PLAYER = 1
        self.WHITE_PLAYER = 2

        self.screen.fill(self.gray)
        self.fonts = pygame.font.SysFont("Sans", 20)

        self.hex_lookup = {}
        self.rects, self.color, self.node = [], [self.bg] * (self.board_size ** 2), None
        self.board_state = [None] * (self.board_size ** 2)  # None means empty, 1 for black, 2 for white

    def draw_hexagon(self, surface: object, color: tuple, position: tuple, node: int):
        # Vertex count and radius
        n = 6
        x, y = position
        offset = 3

        # Outline
        self.hex_lookup[node] = [(x + (self.hex_radius + offset) * cos(radians(90) + 2 * pi * _ / n),
                                  y + (self.hex_radius + offset) * sin(radians(90) + 2 * pi * _ / n))
                                 for _ in range(n)]
        gfxdraw.aapolygon(surface,
                          self.hex_lookup[node],
                          color)

        # Shape
        gfxdraw.filled_polygon(surface,
                               [(x + self.hex_radius * cos(radians(90) + 2 * pi * _ / n),
                                 y + self.hex_radius * sin(radians(90) + 2 * pi * _ / n))
                                for _ in range(n)],
                               self.color[node])

        # Antialiased shape outline
        gfxdraw.aapolygon(surface,
                          [(x + self.hex_radius * cos(radians(90) + 2 * pi * _ / n),
                            y + self.hex_radius * sin(radians(90) + 2 * pi * _ / n))
                           for _ in range(n)],
                          self.gray)

        # Placeholder
        rect = pygame.draw.rect(surface,
                                self.color[node],
                                pygame.Rect(x - self.hex_radius + offset, y - (self.hex_radius / 2),
                                            (self.hex_radius * 2) - (2 * offset), self.hex_radius))
        self.rects.append(rect)

    def draw_text(self):
        alphabet = list(map(chr, range(97, 123)))

        for _ in range(self.board_size):
            # Columns
            text = self.fonts.render(alphabet[_].upper(), True, self.white, self.gray)
            text_rect = text.get_rect()
            text_rect.center = (self.x_offset + (2 * self.hex_radius) * _, self.text_offset / 2)
            self.screen.blit(text, text_rect)

            # Rows
            text = self.fonts.render(str(_), True, self.white, self.gray)
            text_rect = text.get_rect()
            text_rect.center = (
                (self.text_offset / 4 + self.hex_radius * _, self.y_offset + (1.75 * self.hex_radius) * _))
            self.screen.blit(text, text_rect)

    def draw_board(self):
        counter = 0
        for row in range(self.board_size):
            for column in range(self.board_size):
                self.draw_hexagon(self.screen, self.gray, self.get_coordinates(row, column), counter)
                counter += 1
        self.draw_text()

    def get_coordinates(self, row: int, column: int):
        x = self.x_offset + (2 * self.hex_radius) * column + self.hex_radius * row
        y = self.y_offset + (1.75 * self.hex_radius) * row

        return x, y

    def get_true_coordinates(self, node: int):
        return int(node / self.board_size), node % self.board_size

    def get_node_hover(self):
        # Source: https://bit.ly/2Wl5Grz
        mouse_pos = pygame.mouse.get_pos()
        for _, rect in enumerate(self.rects):
            if rect.collidepoint(mouse_pos):
                self.node = _
                break

        if type(self.node) is int:
            # Node
            row, column = int(self.node / self.board_size), self.node % self.board_size
            self.draw_hexagon(self.screen, self.black, self.get_coordinates(row, column), self.node)

            # Text
            x, y = self.get_true_coordinates(self.node)
            x, y = self.get_coordinates(x, y)
            alphabet = list(map(chr, range(97, 123)))
            txt = alphabet[column].upper() + str(row)
            node_font = pygame.font.SysFont("Sans", 18)
            foreground = self.black if self.color[self.node] is self.white else self.white
            text = node_font.render(txt, True, foreground, self.color[self.node])
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            self.screen.blit(text, text_rect)

        return self.node

    def click_to_place_piece(self, player: int):
        """通过鼠标点击来落子"""
        mouse_pos = pygame.mouse.get_pos()
        for index, rect in enumerate(self.rects):
            if rect.collidepoint(mouse_pos):
                if self.board_state[index] is None:  # 只有空位才能落子
                    print(index)
                    self.board_state[index] = player
                    self.color[index] = self.red if player == self.BLACK_PLAYER else self.blue
                    return True,index
                # 如果该位置已经有棋子，回合不改变，返回False
                return False,-1
        return False,-1

    def algorithm_place_piece(self, player: int,index:int):
        self.board_state[index] = player
        self.color[index] = self.red if player == self.BLACK_PLAYER else self.blue
        return True

    def show_winner(self, winner):
        """在主窗口上显示获胜方"""
        winner_color = "Red" if winner == self.BLACK_PLAYER else "Bule"
        self.winner_text = f"{winner_color} is winnner!"  # 更新胜利者文本

        font = pygame.font.SysFont("Arial", 24)
        text = font.render(self.winner_text, True, self.white)
        self.screen.blit(text, (550, 10))  # 在左上角绘制文本
        self.draw_board()
        pygame.display.update()  # 更新屏幕显示
        # 等待用户关闭窗口
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # 按下ESC键退出
                        running = False

        pygame.quit()
        sys.exit()

# # 主程序
# def main():
#     pygame.init()
#
#     board_size = 11  # 设置棋盘大小
#     ui = UI(board_size)
#
#     player_turn = ui.BLACK_PLAYER  # 黑方先手
#     running = True
#     while running:
#         ui.screen.fill(ui.gray)  # 每次循环重新填充背景
#
#         # 处理事件
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:  # 左键点击
#                     if ui.click_to_place_piece(player_turn):
#                         # 如果落子成功，切换玩家
#                         player_turn = ui.WHITE_PLAYER if player_turn == ui.BLACK_PLAYER else ui.BLACK_PLAYER
#
#         # 绘制棋盘
#         ui.draw_board()
#
#         # 检测鼠标悬停的节点并显示
#         ui.get_node_hover()
#
#         pygame.display.flip()  # 更新屏幕
#         ui.clock.tick(30)  # 控制帧率
#
#     pygame.quit()
#     sys.exit()
#
#
# if __name__ == "__main__":
#     main()
