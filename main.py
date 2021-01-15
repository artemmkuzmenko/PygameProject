class Player:
    def __init__(self, pos, image):
        self.x, self.y = self.pos = pos
        self.treasure = False
        self.image = image

    def set_pos(self, pos):
        self.x, self.y = self.pos = pos

    def get_treasure(self):
        self.treasure = True

    def image(self):
        return self.image
