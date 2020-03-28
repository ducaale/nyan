import sys

import pygame

from .utils import make_async

class Game():
    def __init__(self, task_runner, sprite_manager, screen, mouse, keyboard, custom_event):
        self.task_runner = task_runner
        self.sprite_manager = sprite_manager
        self.screen = screen
        self.mouse = mouse
        self.keyboard = keyboard
        self.custom_event = custom_event

        self.when_program_starts_callbacks = []
        self.forever_callbacks = []
        self.clock = pygame.time.Clock()

    def register_when_program_starts_callbacks(self, func):
        self.when_program_starts_callbacks.append(make_async(func))

    def register_forever_callback(self, func):
        self.forever_callbacks.append(make_async(func))

    def invoke_when_program_starts_callbacks(self):
        for callback in self.when_program_starts_callbacks:
            if hasattr(callback, 'tags'):
                for sprite in self.sprite_manager.get_sprites(*callback.tags):
                    self.task_runner.run(callback, sprite)
            else:
                self.task_runner.run(callback)

    def invoke_forever_callbacks(self):
        for callback in self.forever_callbacks:
            if hasattr(callback, 'tags'):
                for sprite in self.sprite_manager.get_sprites(*callback.tags):
                    self.task_runner.run(callback, sprite)
            else:
                self.task_runner.run(callback)

    def handle_events(self):
        self.mouse._clear_frame_events()
        self.keyboard.clear_frame_events()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse._register_click_event()
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse._register_click_release_event()
            if event.type == pygame.MOUSEMOTION:
                self.mouse.x = (event.pos[0] - self.screen.width/2.)
                self.mouse.y = (self.screen.height/2. - event.pos[1])
            if event.type == pygame.KEYDOWN:
                self.keyboard.register_key_down_event(event)
            if event.type == pygame.KEYUP:
                self.keyboard.register_key_up_event(event)

    def invoke_callbacks(self):
        self.mouse._invoke_callbacks(self.task_runner)
        self.keyboard.invoke_callbacks(self.task_runner)
        self.custom_event.invoke_callbacks(self.task_runner)
        self.invoke_forever_callbacks()

    def draw(self):
        self.screen._surface.fill((128, 128, 128))
        self.sprite_manager.draw(self.screen)
        pygame.display.flip()

    def run(self):
        self.clock.tick(60)
        self.handle_events()
        self.invoke_callbacks()
        self.draw()
        self.task_runner.loop.call_soon(self.run)