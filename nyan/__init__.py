__version__ = '0.1.0'

import asyncio as _asyncio

import pygame as _pygame

from .game import Game as _Game
from .screen import Screen as _Screen
from .mouse import Mouse as _Mouse
from .keyboard import Keyboard as _Keyboard
from .sound import Sound as _Sound
from .task_runner import TaskRunner as _TaskRunner
from .sprite import Sprite as _Sprite
from .text import Text as _Text
from .rect import Rect as _Rect
from .circle import Circle as _Circle
from .random import Random as _Random

_pygame.init()
_task_runner = _TaskRunner()
screen = _Screen()
mouse = _Mouse(_task_runner)
_keyboard = _Keyboard(_task_runner)
_random = _Random(screen)
_game = _Game(_task_runner, screen, mouse, _keyboard)

when_mouse_clicked = mouse.when_clicked
when_mouse_click_released = mouse.when_click_released

key_is_pressed = _keyboard.key_is_pressed
when_key_pressed = _keyboard.when_key_pressed
when_key_released = _keyboard.when_key_released
when_any_key_pressed = _keyboard.when_any_key_pressed
when_any_key_released = _keyboard.when_any_key_released

random_color = _random.random_color
random_number = _random.random_number
random_position = _random.random_position

get_sprites = _game.get_sprites

def new_sprite(image, x=0, y=0, z=0, angle=0):
    return _Sprite(_game, image, x, y, z, angle)

def new_text(text, x=0, y=0, z=0, angle=0, font=None, font_size=50, color='black'):
    return _Text(_game, text, x, y, z, angle, font, font_size, color)

def new_rect(color='black', x=0, y=0, z=0, angle=0, width=100, height=200, border_color='light blue', border_width=0):
    return _Rect(_game, color, x, y, z, angle, width, height, border_color, border_width)

def new_circle(color='black', x=0, y=0, z=0, angle=0, radius=100, border_color='light blue', border_width=0):
    return _Circle(_game, color, x, y, z, angle, radius, border_color, border_width)

def new_sound(sound):
    return _Sound(sound)

def when_program_starts(func):
    _game.register_when_program_starts_callbacks(func)
    return func

def repeat_forever(func):
    _game.register_forever_callback(func)
    return func

async def timer(seconds=1.0):
    await _asyncio.sleep(seconds)
    return True

def start_program():
    _game.invoke_when_program_starts_callbacks()
    _task_runner.loop.call_soon(_game.run)
    try:
        _task_runner.loop.run_forever()
    finally:
        _pygame.quit()

"""
1. TODO: implement @foreach_sprite(tag=None) decorator
this will be used for attaching a script to multiple sprites at once.
this will be particularly useful for forever loops that should be
running independently for each sprite

2. TODO: maybe a camera should be implemented? should be useful for things
like screen shake.

3. TODO: add scratch effects such as fisheye, whirl, pixlate, etc

4. TODO: add flappy bird example
"""
