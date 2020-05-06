import math
from collections import namedtuple

from .rect import Rect

Point = namedtuple('Point', ['x', 'y'])

class Line(Rect):
    def __init__(self, game, color, x1, y1, x2, y2, z, thickness):
        self._point1 = Point(x1, y1)
        self._point2 = Point(x2, y2)
        super().__init__(
            game, color, x=0, y=0, z=z, angle=90, width=1, height=thickness,
            border_color='light blue', border_width=0
        )
        self._recompute_line()

    def _recompute_line(self):
        def distance(point1, point2):
            dx = point1.x - point2.x
            dy = point1.y - point2.y
            return math.sqrt(dx**2 + dy**2)
        
        def midpoint(point1, point2):
            return (point1.x + point2.x)/2, (point1.y + point2.y)/2
        
        def angle(point1, point2):
            return math.degrees(math.atan2(point1.y - point2.y, point1.x - point2.x))

        self.go_to(*midpoint(self._point1, self._point2))
        length = distance(self._point1, self._point2)
        if length > 1:
            self.width = length
            self.angle = angle(self._point1, self._point2)

    @property 
    def x1(self):
        return self._point1.x

    @x1.setter
    def x1(self, x1):
        self._point1 = self._point1._replace(x=x1)
        self._recompute_line()

    @property 
    def y1(self):
        return self._point1.y

    @y1.setter
    def y1(self, y1):
        self._point1 = self._point1._replace(y=y1)
        self._recompute_line()

    @property 
    def x2(self):
        return self._point2.x

    @x2.setter
    def x2(self, x2):
        self._point2 = self._point2._replace(x=x2)
        self._recompute_line()

    @property 
    def y2(self):
        return self._point2.y

    @y2.setter
    def y2(self, y2):
        self._point2 = self._point2._replace(y=y2)
        self._recompute_line()