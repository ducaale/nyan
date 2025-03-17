import pygame

from .color import color_name_to_rgb
from .sprite import Sprite

class Circle(Sprite):
    def __init__(self, game, color, x, y, z, angle, radius, border_color, border_width):
        self._radius = radius
        self._color = color
        self._border_color = border_color
        self._border_width = border_width
        super().__init__(game, x, y, z, angle, 100)

    def _compute_primary_surface(self):
        total_diameter = (self._radius + self._border_width) * 2
        surface = pygame.Surface((total_diameter, total_diameter), pygame.SRCALPHA)
        center = self._radius + self._border_width
        if self._border_width and self._border_color:
            pygame.draw.circle(
                surface, color_name_to_rgb(self._border_color), (center, center), self._radius)
            pygame.draw.circle(
                surface, color_name_to_rgb(self._color), (center, center), self._radius - self._border_width)
        else:
            pygame.draw.circle(surface, color_name_to_rgb(self._color), (center, center), self._radius)
        return surface

    @property 
    def color(self):
        return self._color

    @color.setter
    def color(self, _color):
        self._color = _color
        self._primary_surface = self._compute_primary_surface()
        self._secondary_surface = self._compute_secondary_surface()

    @property 
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius
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