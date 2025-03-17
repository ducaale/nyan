import asyncio
import inspect

class TaskRunner():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.running_tasks = set()

    def run(self, func, *args):
        if (func, *args) in self.running_tasks:
            return False

        self.running_tasks.add((func, *args))
        def on_task_end(f): self.running_tasks.remove((func, *args))

        arg_count = len(inspect.signature(func).parameters)
        if arg_count == 0:
            future = self.loop.create_task(func())
        else:
            future = self.loop.create_task(func(*args))

        future.add_done_callback(on_task_end)
        return True
