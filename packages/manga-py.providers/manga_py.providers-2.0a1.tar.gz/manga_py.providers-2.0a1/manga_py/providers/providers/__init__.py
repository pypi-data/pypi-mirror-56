from typing import List

from .readmanga_me import ReadMangaMe
from ..exceptions import ProviderNotFoundError

providers = [
    ReadMangaMe,
]


def get_providers(url: str) -> List:
    """
    Returns a list of provider instances
    """
    _providers = []
    for provider in providers:
        if provider.is_supported(url):
            _providers.append(provider)
    if len(_providers) < 1:
        raise ProviderNotFoundError()
    return _providers


__all__ = ['providers', 'get_providers']
