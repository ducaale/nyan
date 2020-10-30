from functools import partial

def add_animations(sprite, images, animations):
    def set_animation(sprite, name):
        animation = sprite.animations[name]
        if animation == sprite.current_animation: return
        sprite.current_frame = 0
        sprite.current_animation = animation
        sprite.image = sprite.images[sprite.current_animation[sprite.current_frame]]

    def is_current_animation(sprite, animation):
        return sprite.current_animation == sprite.animations[animation]

    def next_frame(sprite):
        sprite.current_frame = (sprite.current_frame + 1) % len(sprite.current_animation)
        sprite.image = sprite.images[sprite.current_animation[sprite.current_frame]]

    def is_last_frame(sprite):
        return sprite.current_frame == len(sprite.current_animation) - 1

    sprite.images = images
    sprite.animations = animations

    sprite.current_frame = 0
    sprite.animations['default'] = [0]
    sprite.current_animation = sprite.animations['default']

    sprite.set_animation = partial(set_animation, sprite)
    sprite.is_current_animation = partial(is_current_animation, sprite)
    sprite.next_frame = partial(next_frame, sprite)
    sprite.is_last_frame = partial(is_last_frame, sprite)