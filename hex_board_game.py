# 按装订区域中的绿色按钮以运行脚本。
import time

from Board import Board
from Player import Player


def two_player_start():
    print("two_player_start")
    pass


def computer_player_start():
    print("computer_player_start")
    pass


def two_computer_start():
    print("two_computer_start")
    pass


# 开始游戏函数
def start(demo, gamer, step_count):
    print("游戏开始！！！")
    demo.print_chequer(demo.board_list)
    print(demo.order_start[demo.start0])

    # 红蓝双方为玩家
    if gamer.isPlayer[0] + gamer.isPlayer[1] == 2:
        two_player_start()

        inp_str = "请输入你要放置棋子的坐标:\n"

        while not demo.is_over:

            print("第%d步" % (step_count + 1))
            s = input(inp_str)
            p = [""] * 2
            p[0] = s[0]
            for i in range(1, len(s)):
                p[1] += s[i]

            if not p[0].isalpha() or not p[1].isdigit() or int(p[1]) > demo.size:
                inp_str = "输入错误，请重新输入:\n"
                pass
            else:
                inp_str = "请输入你要放置棋子的坐标:\n"
                y = ord(p[0].upper()) - 65
                x = int(p[1]) - 1
                demo.make4_move(x, y, step_count, True)
                if not demo.is_clicked:
                    step_count += 1

        demo.refresh_data()

    # 一方为电脑玩家
    elif gamer.isPlayer[0] + gamer.isPlayer[1] == 1:
        computer_player_start()
        inp_str = "请输入你要放置棋子的坐标:\n"

        while not demo.is_over:

            if gamer.isPlayer[0]:  # 红方为玩家
                if (step_count + demo.start0) % 2 == 0:
                    # print(" Blue to move")
                    time_clock("Blue Thinking:", gamer.level[1])
                    print("第%d步" % (step_count + 1))
                    col = ((step_count + 1 + demo.start0) % 2) * 2 - 1
                    demo.get_best_move(col, gamer.level[1], step_count)

                else:
                    inp_is_error = True
                    while inp_is_error:
                        # print(" Red to move")
                        print("第%d步" % (step_count + 1))
                        s = input(inp_str)
                        p = [""] * 2
                        p[0] = s[0]
                        for i in range(1, len(s)):
                            p[1] += s[i]

                        if not p[0].isalpha() or not p[1].isdigit() or int(p[1]) > demo.size:
                            inp_str = "输入错误，请重新输入:\n"
                            inp_is_error = True
                            pass
                        else:
                            inp_str = "请输入你要放置棋子的坐标:\n"

                            y = ord(p[0].upper()) - 65
                            x = int(p[1]) - 1
                            demo.make_move(x, y, step_count, True)
                            inp_is_error = False
            else:

                if (step_count + demo.start0) % 2 == 0:
                    # print(" Blue to move")
                    inp_is_error = True
                    while inp_is_error:
                        # print(" Red to move")
                        print("第%d步" % (step_count + 1))
                        s = input(inp_str)
                        p = [""] * 2
                        p[0] = s[0]
                        for i in range(1, len(s)):
                            p[1] += s[i]

                        if not p[0].isalpha() or not p[1].isdigit() or int(p[1]) > demo.size:
                            inp_str = "输入错误，请重新输入:\n"
                            inp_is_error = True
                            pass
                        else:
                            inp_str = "请输入你要放置棋子的坐标:\n"
                            y = ord(p[0].upper()) - 65
                            x = int(p[1]) - 1
                            demo.make_move(x, y, step_count, True)
                            inp_is_error = False

                else:
                    # print(" Red to move")
                    time_clock("Red Thinking:", gamer.level[0])
                    print("第%d步" % (step_count + 1))
                    col = ((step_count + 1 + demo.start0) % 2) * 2 - 1
                    demo.get_best_move(col, gamer.level[0], step_count)

            if not demo.is_clicked:
                step_count += 1

        demo.refresh_data()

    # 双方为电脑玩家
    elif gamer.isPlayer[0] + gamer.isPlayer[1] == 0:
        two_computer_start()

        while not demo.is_over:

            print("第%d步" % (step_count + 1))

            if (step_count + demo.start0) % 2 == 0:

                time_clock("Blue Thinking:", gamer.level[1])
                col = ((step_count + 1 + demo.start0) % 2) * 2 - 1
                demo.get_best_move(col, gamer.level[1], step_count)

            else:

                time_clock("Red Thinking:", gamer.level[0])
                col = ((step_count + 1 + demo.start0) % 2) * 2 - 1
                demo.get_best_move(col, gamer.level[0], step_count)

            if not demo.is_clicked:
                step_count += 1

        demo.refresh_data()


