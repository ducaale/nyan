import asyncio
import os

import pygame.mixer_music

class Music():
    def play(self, music, loop=False):
        pygame.mixer_music.load(os.path.join('assets', music))
        if loop:
            pygame.mixer_music.play(-1)
        else:
            pygame.mixer_music.play(0)

    async def play_until_done(self, music):
        self.play(music)
        while pygame.mixer_music.get_busy():
            await asyncio.sleep(0)

    def stop(self):
        pygame.mixer_music.stop()

    def pause(self):
        pygame.mixer_music.pause()

    def unpause(self):
        pygame.mixer_music.unpause()

    @property
    def volume(self):
        return pygame.mixer_music.get_volume() * 100

    @volume.setter
    def volume(self, value):
        pygame.mixer_music.set_volume(value/100)