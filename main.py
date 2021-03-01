import os
import random

import pygame

from board import Board


def load_image(name):  # функция загрузки картинки
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    return image


class Player:  # класс игрока
    def __init__(self, pos):
        self.x, self.y = self.pos = pos
        self.treasure = False
        self.lives = 3
        self.image = load_image('player.png')

    def get_treasure(self):
        if self.lives == 3:
            self.treasure = True
            self.image = load_image('player_with_treasure.png')

    def lose_treasure(self):
        self.treasure = False
        self.image = load_image('player.png')


class Hole:  # класс ямы
    def __init__(self, pos):
        self.pos = self.x, self.y = pos
        self.treasure = False
        self.image = load_image('hole.png')
        self.visible = False

    def get_treasure(self):
        self.treasure = True

    def lose_treasure(self):
        self.treasure = False

    def injure(self, player):
        if player.pos == self.pos:
            player.lives -= 1
            self.visible = True

    def __str__(self):
        return 'hole'


class River:  # класс реки
    def __init__(self, positions):
        self.positions = positions
        self.treasure = False
        self.image = load_image('river.png')
        self.visible = False

    def get_treasure(self):
        self.treasure = True

    def lose_treasure(self):
        self.treasure = False

    def injure(self, player):
        player.lives -= 1
        self.visible = True
        for pos in self.positions:
            if player.pos == pos:
                player.pos = self.positions[-1]
            if player.treasure:
                player.treasure = False

    def __str__(self):
        return 'river'


class Treasure:  # класс клада
    def __init__(self, pos):
        self.pos = pos
        self.visible = False

    def __str__(self):
        return 'treasure place'


class Hospital:  # класс больницы
    def __init__(self, pos):
        self.pos = pos
        self.image = load_image('hospital.png')
        self.visible = False

    def treat(self, player):
        if self.pos == player.pos:
            player.lives = 3
            self.visible = True

    def __str__(self):
        return 'hospital'


class Bear:  # класс медведя
    def __init__(self, start_pos):
        self.pos = start_pos
        self.image = load_image('bear.png')
        self.visible = False

    def move(self):
        x, y = self.pos
        self.visible = False
        pos = random.choice([(x - 1, y), (x - 1, y - 1), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1),
                             (x + 1, y), (x + 1, y + 1)])
        self.pos = pos

    def attack(self, player):
        if self.pos == player.pos:
            player.lives -= 1
            self.visible = True

    def __str__(self):
        return 'bear'


class Wall:  # класс стены
    def __init__(self, pos):
        self.pos = pos
        self.image = load_image('wall.png')
        self.visible = False

    def __str__(self):
        return 'wall'


class Labyrinth(Board):  # класс лабиринта
    def __init__(self, width, height):
        super().__init__(width, height)

    # расстановка объектов случайным образом
    def set_player(self):
        player = Player((random.choice(range(self.width)), random.choice(range(self.height))))
        return player

    def set_hole(self):
        while True:
            hole = Hole((random.choice(range(self.width)), random.choice(range(self.height))))
            x, y = hole.pos
            if self.board[x][y] == 0:
                break
        self.board[x][y] = hole
        return hole

    def set_hospital(self):
        while True:
            hospital = Hospital((random.choice(range(self.width)), random.choice(range(self.height))))
            x, y = hospital.pos
            if self.board[x][y] == 0:
                break
        self.board[x][y] = hospital
        return hospital

    def set_treasure(self):
        while True:
            treasure_place = Treasure((random.choice(range(self.width)), random.choice(range(self.height))))
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
            self.board[x][y] = bear
        return bear

    def set_river(self, length):
        positions = []
        pos = (random.choice(range(self.width)), random.choice(range(self.height)))
        positions.append(pos)
        while True:
            try:
                for i in range(length - 1):
                    x, y = pos
                    self.board[x][y] = i + 1
                    pos = random.choice([(x - 1, y), (x - 1, y - 1), (x - 1, y + 1), (x, y - 1), (x, y + 1),
                                         (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)])
                    positions.append(pos)
                x, y = pos
                river = River(positions)
                for x, y in positions:
                    self.board[x][y] = river
                break
            except IndexError:
                pass
        return river

    def set_wall(self):
        while True:
            wall = Wall((random.choice(range(self.width)), random.choice(range(self.height))))
            x, y = wall.pos
            if self.board[x][y] == 0:
                break
        self.board[x][y] = wall
        return wall

    def set_exit(self):
        self.board[9][9] = 'exit'


