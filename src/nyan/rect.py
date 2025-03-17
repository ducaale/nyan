import pygame

from .color import color_name_to_rgb
from .sprite import Sprite

class Rect(Sprite):
    def __init__(self, game, color, x, y, z, angle, width, height, border_color, border_width):
        self._width = width
        self._height = height
        self._color = color
        self._border_color = border_color
        self._border_width = border_width
        super().__init__(game, x, y, z, angle, 100)

    def _compute_primary_surface(self):
        surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        if self._border_width and self._border_color:
            surface.fill(color_name_to_rgb(self._border_color))
            pygame.draw.rect(
                surface,
                color_name_to_rgb(self._color),
                (
                    self._border_width,
                    self._border_width,
                    self._width - (self._border_width*2),
                    self._height - (self._border_width*2)
                )
            )
        else:
            surface.fill(color_name_to_rgb(self._color))
        return surface

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        self._primary_surface = self._compute_primary_surface()
        self._secondary_surface = self._compute_secondary_surface()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        self._primary_surface = self._compute_primary_surface()
        self._secondary_surface = self._compute_secondary_surface()

    @property 
    def color(self):
        return self._color

    @color.setter
    def color(self, _color):
        self._color = _color
        self._primary_surface = self._compute_primary_surface()
        self._secondary_surface = self._compute_secondary_surface()

    @property 
    def border_color(self):
        return self._border_color

    @border_color.setter
    def border_color(self, _border_color):
        self._border_color = _border_color
        self._primary_surface = self._compute_primary_surface()
        self._secondary_surface = self._compute_secondary_surface()

    @property 
    def border_width(self):
        return self._border_width

    @border_width.setter
    def border_width(self, _border_width):
        self._border_width = _border_width
        self._primary_surface = self._compute_primary_surface()
        self._secondary_surface = self._compute_secondary_surface()