import asyncio

class TaskRunner():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.running_tasks = set()

    def run(self, task, *args):
        if (task, *args) in self.running_tasks:
            return False

        self.running_tasks.add((task, *args))
        def on_task_end(f): self.running_tasks.remove((task, *args))
        future = self.loop.create_task(task(*args))
        future.add_done_callback(on_task_end)
        return True
