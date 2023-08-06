from urllib.parse import urlparse

__all__ = ['url2name', ]


def url2name(url: str) -> str:
    path = urlparse(url).path
    name = path[path.find('/') + 1:].rstrip('/')
    if len(name) < 1:
        raise RuntimeError('Name has empty')
    return name