# 时间进度条
def time_clock(m, level):
    scale = board.size * (7 - level)

    t = time.perf_counter()

    for i in range(scale + 1):
        a = '*' * i
        b = '.' * (scale - i)
        c = (i / scale) * 100
        t -= time.perf_counter()
        print("\r{}[{}->{}]{:^3.0f}%:{:.2f}s".format(m, a, b, c, -t), end=' ')
        time.sleep(0.05)
    print("")


# 主函数
if __name__ == '__main__':

    player = Player()
    board = Board()

    while True:

        print("【Hex棋游戏界面】".center((board.size * 6) - 4, "="))
        print("\n欢迎游玩！！！\n"
              "Hex 是一款适合两名玩家的棋盘游戏。\n"
              "它由 Piet Hein 于 1942 年和 John Nash 于 1948 年独立发明，\n"
              "并在 1950 年后以 Hex 的名义流行起来。\n"
              "游戏规则：\n"
              "红色玩家尝试将棋盘上下连通,"
              "而蓝色玩家则尝试将左右连通。\n"
              "游戏永远不会以平局结束：当所有单元格都已着色时，必须存在红色链或蓝色链。\n"
              "祝你好运！！!\n")
        print("【棋盘展示】".center((board.size * 6) - 4, "-"))
        board.print_chequer(board.board_list)
        print("【棋盘属性】".center((board.size * 6) - 4, "-"))
        print("棋盘大小：%d" % board.size)
        print("红方棋子：", board.red_default)
        print("蓝方棋子：", board.blue_default)
        print("【玩家属性】".center((board.size * 6) - 4, "-"))
        print("红方玩家： ", end=" ")
        if player.isPlayer[0]:
            print("非电脑玩家")
        else:
            print("电脑玩家---level:%d" % player.level[0])

        print("蓝方玩家： ", end=" ")
        if player.isPlayer[1]:
            print("非电脑玩家")
        else:
            print("电脑玩家---level:%d" % player.level[1])
        print("【先手顺序】".center((board.size * 6) - 4, "-"))
        print("先手方：", end=" ")
        if board.start0:
            print("红方玩家")
        else:
            print("蓝方玩家")

        print("【棋盘操作】".center((board.size * 6) - 4, "-"))
        print("1.设置棋盘属性")
        print("2.设置玩家属性")
        print("3.设置先手顺序")
        print("4.开始游戏")
        choice = int(input("请选择:"))
        match choice:
            case 1:
                inp_size = int(input("请输入一个不小于9的整数："))
                board.size = inp_size
                board.refresh_data()
                print("棋盘大小成功设置为%d !!!\n" % board.size)

            case 2:
                print("设置红色方玩家属性".center((board.size * 6) - 4, "-"))
                inp_red_player_state = int(input("请输入0或1设置红方是否为电脑玩家（0--电脑玩家、1--非电脑玩家）:"))
                player.set_red_player_state(inp_red_player_state)
                print("红方成功设置为:", player.state[player.isPlayer[0]], end=" !!!\n")

                if not inp_red_player_state:
                    inp_red_player_level = int(input("请输入（1、2、3）设置电脑玩家的等级："))
                    player.set_red_computer_level(inp_red_player_level)
                    print("红方电脑玩家等级成功设置为：", player.level[0], end="级 ！！！\n\n")

                print("设置蓝色方玩家属性".center((board.size * 6) - 4, "-"))
                inp_blue_player_state = int(input("请输入0或1设置蓝方是否为电脑玩家（0--电脑玩家、1--非电脑玩家）:"))
                player.set_blue_player_state(inp_blue_player_state)
                print("蓝方成功设置为:", player.state[player.isPlayer[1]], end=" !!!\n")

                if not inp_blue_player_state:
                    inp_red_player_level = int(input("请输入（1、2、3）设置电脑玩家的等级："))
                    player.set_blue_computer_level(inp_red_player_level)
                    print("蓝方电脑玩家等级成功设置为：", player.level[1], end="级 ！！！\n\n")

            case 3:
                inp_start0 = int(input("请输入0或1设置红蓝先手顺序（0--Blue、1--Red）:"))
                board.start0 = inp_start0
                print("红蓝先手顺序成功设置为：", board.order_start[board.start0], end=" !!!\n")

            case 4:
                move_count = 0
                start(board, player, move_count)
