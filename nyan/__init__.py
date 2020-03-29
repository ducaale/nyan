__version__ = '0.1.0'

import asyncio as _asyncio

import pygame as _pygame

from .game import Game as _Game
from .sprite_manager import SpriteManager as _SpriteManager
from .screen import Screen as _Screen
from .mouse import Mouse as _Mouse
from .keyboard import Keyboard as _Keyboard
from .custom_event import CustomEvent as _CustomEvent
from .sound import Sound as _Sound
from .music import Music as _Music
from .task_runner import TaskRunner as _TaskRunner
from .sprite import Sprite as _Sprite
from .text import Text as _Text
from .rect import Rect as _Rect
from .circle import Circle as _Circle
from .random import Random as _Random
from .timer import new_timer

_pygame.init()

_task_runner = _TaskRunner()
screen = _Screen()
mouse = _Mouse()
_keyboard = _Keyboard()
_custom_event = _CustomEvent()
_random = _Random(screen)
_sprite_manager = _SpriteManager()
music = _Music()
_game = _Game(_task_runner, _sprite_manager, screen, mouse, _keyboard, _custom_event)

when_mouse_clicked = mouse.when_clicked
when_mouse_click_released = mouse.when_click_released

key_is_pressed = _keyboard.key_is_pressed
when_key_pressed = _keyboard.when_key_pressed
when_key_released = _keyboard.when_key_released
when_any_key_pressed = _keyboard.when_any_key_pressed
when_any_key_released = _keyboard.when_any_key_released

broadcast = _custom_event.broadcast
when_event_recieved = _custom_event.when_event_recieved

random_color = _random.random_color
random_number = _random.random_number
random_position = _random.random_position

get_sprites = _sprite_manager.get_sprites

def _position_sprite(sprite, top, bottom, right, left):
    if top is not None: sprite.top = top
    if bottom is not None: sprite.bottom = bottom
    if left is not None: sprite.left = left
    if right is not None: sprite.right = right
    return sprite

def new_sprite(
    image, x=0, y=0, z=0, top=None, bottom=None, right=None, left=None, angle=0,
    size=100, is_hidden=False
):
    sprite = _Sprite(_sprite_manager, image, x, y, z, angle, size)
    _position_sprite(sprite, top, bottom, right, left)
    sprite.is_hidden = is_hidden
    return sprite

def new_text(
    text, x=0, y=0, z=0, top=None, bottom=None, right=None, left=None, angle=0,
    font=None, font_size=50, color='black', is_hidden=False
):
    text = _Text(_sprite_manager, text, x, y, z, angle, font, font_size, color)
    _position_sprite(text, top, bottom, right, left)
    text.is_hidden = is_hidden
    return text

def new_rect(
    color='black', x=0, y=0, z=0, top=None, bottom=None, right=None, left=None,
    angle=0, width=100, height=200, border_color='light blue', border_width=0, is_hidden=False
):
    rect = _Rect(
        _sprite_manager, color, x, y, z, angle, width, height, border_color, border_width
    )
    _position_sprite(rect, top, bottom, right, left)
    rect.is_hidden = is_hidden
    return rect

def new_circle(
    color='black', x=0, y=0, z=0, top=None, bottom=None, right=None, left=None,
    angle=0, radius=100, border_color='light blue', border_width=0, is_hidden=False
):
    circle = _Circle(_sprite_manager, color, x, y, z, angle, radius, border_color, border_width)
    _position_sprite(circle, top, bottom, right, left)
    circle.is_hidden = is_hidden
    return circle

def new_sound(sound):
    return _Sound(sound)

def when_program_starts(func):
    """
    Call code right when the program starts.
    Used like this:
    ```
    @nyan.when_program_starts
    def do():
        print('the program just started!')
    ```
    """
    _game.register_when_program_starts_callbacks(func)
    return func

def repeat_forever(func):
    """
    Calls the given function repeatedly in the game loop.
    Example:
    ```
    text = nyan.new_text('hello world')
    @nyan.repeat_forever
    async def do():
        text.turn(degrees=15)
    ```
    """
    _game.register_forever_callback(func)
    return func

"""
TODO: determine the best name for this function. these are the current
candidates, other names are also welcome:

- @foreach_sprite_with_tag('player', 'bullet')
- @foreach_sprite('player', 'player')
- @foreach('player', 'bullet')

I am leaning toward the first one, but the name is somewhat confusing
when multiple tags are passed. for example, will this function
`@foreach_sprite_with_tag('player', 'bullet')` return sprites that has
both tags or one of them?
"""
def foreach_sprite(tags=[]):
    """
    Calls the given function for each sprite that has any of the passed tags.
    To be used in conjunction with `@repeat_forever` and `@when_program_starts`
    decorators. Example:
    ```
    @nyan.repeat_forever
    @nyan.foreach_sprite(tags=['projectile'])
    async def propel_projectile(projectile):
        projectile.move(25)
    ```
    """
    def decorator(func):
        func.tags = tags
        return func
    return decorator

async def sleep(seconds=1.0):
    """
    Wait a number of seconds. Used with the await keyword like this:
    ```
    @nyan.repeat_forever
    async def do():
        await nyan.sleep(seconds=2)
        print('hi')
    ```
    """
    await _asyncio.sleep(seconds)

def start_program():
    """
    Calling this function starts your program running.
    `nyan.start_program()` should almost certainly go at the very end of your program.
    """
    _game.invoke_when_program_starts_callbacks()
    _task_runner.loop.call_soon(_game.run)
    try:
        _task_runner.loop.run_forever()
    finally:
        _pygame.quit()