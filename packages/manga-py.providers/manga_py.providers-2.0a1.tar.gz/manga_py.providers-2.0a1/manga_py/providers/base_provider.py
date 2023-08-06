import re
from abc import ABCMeta, abstractmethod
from typing import List, Union, Optional, Iterable, Type

from .types import *
from .utils.html_parser import HtmlParser
from .utils.properties import ProviderProperties
from .utils.request import Request


class BaseProvider(ProviderProperties, metaclass=ABCMeta):
    DISABLED = False
    AUTO_INIT = True

    def __init__(
            self, url: str, connection: Request = None,
            html_parser: Union[HtmlParser, Type[HtmlParser]] = None,
            **kwargs
    ):
        url = self._url(url)
        if connection is None:
            connection = Request({})
            connection.headers_update(kwargs.get('headers', {}))
            connection.cookies_update(self._cookies(kwargs.get('cookies', {})))
        super().__init__(url=url, connection=connection, html_parser=(html_parser or HtmlParser))
        self._cache.setdefault('run_params', kwargs)
        self._requests = connection  # type: Request

        if self.AUTO_INIT:
            try:
                self.prepare()
                self.meta = self.get_meta()
            except Exception as e:
                self.handle_error(e)
        else:
            self.info('Please, call prepare() manual')

    @staticmethod
    @abstractmethod
    def supported_urls() -> List[str]:
        """
        Example:
        [
            r'//bato\.to/series/\d',
            r'//www\.mangahere\.cc/manga/\w',
        ]
        """
        raise NotImplementedError()

    @classmethod
    def is_supported(cls, url) -> bool:
        for _url in cls.supported_urls():
            if not cls.DISABLED and re.search(_url, url):
                return True
        return False

    # region abstract
    def allow_send_files_referrer(self) -> bool:
        """ allow send referrer header """
        return True

    @abstractmethod
    def prepare(self):
        self.init_content()
        self.info_or_raise('Default prepare method')

    @abstractmethod
    def get_chapters(self) -> Iterable[Chapter]:
        raise NotImplementedError()

    def get_chapters_count(self) -> int:
        """ If -1, then continue always """
        return self.chapters_count

    @abstractmethod
    def get_chapter_files(self, chapter: Chapter) -> Iterable[Union[Image, Archive]]:
        raise NotImplementedError()

    def get_chapter_files_count(self, chapter: Chapter) -> int:
        return self.images_count

    @abstractmethod
    def get_meta(self) -> Meta:
        raise NotImplementedError()
    # endregion abstract

    # region special methods
    def _url(self, url: str) -> str:
        """ Modify url if need (before init provider) """
        return url

    def _cookies(self, cookies: dict) -> dict:
        """ Modify cookies if need (before init provider) """
        return cookies

    def _headers(self, headers: dict) -> dict:
        """ Modify headers if need (before init provider) """
        return headers

    def flat_chapters(self) -> bool:
        """ This is used when a "chapter" contains maybe only 1 image e.g. pixiv.net """
        return False

    def handle_error(self, state: Exception):
        """ overload this for catching errors OR run provider with option quiet=True  """
        super().handle_error(state)

    def before_image_save(self, image: Image) -> Optional[LocalImage]:
        """ Manipulate image before saving """
        pass

    def after_image_save(self, image: LocalImage):
        """ Manipulate image after saving """
        pass
    # endregion special methods
