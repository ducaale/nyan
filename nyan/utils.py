import asyncio
from functools import wraps

def clamp(num, lowest, highest):
    return min(max(num, lowest), highest)

def point_touching_sprite(point, sprite):
    return sprite.left <= point.x <= sprite.right and sprite.bottom <= point.y <= sprite.top

def sprite_touching_sprite(a, b):
    if a.left >= b.right or a.right <= b.left or a.top <= b.bottom or a.bottom >= b.top:
        return False
    return True

def make_async(func):
    if asyncio.iscoroutinefunction(func): return func
    @wraps(func)
    async def async_func(*args, **kwargs):
        return func(*args, **kwargs)
    return async_func