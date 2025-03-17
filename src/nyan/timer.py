import pygame

class Timer:
    def __init__(self):
        self.reset()

    @property
    def seconds(self):
        return self.milliseconds / 1000

    @property
    def milliseconds(self):
        return (pygame.time.get_ticks() - self._start_time)

    def reset(self):
        self._start_time = pygame.time.get_ticks()

def new_timer():
    return Timer()