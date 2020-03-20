import math
from abc import ABC, abstractmethod
from copy import copy

import pygame

from .utils import clamp, change_alpha, sprite_touching_sprite, point_touching_sprite

class Drawable2D(ABC):
    def __init__(self, game, x, y, z, angle):
        self._game = game
        self.x = x
        self.y = y
        self.z = z
        self._angle = angle
        self._size = 100
        self._transparency = 100

        self.is_clicked = False
        self.is_hidden = False
        self._tags = set()

        self._primary_surface = self._compute_primary_surface()
        self._secondary_surface = self._compute_secondary_surface()
        self._game.register_sprite(self)

    @abstractmethod
    def _compute_primary_surface(self):
        pass

    def _compute_secondary_surface(self):
        surface = pygame.transform.rotate(self._primary_surface, self._angle)
        surface = pygame.transform.scale(
            surface,
            (round(surface.get_width() * (self._size/100)),
            round(surface.get_height() * (self._size/100)))
        )
        change_alpha(surface, round((self._transparency/100) * 255))
        return surface

    def add_tag(self, tag):
        self._tags.add(tag)
        self._game.add_sprite_to_group(self, tag)
 
    def remove_tag(self, tag):
        self._tags.remove(tag)
        self._game.remove_sprite_from_group(self, tag)

    def clone(self):
        clone = copy(self)
        clone._tags = clone._tags.copy()
        self._game.register_sprite(clone)
        return clone

    def remove(self):
        self._game.unregister_sprite(self)

    @property 
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self._secondary_surface = self._compute_secondary_surface()

    @property 
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = clamp(size, 0, math.inf)
        self._secondary_surface = self._compute_secondary_surface()

    @property
    def transparency(self):
        return self._transparency

    @transparency.setter
    def transparency(self, alpha):
        self._transparency = clamp(alpha, 0, 100)
        self._secondary_surface = self._compute_secondary_surface()
    
    def move(self, steps):
        angle = math.radians(self._angle)
        self.x += steps * math.cos(angle)
        self.y += steps * math.sin(angle)

    def turn(self, degrees):
        self._angle = (self._angle + degrees) % 360
        self._secondary_surface = self._compute_secondary_surface()
    
    def hide(self):
        self.is_hidden = True

    def show(self):
        self.is_hidden = False

    @property
    def is_shown(self):
        return not self._is_hidden

    @is_shown.setter
    def is_shown(self, show):
        self._is_hidden = not show

    def is_touching(self, sprite_or_point):
        if isinstance(sprite_or_point, Drawable2D):
            return sprite_touching_sprite(sprite_or_point, self)
        else:
            return point_touching_sprite(sprite_or_point, self)

    def point_towards(self, x, y=None):
        try:
            # x can either be a number or a sprite. If it's a sprite:
            x, y = x.x, x.y
        except AttributeError:
            x, y = x, y
        self._angle = math.degrees(math.atan2(y - self.y, x - self.x))

    def go_to(self, x, y=None):
        try:
            # x can either be a number or a sprite. If it's a sprite:
            self.x = x.x
            self.y = x.y
        except AttributeError:
            self.x = x
            self.y = y

    def distance_to(self, x, y=None):
        try:
            # x can either be a number or a sprite. If it's a sprite:
            x1 = x.x
            y1 = x.y
        except AttributeError:
            x1 = x
            y1 = y

        dx = self.x - x1
        dy = self.y - y1

        return math.sqrt(dx**2 + dy**2)

    @property
    def width(self):
        return self._secondary_surface.get_width()

    @property
    def height(self):
        return self._secondary_surface.get_height()

    @property
    def right(self):
        return self.x + self.width / 2

    @right.setter
    def right(self, x):
        self.x = x - self.width / 2

    @property
    def left(self):
        return self.x - self.width / 2

    @left.setter
    def left(self, x):
        self.x = x + self.width / 2

    @property
    def top(self):
        return self.y + self.height / 2

    @top.setter
    def top(self, y):
        self.y = y - self.height / 2

    @property
    def bottom(self):
        return self.y - self.height / 2

    @bottom.setter
    def bottom(self, y):
        self.y = y + self.height / 2

    # replace screen with camera object
    def _draw(self, screen):
        if self.is_hidden: return
        x = self.x + (screen.width/2) - (self.width/2)
        y = (screen.height/2) - self.y - (self.height/2)
        screen._surface.blit(self._secondary_surface, (x, y))