import os
import pygame.mixer

class Sound():
    def __init__(self, sound):
        self.sound = pygame.mixer.Sound(os.path.join('assets', sound))

    def play(self):
        self.sound.play()