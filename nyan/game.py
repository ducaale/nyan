import sys
from collections import defaultdict

import pygame

from .utils import make_async

class Game():
    def __init__(self, task_runner, screen, mouse, keyboard):
        self.task_runner = task_runner
        self.screen = screen
        self.mouse = mouse
        self.keyboard = keyboard

        self.all_sprites = []
        self.sprite_groups = defaultdict(set)
        self.when_program_starts_callbacks = []
        self.forever_callbacks = []
        self.clock = pygame.time.Clock()

    def get_sprites(self, *tags):
        if len(tags) == 0:
            return self.all_sprites
        elif len(tags) == 1:
            return self.sprite_groups[tags[0]]
        else:
            sprites = set()
            for tag in tags:
                sprites |= self.sprite_groups[tag]
            return sprites

    def add_sprite_to_group(self, sprite, group):
        self.sprite_groups[group].add(sprite)

    def remove_sprite_from_group(self, sprite, group):
        self.sprite_groups[group].remove(sprite)

    def register_sprite(self, sprite):
        self.all_sprites.append(sprite)
        for tag in sprite._tags:
            self.add_sprite_to_group(sprite, tag)

    def unregister_sprite(self, sprite):
        self.all_sprites.remove(sprite)
        for tag in sprite._tags:
            self.remove_sprite_from_group(sprite, tag)

    def register_when_program_starts_callbacks(self, func):
        self.when_program_starts_callbacks.append(make_async(func))

    def register_forever_callback(self, func):
        self.forever_callbacks.append(make_async(func))
    
    def invoke_when_program_starts_callbacks(self):
        for callback in self.when_program_starts_callbacks:
            self.task_runner.run(callback)
    
    def invoke_forever_callbacks(self):
        for callback in self.forever_callbacks:
            self.task_runner.run(callback)

    def handle_events(self):
        self.mouse._clear_release_events()
        self.keyboard.clear_release_events()
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
        self.mouse._invoke_callbacks()
        self.keyboard.invoke_callbacks()
        self.invoke_forever_callbacks()

    def draw(self):
        self.screen._surface.fill((0, 0, 0))
        self.all_sprites = sorted(self.all_sprites, key=lambda sprite: sprite.z)
        for sprite in self.all_sprites: sprite._draw(self.screen)
        pygame.display.flip()
    
    def run(self):
        self.clock.tick(60)
        self.handle_events()
        self.invoke_callbacks()
        self.draw()
        self.task_runner.loop.call_soon(self.run)