import math
from abc import ABC, abstractmethod
from copy import copy

import pygame

from .utils import clamp, sprite_touching_sprite, point_touching_sprite, make_async

class Sprite(ABC):
    def __init__(self, game, x, y, z, angle, size):
        self._game = game
        self.x = x
        self.y = y
        self.z = z
        self._angle = angle

        self._size = size
        self._transparency = 100
        self._brightness = 0

        self.is_hidden = False
        self.is_dead = False
        self._tags = set()
        self._when_clicked_callbacks = []

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
        scaled_transparency = round((self._transparency/100) * 255)
        surface.fill((255, 255, 255, scaled_transparency), special_flags=pygame.BLEND_RGBA_MULT)

        scaled_brightness = round((abs(self._brightness)/100) * 255)
        brightness_blend_mode = pygame.BLEND_RGB_ADD if self._brightness > 0 else pygame.BLEND_RGB_SUB
        surface.fill((scaled_brightness, scaled_brightness, scaled_brightness), special_flags=brightness_blend_mode)

        return surface

    def _invoke_when_clicked_callbacks(self, task_runner):
        if self.is_hidden or self.is_dead: return False

        for callback in self._when_clicked_callbacks:
            try:
                iterator = iter(callback)
            except TypeError:
                task_runner.run(callback)
            else:
                task_runner.run(*callback)

    def when_clicked(self, callback, call_with_sprite=False):
        if call_with_sprite:
            self._when_clicked_callbacks.append((make_async(callback), self))
        else:
            self._when_clicked_callbacks.append(make_async(callback))

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
        self.is_dead = True
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
    def transparency(self, amount):
        self._transparency = clamp(amount, 0, 100)
        self._secondary_surface = self._compute_secondary_surface()

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = clamp(value, -100, 100)
        self._secondary_surface = self._compute_secondary_surface()

    def move(self, steps, direction=None):
        if direction is None:
            angle = math.radians(self.angle)
        else:
            angle = math.radians(direction)
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
        return not self.is_hidden

    @is_shown.setter
    def is_shown(self, show):
        self.is_hidden = not show

    def is_touching(self, sprite_or_point):
        if self.is_hidden or self.is_dead: return False

        if isinstance(sprite_or_point, Sprite):
            if sprite_or_point.is_hidden or sprite_or_point.is_dead:
                return False
            return sprite_touching_sprite(sprite_or_point, self)
        else:
            return point_touching_sprite(sprite_or_point, self)

    def point_towards(self, x, y=None):
        try:
            # x can either be a number or a sprite. If it's a sprite:
            x, y = x.x, x.y
        except AttributeError:
            x, y = x, y
        self.angle = math.degrees(math.atan2(y - self.y, x - self.x))

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

    def _surface_width(self):
        return self._secondary_surface.get_width()

    def _surface_height(self):
        return self._secondary_surface.get_height()

    @property
    def right(self):
        return self.x + self._surface_width() / 2

    @right.setter
    def right(self, x):
        self.x = x - self._surface_width() / 2

    @property
    def left(self):
        return self.x - self._surface_width() / 2

    @left.setter
    def left(self, x):
        self.x = x + self._surface_width() / 2

    @property
    def top(self):
        return self.y + self._surface_height() / 2

    @top.setter
    def top(self, y):
        self.y = y - self._surface_height() / 2

    @property
    def bottom(self):
        return self.y - self._surface_height() / 2

    @bottom.setter
    def bottom(self, y):
        self.y = y + self._surface_height() / 2

    # replace screen with camera object
    def _draw(self, screen):
        if self.is_hidden: return
        x = self.x + (screen.width/2) - (self._surface_width()/2)
        y = (screen.height/2) - self.y - (self._surface_height()/2)
        screen._surface.blit(self._secondary_surface, (x, y))