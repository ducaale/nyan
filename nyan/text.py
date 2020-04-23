import os

import pygame

from .color import color_name_to_rgb
from .sprite import Sprite

class Text(Sprite):
    def __init__(self, game, text, x, y, z, angle, font, font_size, color):
        self._text = text
        self._font = font
        self._font_size = font_size
        self._color = color
        super().__init__(game, x, y, z, angle, 100)

    def _compute_primary_surface(self):
        if self._font is not None:
            font = os.path.join('assets', self._font)
            pygame_font = pygame.font.Font(font, self._font_size)
        else:
            pygame_font = pygame.font.SysFont('Sans', self._font_size)
        surface = pygame_font.render(self._text, True, color_name_to_rgb(self._color))
        return surface

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self._primary_surface = self._compute_primary_surface()
        self._secondary_surface = self._compute_secondary_surface()

    # propery alias to achieve compatibility with replit-play api
    words = text

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font):
        self._font = font
        self._primary_surface = self._compute_primary_surface()
        self._secondary_surface = self._compute_secondary_surface()

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        self._font_size = font_size
        self._primary_surface = self._compute_primary_surface()
        self._secondary_surface = self._compute_secondary_surface()

    @property 
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self._primary_surface = self._compute_primary_surface()
        self._secondary_surface = self._compute_secondary_surface()