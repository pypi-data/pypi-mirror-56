import re
from enum import Enum
from pathlib import Path
from typing import NamedTuple, List, Optional, Union, Tuple

from .utils.request_utils import url2name

__all__ = ['Image', 'Archive', 'Chapter', 'Meta', 'LocalImage', 'ImageTypes']


class ImageTypes(Enum):
    NORMAL: int = 0
    ENCRYPTED: int = 1
    WEBP: int = 2


class Image(NamedTuple):
    idx: int  # sequent image index
    url: str  # image url
    alternative_urls: Optional[List[str]]  # alternative urls
    name_format: str = '{idx:>03}-{name}.{extension}'
    # Explicitly specifying an extension is always preferable.
    extension: Optional[str] = None  # preferred extension
    type: int = 0  # image type @see ImageTypes.NORMAL
    name: Optional[str] = None  # force file name
    raw: Optional[bytes] = None  # raw bytes image

    def __str__(self) -> str:
        name = url2name(self.url)
        _re = re.search(r'(.+)\.(\w+)$', name)
        if _re is not None:
            name, ext = _re.groups()
        else:
            ext = None  # type: ignore
        return self.name_format.format(
            idx=self.idx,
            url=self.url,
            extension=self.extension or (ext or 'png'),
            name=self.name or name,
        )


class LocalImage(NamedTuple):  # m.b. delete this
    image: Image
    path: Path


class Archive(NamedTuple):  # for some sites
    idx: int  # sequent archive index
    url: str  # archive url
    name: str  # archive name
    date: Optional[str]  # chapter publication date
    name_format: str = 'arc_{idx:>03}-{name}'

    def __str__(self):
        # chapter human-friendly name
        return self.name_format.format(
            idx=self.idx,
            url=self.url,
            name=self.name,
            date=self.date,
        )


class Chapter(NamedTuple):
    """
    Example: Chapter(vol='4', ch='104', name='Tamatan, The Spirit', url='https://bato.to/chapter/1381023')
    """
    vol: str  # volume number
    ch: str  # chapter number
    url: str  # chapter url
    name: str  # chapter human-friendly name
    date: Optional[str] = None  # chapter publication date
    name_format: str = 'vol_{vol:>03}_ch_{ch:>03}-{name}'

    def __str__(self):
        # chapter human-friendly name
        return self.name_format.format(
            vol=self.vol,
            ch=self.ch,
            url=self.url,
            name=self.name,
            date=self.date,
        )


class Meta(NamedTuple):
    url: str  # manga url
    author: str  # author (Translated variant)
    author_original: str  # author (Original variant)
    title: str  # title (Translated variant)
    title_original: str  # title (Original variant)
    annotation: str
    keywords: List[str]
    cover: Union[str, bytes]  # manga cover url OR bytes
    rating: Tuple[float, float]  # manga rating (<current> / <max>)
