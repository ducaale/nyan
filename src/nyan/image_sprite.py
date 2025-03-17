import os

import pygame

from .sprite import Sprite

class ImageSprite(Sprite):
    def __init__(self, game, image, x, y, z, angle, size):
        self._image = image
        super().__init__(game, x, y, z, angle, size)

    def _compute_primary_surface(self):
        return pygame.image.load(os.path.join('assets', self._image)).convert_alpha()
 
    @property
    def image(self):
        return image

    @image.setter
    def image(self, image):
        self._image = image
        self._primary_surface = self._compute_primary_surface()
        self._secondary_surface = self._compute_secondary_surface()