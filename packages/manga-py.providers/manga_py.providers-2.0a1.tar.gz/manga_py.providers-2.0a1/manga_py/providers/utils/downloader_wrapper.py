from typing import Callable, Iterable

from .queue_wrapper import Wrapper

__all__ = ['Downloader']


class Downloader(Wrapper):
    def download(self, callback: Callable, urls: Iterable, *args, **kwargs):
        """
        callback: Callable
        def download_fn(url: str, *args, **kwargs):
            url == 'http://site/path/to/image.png'
            _idx == 0  # increment
            pass

        dl = Downloader()
        dl.download(download_fn, 'http://site/path/to/image.png')
        """
        for idx, url in enumerate(urls):
            kwargs.update({'_idx': idx})
            self.queue.put((callback, url, args, kwargs))
        self.queue.join()