class Game:  # класс самой игры
    def __init__(self, screen):
        self.lab = Labyrinth(10, 10)
        self.lab.set_view(10, 10, 40)
        self.screen = screen
        self.victory = False

    def start_pos(self):
        self.player = self.lab.set_player()
        self.river = self.lab.set_river(6)
        self.lab.set_exit()
        self.wall = []
        for _ in range(10):
            self.wall.append(self.lab.set_wall())
        self.hole1 = self.lab.set_hole()
        self.hole2 = self.lab.set_hole()
        self.treasure = self.lab.set_treasure()
        self.hospital = self.lab.set_hospital()
        self.bear = self.lab.set_bear()


    # сам ход
    def move(self, direction):
        pos = self.player.pos
        x, y = pos
        x1 = x
        y1 = y
        # определяем направление
        if direction == 'up':
            x1, y1 = x, y - 1
        elif direction == 'down':
            x1, y1 = x, y + 1
        elif direction == 'left':
            x1, y1 = x - 1, y
        elif direction == 'right':
            x1, y1 = x + 1, y
        wall = False
        try:
            if str(self.lab.board[x1][y1]) == 'wall':
                self.lab.board[x1][y1].visible = True
                wall = True
        except IndexError:
            pass
        if x1 > 9 or x1 < 0 or y1 > 9 or y1 < 0:
            pass
        elif not wall:
            self.player.pos = x1, y1
            self.player.x = x1
            self.player.y = y1
        x, y = self.player.pos
        # прописываем действия для разных объектов
        if str(self.lab.board[x][y]) == 'treasure place':
            self.player.get_treasure()
            self.treasure.visible = True
            self.lab.board[x][y] = 0
        elif str(self.lab.board[x][y]) == 'hole':
            if self.lab.board[x][y].treasure:
                self.player.get_treasure()
                self.lab.board[x][y].lose_treasure()
            else:
                self.lab.board[x][y].injure(self.player)
                if self.player.treasure:
                    self.player.lose_treasure()
                    self.lab.board[x][y].get_treasure()
        elif str(self.lab.board[x][y]) == 'hospital':
            self.lab.board[x][y].treat(self.player)
        elif str(self.lab.board[x][y]) == 'bear':
            self.lab.board[x][y].attack(self.player)
            if self.player.treasure:
                self.player.lose_treasure()
        elif str(self.lab.board[x][y]) == 'exit' and self.player.treasure:
            win(self.screen)
            self.victory = True
        elif str(self.lab.board[x][y]) == 'river':
            if self.lab.board[x][y].treasure:
                self.player.get_treasure()
                self.lab.board[x][y].lose_treasure()
            else:
                if self.player.treasure:
                    self.treasure.pos = self.river.positions[-1]
                self.lab.board[x][y].injure(self.player)
        if self.player.treasure:
            self.treasure.pos = self.player.pos
        self.bear.move()


# функции победы проигрыша и заставки
def win(screen):
    image = load_image('victory.jpg')
    screen.blit(image, (0, 0))


def game_over(screen):
    image = load_image('game over.jpg')
    screen.blit(image, (0, 0))


def start(screen):
    image = load_image('start.jpeg')
    screen.blit(image, (0, 0))


def main():
    if __name__ == '__main__':
        pygame.init()
        size = 500, 500
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Лабиринт')
        start(screen)
        pygame.time.delay(2000)
        pygame.display.flip()
        game = Game(screen)
        game.start_pos()
        running = True
        pygame.display.flip()
        while running:
            screen.fill(pygame.Color('white'))
            game.lab.render(screen)
            if game.player.lives == 0:
                game_over(screen)
                pygame.time.delay(2000)
                running = False
            if game.victory:
                pygame.time.delay(2000)
                running = False
            for i in range(10):
                for j in range(10):
                    if not isinstance(game.lab.board[i][j], int) and not isinstance(game.lab.board[i][j], str):
                        if game.lab.board[i][j].visible:
                            screen.blit(game.lab.board[i][j].image, (game.lab.left + game.lab.cell_size * i,
                                        game.lab.top + game.lab.cell_size * j))
            screen.blit(game.player.image, (game.player.x * game.lab.cell_size + game.lab.left,
                        game.player.y * game.lab.cell_size + game.lab.top))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        game.move('down')
                    elif event.key == pygame.K_UP:
                        game.move('up')
                    elif event.key == pygame.K_LEFT:
                        game.move('left')
                    elif event.key == pygame.K_RIGHT:
                        game.move('right')
            screen.blit(game.player.image, (game.player.x * game.lab.cell_size + game.lab.left,
                                            game.player.y * game.lab.cell_size + game.lab.top))
            pygame.display.flip()
        pygame.quit()


main()
