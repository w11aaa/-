from Board import Board
from Player import Player
from ui import UI
import pygame
from pygame import gfxdraw
from pygame import time
import sys
from hex_board_game import *


def main():

    pygame.init()

    board_size = 11  # 设置棋盘大小
    ui = UI(board_size)

    player_turn = ui.WHITE_PLAYER  # 黑方先手
    player_current=2 #当前的下棋玩家

    running = True

    player = Player()
    board = Board()
    board.size=11
    board.refresh_data()
    # 默认红色为真人玩家（1），蓝色为电脑玩家（0）
    # 默认红色电脑难度为3，蓝色电脑难度为3
    inp_red_player_state = 1
    player.set_red_player_state(inp_red_player_state)
    if not inp_red_player_state:
        inp_red_player_level = 3
        player.set_red_computer_level(inp_red_player_level)

    inp_blue_player_state = 0
    player.set_blue_player_state(inp_blue_player_state)
    if not inp_blue_player_state:
        inp_red_player_level = 3
        player.set_blue_computer_level(inp_red_player_level)
    # 设置红色先手
    inp_start0 = 1
    board.start0 = inp_start0
    move_count = 0
    # start(board, player, move_count)


    while running:
        ui.screen.fill(ui.gray)  # 每次循环重新填充背景

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    Legal_location,index=ui.click_to_place_piece(player_turn)
                    if Legal_location and player_current==1: # 如果点击位置合法且轮到玩家下棋
                        # player_turn = ui.WHITE_PLAYER if player_turn == ui.BLACK_PLAYER else ui.BLACK_PLAYER
                        col=index%board.size
                        row=index//board.size
                        board.make_move(col, row, move_count, board.start0)
                        if board.is_over:
                            print("游戏结束！")
                            ui.show_winner(player_turn)
                        move_count += 1
                        player_current=2

        if player_current==1 and player_turn == ui.WHITE_PLAYER:
            player_turn = ui.BLACK_PLAYER #切换到黑方下棋

        if player_current==2 and player_turn == ui.WHITE_PLAYER:
            # 如果轮到电脑下棋，调用电脑下棋函数
            col = ((move_count + 1 + board.start0) % 2) * 2 - 1
            col,row=board.get_best_move(col, player.level[1], move_count)
            index=row*board.size+col
            ui.algorithm_place_piece(player_turn, index)
            if board.is_over:
                print("游戏结束！")
                ui.show_winner(player_turn)

            move_count += 1
            player_current=1

        if player_current==2 and player_turn == ui.BLACK_PLAYER:
            player_turn = ui.WHITE_PLAYER #切换到白方下棋

        # 绘制棋盘
        ui.draw_board()
        # # 检测鼠标悬停的节点并显示
        # ui.get_node_hover()
        pygame.display.flip()  # 更新屏幕
        ui.clock.tick(30)  # 控制帧率

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
