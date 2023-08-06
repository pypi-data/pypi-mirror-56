from queue import Queue
from threading import Thread

__all__ = ['Wrapper']


class Wrapper:
    _queue: Queue

    class Daemon(Thread):
        def __init__(self, queue):
            super().__init__()
            self.queue = queue

        def run(self):
            while True:
                callback, url, args, kwargs = self.queue.get()
                callback(url, *args, **kwargs)
                self.queue.task_done()

    def __init__(self):
        self._queue = Queue()

        try:
            from multiprocessing import cpu_count
            max_threads = cpu_count()
        except ImportError:
            max_threads = 2

        for i in range(max_threads):
            t = self.Daemon(self._queue)
            t.setDaemon(True)
            t.start()

    @property
    def queue(self) -> Queue:
        return self._queue
