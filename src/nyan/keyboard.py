from collections import defaultdict

import pygame

from .utils import make_async

ANY_KEY = 'any_key'

class Keyboard():
    def __init__(self):
        self.pressed_keys = set()
        self.released_keys = set()
        self.keys_pressed_this_frame = set()
        self.keypress_callbacks = defaultdict(list)
        self.keyrelease_callbacks = defaultdict(list)

    def register_key_down_event(self, event):
        if event.key in key_map:
            self.pressed_keys.add(pygame_key_to_name(event))
            self.keys_pressed_this_frame.add(pygame_key_to_name(event))

    def register_key_up_event(self, event):
        if event.key in key_map:
            self.pressed_keys.remove(pygame_key_to_name(event))
            self.released_keys.add(pygame_key_to_name(event))

    def clear_frame_events(self):
        self.released_keys.clear()
        self.keys_pressed_this_frame.clear()

    def invoke_callbacks(self, task_runner):
        for key in self.keys_pressed_this_frame:
            for callback in self.keypress_callbacks[key]:
                task_runner.run(callback, key)
            for callback in self.keypress_callbacks[ANY_KEY]:
                task_runner.run(callback, key)

        for key in self.released_keys:
            for callback in self.keyrelease_callbacks[key]:
                task_runner.run(callback, key)
            for callback in self.keyrelease_callbacks[ANY_KEY]:
                task_runner.run(callback, key)

    def when_any_key_pressed(self, func):
        self.keypress_callbacks[ANY_KEY].append(make_async(func))
        return func

    def when_key_pressed(self, *keys):
        def decorator(func):
            for key in keys:
                self.keypress_callbacks[key].append(make_async(func))
            return func
        return decorator

    def when_any_key_released(self, func):
        self.keyrelease_callbacks[ANY_KEY].append(make_async(func))
        return func

    def when_key_released(self, *keys):
        def decorator(func):
            for key in keys:
                self.keyrelease_callbacks[key].append(make_async(func))
            return func
        return decorator

    def key_is_pressed(self, *keys):
        """
        Returns True if any of the given keys are pressed.
        Example:
        ```
        @nyan.repeat_forever
        async def do():
            if nyan.key_is_pressed('up', 'w'):
                print('up or w pressed')
        ```
        """
        for key in keys:
            if key in self.pressed_keys:
                return True
        return False

key_map = {
    pygame.K_BACKSPACE: 'backspace',
    pygame.K_TAB: 'tab',
    pygame.K_CLEAR: 'clear',
    pygame.K_RETURN: 'enter',
    pygame.K_PAUSE: 'pause',
    pygame.K_ESCAPE: 'escape',
    pygame.K_SPACE: 'space',
    pygame.K_EXCLAIM: '!',
    pygame.K_QUOTEDBL: '"',
    pygame.K_HASH: '#',
    pygame.K_DOLLAR: '$',
    pygame.K_AMPERSAND: '&',
    pygame.K_QUOTE: "'",
    pygame.K_LEFTPAREN: '(',
    pygame.K_RIGHTPAREN: ')',
    pygame.K_ASTERISK: '*',
    pygame.K_PLUS: '+',
    pygame.K_COMMA: ',',
    pygame.K_MINUS: '-',
    pygame.K_PERIOD: '.',
    pygame.K_SLASH: '/',
    pygame.K_0: '0',
    pygame.K_1: '1',
    pygame.K_2: '2',
    pygame.K_3: '3',
    pygame.K_4: '4',
    pygame.K_5: '5',
    pygame.K_6: '6',
    pygame.K_7: '7',
    pygame.K_8: '8',
    pygame.K_9: '9',
    pygame.K_COLON: ':',
    pygame.K_SEMICOLON: ';',
    pygame.K_LESS: '<',
    pygame.K_EQUALS: '=',
    pygame.K_GREATER: '>',
    pygame.K_QUESTION: '?',
    pygame.K_AT: '@',
    pygame.K_LEFTBRACKET: '[',
    pygame.K_BACKSLASH: '\\',
    pygame.K_RIGHTBRACKET: ']',
    pygame.K_CARET: '^',
    pygame.K_UNDERSCORE: '_',
    pygame.K_BACKQUOTE: '`',
    pygame.K_a: 'a',
    pygame.K_b: 'b',
    pygame.K_c: 'c',
    pygame.K_d: 'd',
    pygame.K_e: 'e',
    pygame.K_f: 'f',
    pygame.K_g: 'g',
    pygame.K_h: 'h',
    pygame.K_i: 'i',
    pygame.K_j: 'j',
    pygame.K_k: 'k',
    pygame.K_l: 'l',
    pygame.K_m: 'm',
    pygame.K_n: 'n',
    pygame.K_o: 'o',
    pygame.K_p: 'p',
    pygame.K_q: 'q',
    pygame.K_r: 'r',
    pygame.K_s: 's',
    pygame.K_t: 't',
    pygame.K_u: 'u',
    pygame.K_v: 'v',
    pygame.K_w: 'w',
    pygame.K_x: 'x',
    pygame.K_y: 'y',
    pygame.K_z: 'z',
    pygame.K_DELETE: 'delete',
    pygame.K_UP: 'up',
    pygame.K_DOWN: 'down',
    pygame.K_RIGHT: 'right',
    pygame.K_LEFT: 'left',
    pygame.K_INSERT: 'insert',
    pygame.K_HOME: 'home',
    pygame.K_END: 'end',
    pygame.K_PAGEUP: 'pageup',
    pygame.K_PAGEDOWN: 'pagedown',
    pygame.K_F1: 'F1',
    pygame.K_F2: 'F2',
    pygame.K_F3: 'F3',
    pygame.K_F4: 'F4',
    pygame.K_F5: 'F5',
    pygame.K_F6: 'F6',
    pygame.K_F7: 'F7',
    pygame.K_F8: 'F8',
    pygame.K_F9: 'F9',
    pygame.K_F10: 'F10',
    pygame.K_F11: 'F11',
    pygame.K_F12: 'F12',
    pygame.K_F13: 'F13',
    pygame.K_F14: 'F14',
    pygame.K_F15: 'F15',
    pygame.K_NUMLOCK: 'numlock',
    pygame.K_CAPSLOCK: 'capslock',
    pygame.K_SCROLLOCK: 'scrollock',
    pygame.K_RSHIFT: 'shift',
    pygame.K_LSHIFT: 'shift',
    pygame.K_RCTRL: 'control',
    pygame.K_LCTRL: 'control',
    pygame.K_RALT: 'alt',
    pygame.K_LALT: 'alt',
    pygame.K_RMETA: 'meta',
    pygame.K_LMETA: 'meta',
    pygame.K_LSUPER: 'super',
    pygame.K_RSUPER: 'super',
    pygame.K_EURO: '€',
}

def pygame_key_to_name(pygame_key_event):
    return key_map[pygame_key_event.key]