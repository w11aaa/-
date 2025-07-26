import math
import random


class Board:
    order_start = ["Blue Begins", "Red Begins"]

    def __init__(self, size=9, default="*"):
        self.max_move_count = 0
        self.size = size
        self.default = default
        self.red_default = "X"
        self.blue_default = "0"
        self.is_swap = 0
        self.is_over = False
        self.max_fld = self.size * self.size
        self.active_color = 0
        self.is_clicked = False
        self.start0 = False
        self.is_running = False

        self.board_list = [[self.default] * int(self.size) for _ in range(int(self.size))]
        self.upd_list = [[0] * int(self.size) for _ in range(int(self.size))]
        self.fld_list = [[0] * int(self.size) for _ in range(int(self.size))]
        self.history_list = [[0] * 2 for _ in range(self.max_fld + 1)]
        self.pot_list = [[[0] * 4 for _ in range(self.size)] for _ in range(self.size)]
        self.bridge_list = [[[0] * 4 for _ in range(self.size)] for _ in range(self.size)]
        self.vv_list = [0] * 6
        self.tt_list = [0] * 6

    # 刷新初始化数组列表
    def refresh_data(self):
        self.is_over = False
        self.max_fld = self.size * self.size
        self.board_list = [[self.default] * int(self.size) for _ in range(int(self.size))]
        self.upd_list = [[0] * int(self.size) for _ in range(int(self.size))]
        self.fld_list = [[0] * int(self.size) for _ in range(int(self.size))]
        self.history_list = [[0] * 2 for _ in range(self.max_fld + 1)]
        self.pot_list = [[[0] * 4 for _ in range(self.size)] for _ in range(self.size)]
        self.bridge_list = [[[0] * 4 for _ in range(self.size)] for _ in range(self.size)]
        self.vv_list = [0] * 6
        self.tt_list = [0] * 6

    # 格式化打印数组列表
    @staticmethod
    def print_chequer(demo):
        print("", end=" " * 3)
        for i in range(0, len(demo)):
            print(chr(i + 65), end=" " * 3)
        print(" ")
        for i in range(0, len(demo)):
            for j in range(i):
                print(" ", end=" ")
            print(i + 1, end=" " * 2)
            for k in range(0, len(demo[i])):
                print(demo[i][k], end=" " * 3)
                if k == len(demo[i]) - 1:
                    print("")
        # print(demo)


    # 设置红方棋子落点
    def set_red_value(self, x, y):

        if self.board_list[x][y] == self.default:
            self.board_list[x][y] = self.red_default
            self.is_clicked = False
            return self.board_list
        else:
            print("该点已有棋子，请重新下子\n")
            self.is_clicked = True
            return self.board_list

    # 设置蓝色方棋子落点
    def set_blue_value(self, x, y):

        if self.board_list[x][y] == self.default:
            self.board_list[x][y] = self.blue_default
            self.is_clicked = False
            return self.board_list
        else:
            print("该点已有棋子，请重新下子\n")
            self.is_clicked = True
            return self.board_list

    # 落点并判断输赢
    def make_move(self, x, y, move_count, oo):
        print(x,y)
        if move_count == 1:
            if self.fld_list[x][y] != 0:
                self.fld_list[x][y] = 0
                tem = x
                x = y
                y = tem
                self.is_swap = 1
            else:
                self.is_swap = 0

        col = ((move_count + 1 + self.start0) % 2) * 2 - 1
        self.fld_list[x][y] = col

        if self.history_list[move_count][0] != x:
            self.history_list[move_count][0] = x
            self.max_move_count = move_count + 1

        if self.history_list[move_count][1] != y:
            self.history_list[move_count][1] = y
            self.max_move_count = move_count + 1

        # move_count += 1

        if self.max_move_count < move_count:
            self.max_move_count = move_count

        if move_count < 10:
            print("%d<10" % move_count)
        else:
            print(move_count)

        if (move_count + self.start0) % 2 == 0:
            print(" Blue to move")
            self.set_blue_value(x, y)
            self.print_chequer(self.board_list)

        else:
            print(" Red to move")
            self.set_red_value(x, y)
            self.print_chequer(self.board_list)

        if not oo:
            return

        self.get_pot(0, move_count, self.start0)

        if col < 0:
            if self.pot_list[x][y][2] > 0 or self.pot_list[x][y][3] > 0:
                return
            else:

                print(" Red has won!\n")

        else:
            if self.pot_list[x][y][0] > 0 or self.pot_list[x][y][1] > 0:
                return
            else:

                print(" Blue has won!\n")

        self.is_over = True

    # 更新判断输赢依据
    def get_pot(self, level, move_count, start0):
        dd = 128
        self.active_color = ((move_count + 1 + start0) % 2) * 2 - 1
        self.pot_list = [[[20000] * 4 for _ in range(self.size)] for _ in range(self.size)]
        self.bridge_list = [[[0] * 4 for _ in range(self.size)] for _ in range(self.size)]

        for x in range(self.size):
            if self.fld_list[x][0] == 0:
                self.pot_list[x][0][0] = dd
            elif self.fld_list[x][0] > 0:
                self.pot_list[x][0][0] = 0
            if self.fld_list[x][self.size - 1] == 0:
                self.pot_list[x][self.size - 1][1] = dd
            elif self.fld_list[x][self.size - 1] > 0:
                self.pot_list[x][self.size - 1][1] = 0

        for y in range(self.size):
            if self.fld_list[0][y] == 0:
                self.pot_list[0][y][2] = dd
            elif self.fld_list[0][y] < 0:
                self.pot_list[0][y][2] = 0
            if self.fld_list[self.size - 1][y] == 0:
                self.pot_list[self.size - 1][y][3] = dd
            elif self.fld_list[self.size - 1][y] < 0:
                self.pot_list[self.size - 1][y][3] = 0

        for z in range(2):
            for x in range(self.size):
                for y in range(self.size):
                    self.upd_list[x][y] = True
            nn = 1
            bb = 0
            for x in range(self.size):
                for y in range(self.size):
                    if self.upd_list[x][y]:
                        bb += self.set_pot(x, y, z, 1, level)

            for x in range(self.size - 1, -1, -1):
                for y in range(self.size - 1, -1, -1):
                    if self.upd_list[x][y]:
                        bb += self.set_pot(x, y, z, 1, level)

            while bb > 0 and nn < 12:
                nn += 1
                for x in range(self.size):
                    for y in range(self.size):
                        if self.upd_list[x][y]:
                            bb += self.set_pot(x, y, z, 1, level)

                for x in range(self.size - 1, -1, -1):
                    for y in range(self.size - 1, -1, -1):
                        if self.upd_list[x][y]:
                            bb += self.set_pot(x, y, z, 1, level)

        for z in range(2, 4):
            for x in range(self.size):
                for y in range(self.size):
                    self.upd_list[x][y] = True
            nn = 1
            bb = 0
            for x in range(self.size):
                for y in range(self.size):
                    if self.upd_list[x][y]:
                        bb += self.set_pot(x, y, z, -1, level)

            for x in range(self.size - 1, -1, -1):
                for y in range(self.size - 1, -1, -1):
                    if self.upd_list[x][y]:
                        bb += self.set_pot(x, y, z, -1, level)

            while bb > 0 and nn < 12:
                nn += 1
                for x in range(self.size):
                    for y in range(self.size):
                        if self.upd_list[x][y]:
                            bb += self.set_pot(x, y, z, -1, level)

                for x in range(self.size - 1, -1, -1):
                    for y in range(self.size - 1, -1, -1):
                        if self.upd_list[x][y]:
                            bb += self.set_pot(x, y, z, -1, level)

    def set_pot(self, x, y, z, k, level):
        self.upd_list[x][y] = False
        self.bridge_list[x][y][z] = 0

        if self.fld_list[x][y] == -k:
            return 0
        ddb = 0

        dd = 140
        bb = 66
        if k != self.active_color:
            bb = 52

        self.vv_list[0] = self.pot_val(x + 1, y, z, k)
        self.vv_list[1] = self.pot_val(x, y + 1, z, k)
        self.vv_list[2] = self.pot_val(x - 1, y + 1, z, k)
        self.vv_list[3] = self.pot_val(x - 1, y, z, k)
        self.vv_list[4] = self.pot_val(x, y - 1, z, k)
        self.vv_list[5] = self.pot_val(x + 1, y - 1, z, k)

        for i in range(6):
            if self.vv_list[i] >= 30000 and self.vv_list[(i + 2) % 6] >= 30000:
                if self.vv_list[(i + 1) % 6] < 0:
                    ddb += 32
                else:
                    self.vv_list[(i + 1) % 6] += 128

        for ll in range(6):
            if self.vv_list[ll] >= 30000 and self.vv_list[(ll + 3) % 6] >= 30000:
                ddb += 30

        mm = 30000
        for m in range(6):
            if self.vv_list[m] < 0:
                self.vv_list[m] += 30000
                self.tt_list[m] = 10
            else:
                self.tt_list[m] = 1

            if mm > self.vv_list[m]:
                mm = self.vv_list[m]

        nn = 0
        for n in range(6):
            if self.vv_list[n] == mm:
                nn += self.tt_list[n]

        if level > 1:
            self.bridge_list[x][y][z] = nn / 5

            if (nn >= 2) and (nn < 10):
                self.bridge_list[x][y][z] = bb + nn - 2
                mm -= 32
            if nn < 2:
                oo = 30000
                for i in range(6):
                    if (self.vv_list[i] > mm) and (oo > self.vv_list[i]):
                        oo = self.vv_list[i]

                if oo <= mm + 104:
                    self.bridge_list[x][y][z] = bb - (oo - mm) / 4
                    mm -= 64
                mm += oo
                mm /= 2
        if (x > 0) and (x < self.size - 1) and (y > 0) and y < self.size - 1:
            self.bridge_list[x][y][z] += ddb
        else:
            self.bridge_list[x][y][z] -= 2
        if (x == 0 or x == self.size - 1) and (y == 0 or y == self.size - 1):
            self.bridge_list[x][y][z] /= 2
        if self.bridge_list[x][y][z] > 68:
            self.bridge_list[x][y][z] = 68

        if self.fld_list[x][y] == k:
            if mm < self.pot_list[x][y][z]:
                self.pot_list[x][y][z] = mm
                self.set_upd(x + 1, y, k)
                self.set_upd(x, y + 1, k)
                self.set_upd(x - 1, y + 1, k)
                self.set_upd(x - 1, y, k)
                self.set_upd(x, y - 1, k)
                self.set_upd(x + 1, y - 1, k)
                return 1
            return 0
        if mm + dd < self.pot_list[x][y][z]:
            self.pot_list[x][y][z] = mm + dd
            self.set_upd(x + 1, y, k)
            self.set_upd(x, y + 1, k)
            self.set_upd(x - 1, y + 1, k)
            self.set_upd(x - 1, y, k)
            self.set_upd(x, y - 1, k)
            self.set_upd(x + 1, y - 1, k)
            return 1
        return 0

    def pot_val(self, x, y, z, k):
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return 30000
        if self.fld_list[x][y] == 0:
            return self.pot_list[x][y][z]
        if self.fld_list[x][y] == -k:
            return 30000
        return int(self.pot_list[x][y][z]) - 30000

    def set_upd(self, x, y, k):
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return

        self.upd_list[x][y] = True

    @staticmethod
    def sign(x):
        if x < 0:
            return -1
        elif x > 0:
            return 1
        else:
            return 0

    def get_fld(self, x, y):
        if x < 0:
            return -1
        if y < 0:
            return 1
        if x >= self.size:
            return -1
        if y >= self.size:
            return 1
        return self.fld_list[x][y]

    # 电脑玩家移动棋子判断
    def get_best_move(self, col, level, move_count):

        ff = 0
        if move_count > 0:
            ff = 190 / (move_count * move_count)
        mm = 20000
        a = 0
        b = 0
        x = 0
        y = 0
        x1 = 0
        y1 = 0
        c = [0] * self.max_fld
        temp = [0, 0, 0, 0]
        temp_is_zero = True
        for i in range(self.size):
            for j in range(self.size):
                if self.fld_list[i][j] != 0:
                    a += 2 * i + 1 - self.size
                    b += 2 * j + 1 - self.size

        a = self.sign(a)
        b = self.sign(b)
        for i in range(self.size):
            for j in range(self.size):
                if self.fld_list[i][j] == 0:

                    mp = random.random() * (49 - level * 16)
                    mp += math.fabs(i - 5) + math.fabs(j - 5) * ff
                    mp += 8 * (a * (i - 5) + b * (j - 5)) / (move_count + 1)

                    if level > 2:
                        for k in range(4):
                            mp -= self.bridge_list[i][j][k]

                    p0 = self.pot_list[i][j][0] + self.pot_list[i][j][1]
                    p1 = self.pot_list[i][j][2] + self.pot_list[i][j][3]
                    mp += p0 + p1
                    if p0 <= 268 or p1 <= 268:
                        mp -= 400
                    c[i * self.size + j] = mp
                    if mp < mm:
                        mm = mp
                        x = i
                        y = j
                        x1 = i
                        y1 = j

        if level > 2:
            mm += 108
            for i in range(self.size):
                for j in range(self.size):
                    if c[i * self.size + j] < mm:
                        if col < 0:  # red
                            if i in range(4, self.size - 1) and j in range(1, 3):

                                if self.fld_list[i - 1][j + 2] == -col:
                                    cc = self.can_connect_far_board(i - 1, j + 2, -col)
                                    if cc < 2:
                                        x = i
                                        if cc < -1:
                                            x -= 1
                                            cc += 1
                                        y = j - cc
                                        mm = c[i * self.size + j]

                                        # print("1.x=%d,y=%d" % (x, y))
                            if i in range(1, self.size - 1) and j == 0:
                                temp[0] = int(self.fld_list[i - 1][j])
                                temp[1] = int(self.fld_list[i - 1][j + 1])
                                temp[2] = int(self.fld_list[i][j + 1])
                                temp[3] = int(self.fld_list[i + 1][j])
                                for t in range(4):
                                    if temp[t] != 0:
                                        temp_is_zero = False

                                if self.fld_list[i - 1][j + 2] == -col and temp_is_zero:
                                    x = i
                                    y = j
                                    mm = c[i * self.size + j]
                                    # print("2.x=%d,y=%d" % (x, y))

                            if i in range(1, self.size - 4) and j in range(self.size - 3, self.size - 1):

                                if self.fld_list[i + 1][j - 2] == -col:
                                    cc = self.can_connect_far_board(i + 1, j - 2, -col)
                                    if cc < 2:
                                        x = i
                                        if cc < -1:
                                            x += 1
                                            cc += 1
                                        y = j + cc
                                        mm = c[i * self.size + j]
                                        # print("3.x=%d,y=%d" % (x, y))
                            if i in range(1, self.size - 1) and j == self.size - 1:

                                temp[0] = int(self.fld_list[i + 1][j])
                                temp[1] = int(self.fld_list[i + 1][j - 1])
                                temp[2] = int(self.fld_list[i][j - 1])
                                temp[3] = int(self.fld_list[i - 1][j])
                                for t in range(4):
                                    if temp[t] != 0:
                                        temp_is_zero = False

                                if self.fld_list[i + 1][j - 2] == -col and temp_is_zero:
                                    x = i
                                    y = j
                                    mm = c[i * self.size + j]
                                    # print("4.x=%d,y=%d" % (x, y))

                        else:
                            if j in range(4, self.size - 1) and i in range(1, 3):

                                if self.fld_list[i + 2][j - 1] == -col:
                                    cc = self.can_connect_far_board(i + 2, j - 1, -col)
                                    if cc < 2:
                                        y = j
                                        if cc < -1:
                                            y -= 1
                                            cc += 1
                                        x = i - cc

                                        mm = c[i * self.size + j]
                                        # print("5.x=%d,y=%d" % (x, y))

                            if j in range(1, self.size - 1) and i == 0:

                                temp[0] = int(self.fld_list[i][j - 1])
                                temp[1] = int(self.fld_list[i + 1][j - 1])
                                temp[2] = int(self.fld_list[i + 1][j])
                                temp[3] = int(self.fld_list[i][j + 1])
                                for t in range(4):
                                    if temp[t] != 0:
                                        temp_is_zero = False

                                if self.fld_list[i + 2][j - 1] == -col and temp_is_zero:
                                    x = i
                                    y = j
                                    mm = c[i * self.size + j]
                                    # print("6.x=%d,y=%d" % (x, y))

                            if j in range(1, self.size - 4) and i in range(self.size - 3, self.size - 1):

                                if self.fld_list[i - 2][j + 1] == -col:
                                    cc = self.can_connect_far_board(i - 2, j + 1, -col)
                                    if cc < 2:
                                        y = j
                                        if cc < -1:
                                            y += 1
                                            cc += 1
                                        x = i + cc
                                        mm = c[i * self.size + j]
                                        # print("7.x=%d,y=%d" % (x, y))
                            if j in range(1, self.size - 1) and i == self.size - 1:

                                temp[0] = self.fld_list[i][j + 1]
                                temp[1] = self.fld_list[i - 1][j + 1]
                                temp[2] = self.fld_list[i - 1][j]
                                temp[3] = self.fld_list[i][j - 1]
                                for t in range(4):
                                    if temp[t] != 0:
                                        temp_is_zero = False

                                if self.fld_list[i - 2][j + 1] == -col and temp_is_zero:
                                    x = i
                                    y = j
                                    mm = c[i * self.size + j]
                                    # print("8.x=%d,y=%d" % (x, y))
        if self.fld_list[x][y] != 0:
            x = x1
            y = y1

        self.make_move(x, y, move_count, False)
        self.get_pot(level, move_count, self.start0)

        if col < 0:

            if self.pot_list[x][y][2] > 0 or self.pot_list[x][y][3] > 0:
                return x,y
            else:
                print(" Red has won !\n")

        else:
            if self.pot_list[x][y][0] > 0 or self.pot_list[x][y][1] > 0:
                return x,y
            else:
                print(" Blue has won !\n")

        self.is_over = True
        return x, y

    # 判断是否连通
    def can_connect_far_board(self, nn, mm, cc):
        if cc > 0:  # blue
            if (2 * mm) < (self.size - 1):
                for i in range(self.size):
                    for j in range(mm):
                        if (j - i < mm - nn) and (i + j <= nn + mm) and (self.fld_list[i][j] != 0):
                            return 2

                if self.fld_list[nn - 1][mm] == -cc:
                    return 0
                if self.fld_list[nn - 1][mm - 1] == -cc:
                    if self.get_fld(nn + 2, mm - 1) == -cc:
                        return 0

                    return -1

                if self.get_fld(nn + 2, mm - 1) == -cc:
                    return -2
            else:
                for i in range(self.size):
                    for j in range(self.size - 1, mm, -1):
                        if (j - i > mm - nn) and (i + j >= nn + mm) and (self.fld_list[i][j] != 0):
                            return 2

                if self.fld_list[nn + 1][mm] == -cc:
                    return 0
                if self.fld_list[nn + 1][mm + 1] == -cc:
                    if self.get_fld(nn - 2, mm + 1) == -cc:
                        return 0

                    return -1
                if self.get_fld(nn - 2, mm + 1) == -cc:
                    return -2

        else:
            if 2 * nn < self.size - 1:
                for j in range(self.size):
                    for i in range(nn):
                        if i - j < nn - mm and i + j <= nn + mm and self.fld_list[i][j] != 0:
                            return 2
                if self.fld_list[nn][mm - 1] == -cc:
                    return 0
                if self.fld_list[nn - 1][mm - 1] == -cc:
                    if self.get_fld(nn - 1, mm + 2) == -cc:
                        return 0
                    return -1
                if self.get_fld(nn - 1, mm + 2) == -cc:
                    return -2
            else:
                for j in range(self.size):
                    for i in range(self.size - 1, nn, -1):
                        if i - j > nn - mm and i + j >= nn + mm and self.fld_list[i][j] != 0:
                            return 2

                if self.fld_list[nn][mm + 1] == -cc:
                    return 0
                if self.fld_list[nn + 1][mm + 1] == -cc:
                    if self.get_fld(nn + 1, mm - 2) == -cc:
                        return 0
                    return -1
                if self.get_fld(nn + 1, mm - 2) == -cc:
                    return -2

        return 1
