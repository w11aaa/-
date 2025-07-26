class Player:
    isPlayer = [True] * 2
    level = [3] * 2
    state = ["电脑玩家", "玩家"]

    def __init__(self, is_red_player=True, is_blue_player=True, red_computer_level=3, blue_computer_level=3):
        self.isPlayer[0] = is_red_player
        self.isPlayer[1] = is_blue_player
        self.level[0] = red_computer_level
        self.level[1] = blue_computer_level

    def set_red_player_state(self, is_red_player):
        self.isPlayer[0] = is_red_player

    def set_blue_player_state(self, is_blue_player):
        self.isPlayer[1] = is_blue_player

    def set_red_computer_level(self, level):
        self.level[0] = level

    def set_blue_computer_level(self, level):
        self.level[1] = level
