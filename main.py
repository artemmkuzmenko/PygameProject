import random

from board import Board


class Player:
    def __init__(self, pos, image):
        self.x, self.y = self.pos = pos
        self.treasure = False
        self.image = image
        self.lives = 3

    def set_pos(self, pos):
        self.x, self.y = self.pos = pos

    def get_treasure(self):
        self.treasure = True

    def lose_treasure(self):
        self.treasure = False

    def image(self):
        return self.image


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


class Labyrinth(Board):
    def __init__(self, width, height, objects):
        super().__init__(width, height)
        self.objects = objects
