from collections import defaultdict

class SpriteManager():
    def __init__(self):
        self.all_sprites = []
        self.sprite_groups = defaultdict(set)

    def get_sprites(self, *, tag=None):
        if tag is None:
            return self.all_sprites.copy()
        else:
            return self.sprite_groups[tag].copy()

    def add_sprite_to_group(self, sprite, group):
        self.sprite_groups[group].add(sprite)

    def remove_sprite_from_group(self, sprite, group):
        self.sprite_groups[group].remove(sprite)

    def register_sprite(self, sprite):
        self.all_sprites.append(sprite)
        for tag in sprite._tags:
            self.add_sprite_to_group(sprite, tag)

    def unregister_sprite(self, sprite):
        try:
            self.all_sprites.remove(sprite)
            for tag in sprite._tags:
                self.remove_sprite_from_group(sprite, tag)
        except ValueError:
            pass

    def invoke_callbacks(self, task_runner, mouse):
        if not mouse._is_clicked_this_frame: return

        for sprite in self.all_sprites:
            if sprite.is_touching(mouse) and sprite.is_shown:
                sprite._invoke_when_clicked_callbacks(task_runner)

    def draw(self, screen):
        self.all_sprites = sorted(self.all_sprites, key=lambda sprite: sprite.z)
        for sprite in self.all_sprites:
            sprite._draw(screen)
