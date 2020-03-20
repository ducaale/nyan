import asyncio

class TaskRunner():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.running_tasks = set()
    
    def run(self, task, *args, **kwargs):
        if task in self.running_tasks:
            return False

        self.running_tasks.add(task)
        def on_task_end(f): self.running_tasks.remove(task)
        future = self.loop.create_task(task(*args, **kwargs))
        future.add_done_callback(on_task_end)
        return True
