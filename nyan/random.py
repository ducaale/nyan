import random
from collections import namedtuple

Position = namedtuple('Position', ['x', 'y'])

class Random():
    def __init__(self, screen):
        self.screen = screen

    def random_number(self, lowest=0, highest=100):
        # if user supplies whole numbers, return whole numbers
        if type(lowest) == int and type(highest) == int:
            return random.randint(lowest, highest)
        else:
            # if user supplied any floats, return decimals
            return round(random.uniform(lowest, highest), 2)

    def random_color(self):
        return (
            self.random_number(0, 255),
            self.random_number(0, 255),
            self.random_number(0, 255)
        )

    def random_position(self):
        """
        Returns a random position on the screen. A position has an `x` and `y` e.g.:
        ```
        position = nyan.random_position()
        sprite.x = position.x
        sprite.y = position.y
        ```
        or equivalently:
        ```
        sprite.go_to(nyan.random_position())
        ```
        """
        return Position(
            self.random_number(self.screen.left, self.screen.right),
            self.random_number(self.screen.bottom, self.screen.top)
        )
 
    def random_item(self, items):
        assert len(items) > 0
        return items[self.random_number(0, len(items)-1)]