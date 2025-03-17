import pygame

class Screen():
    def __init__(self, width=800, height=600):
        self._width = width
        self._height = height
        self._surface = pygame.display.set_mode((self._width, self._height))

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        self._surface = pygame.display.set_mode((self._width, self._height))

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        self._surface = pygame.display.set_mode((self._width, self._height))

    @property
    def top(self):
        return self.height / 2

    @property
    def bottom(self):
        return self.height / -2

    @property
    def left(self):
        return self.width / -2

    @property
    def right(self):
        return self.width / 2