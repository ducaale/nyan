from collections import defaultdict

from .utils import make_async

class CustomEvent():
    def __init__(self, task_runner):
        self.broadcasted_events = set()
        self.callbacks = defaultdict(list)
        self.task_runner = task_runner

    def broadcast(self, event):
        self.broadcasted_events.add(event)

    def when_event_recieved(self, event):
        def decorator(func):
            self.callbacks[event].append(make_async(func))
            return func
        return decorator

    def invoke_callbacks(self):
        for event in self.broadcasted_events:
            for callback in self.callbacks[event]:
                self.task_runner.run(callback)

        self.broadcasted_events.clear()