import math

from .utils import point_touching_sprite, make_async

class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.is_clicked = False
        self.is_click_relased = False
        self._is_clicked_this_frame = False
        self._when_clicked_callbacks = []
        self._when_click_released_callbacks = []

    def _register_click_event(self):
        self.is_clicked = True
        self._is_clicked_this_frame = True

    def _register_click_release_event(self):
        self.is_clicked = False
        self.is_click_relased = True

    def _clear_frame_events(self):
        self.is_click_relased = False
        self._is_clicked_this_frame = False

    def _invoke_callbacks(self, task_runner):
        if self._is_clicked_this_frame:
            for callback in self._when_clicked_callbacks:
                task_runner.run(callback)

        if self.is_click_relased:
            for callback in self._when_click_released_callbacks:
                task_runner.run(callback)

    def is_touching(self, other):
        if self.is_hidden: return False

        return point_touching_sprite(self, other)

    def when_clicked(self, func):
        self._when_clicked_callbacks.append(make_async(func))
        return func

    def when_click_released(self, func):
        self._when_click_released_callbacks.append(make_async(func))
        return func

    def distance_to(self, x, y=None):
        try:
            # x can either by a number or a sprite. If it's a sprite:
            x = x.x
            y = x.y
        except AttributeError:
            x = x
            y = y

        dx = self.x - x
        dy = self.y - y

        return math.sqrt(dx**2 + dy**2)