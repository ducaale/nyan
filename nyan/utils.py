import asyncio

import numpy
import pygame

def clamp(num, min_, max_):
    if num < min_:
        return min_
    elif num > max_:
        return max_
    return num

def point_touching_sprite(point, sprite):
    return sprite.left <= point.x <= sprite.right and sprite.bottom <= point.y <= sprite.top

def sprite_touching_sprite(a, b):
    if a.left >= b.right or a.right <= b.left or a.top <= b.bottom or a.bottom >= b.top:
        return False
    return True

def make_async(func):
    if asyncio.iscoroutinefunction(func): return func
    async def async_func(*args, **kwargs):
        return func(*args, **kwargs)
    return async_func

# https://stackoverflow.com/a/35632748/5915221
def change_alpha(img, alpha):
    chan = pygame.surfarray.pixels_alpha(img)
    chan2 = numpy.minimum(chan, numpy.ones(chan.shape, dtype=chan.dtype)) * alpha
    numpy.copyto(chan, chan2)
    del chan