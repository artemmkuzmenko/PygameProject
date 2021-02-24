import random

from board import Board


class Player:
    def __init__(self, pos):
        self.x, self.y = self.pos = pos
        self.treasure = False
        self.lives = 3

    def set_pos(self, pos):
        self.x, self.y = self.pos = pos

    def get_treasure(self):
        if self.lives == 3:
            self.treasure = True

    def lose_treasure(self):
        self.treasure = False


class Hole:
    def __init__(self, pos):
        self.pos = self.x, self.y = pos
        self.treasure = False

    def get_treasure(self):
        self.treasure = True

    def lose_treasure(self):
        self.treasure = False

    def injure(self, player):
        if player.pos == self.pos:
            player.lives -= 1


class River:
    def __init__(self, positions):
        self.positions = positions
        self.treasure = False

    def get_treasure(self):
        self.treasure = True

    def lose_treasure(self):
        self.treasure = False

    def injure(self, player):
        for pos in self.positions:
            if player.pos == pos:
                player.lives -= 1


class TreasurePlace:
    def __init__(self, pos):
        self.pos = pos
        self.treasure = True

    def lose_treasure(self):
        self.treasure = False


class Hospital:
    def __init__(self, pos):
        self.pos = pos

    def treat(self, player):
        if self.pos == player.pos:
            player.lives = 3


class Bear:
    def __init__(self, start_pos):
        self.pos = start_pos

    def move(self):
        x, y = self.pos
        pos = random.choice([(x - 1, y), (x - 1, y - 1), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1),
                             (x + 1, y), (x + 1, y + 1)])
        self.pos = pos

    def attack(self, player):
        if self.pos == player.pos:
            player.lives -= 1


class Wall:
    def __init__(self, pos):
        self.pos = pos


class Labyrinth(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    def set_player(self):
        player = Player((random.choice(range(self.width)), random.choice(range(self.height))))
        return player

    def set_hole(self):
        while True:
            hole = Hole((random.choice(range(self.width)), random.choice(range(self.height))))
            x, y = hole.pos
            if self.board[x][y] == 0:
                break
        self.board[x][y] = 'hole'
        return hole

    def set_hospital(self):
        while True:
            hospital = Hospital((random.choice(range(self.width)), random.choice(range(self.height))))
            x, y = hospital.pos
            if self.board[x][y] == 0:
                break
        self.board[x][y] = 'hospital'
        return hospital

    def set_treasure_place(self):
        while True:
            treasure_place = TreasurePlace((random.choice(range(self.width)), random.choice(range(self.height))))
            x, y = treasure_place.pos
            if self.board[x][y] == 0:
                break
        self.board[x][y] = 'treasure place'
        return treasure_place

    def set_bear(self):
        while True:
            bear = Bear((random.choice(range(self.width)), random.choice(range(self.height))))
            x, y = bear.pos
            if self.board[x][y] == 0:
                break
        return bear

    def set_river(self, length):
        positions = []
        pos = (random.choice(range(self.width)), random.choice(range(self.height)))
        positions.append(pos)
        for i in range(length - 1):
            x, y = pos
            self.board[x][y] = i + 1
            pos = random.choice([(x - 1, y), (x - 1, y - 1), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1),
                                 (x + 1, y), (x + 1, y + 1)])
            positions.append(pos)
        x, y = pos
        self.board[x][y] = length + 1
        river = River(positions)
        return river

    def set_wall(self):
        while True:
            wall = Wall((random.choice(range(self.width)), random.choice(range(self.height))))
            x, y = wall.pos
            if self.board[x][y] == 0:
                break
        self.board[x][y] = 'wall'
        return wall
