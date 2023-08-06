from collections import OrderedDict
from pathlib import Path
from typing import Union, Tuple, Optional

from cloudscraper import CloudScraper
from requests import Session, Response
from requests.adapters import HTTPAdapter
from requests.cookies import RequestsCookieJar
from requests.utils import default_headers

from ..exceptions import CantWriteFileException
from .request_utils import url2name
from ..types import Image, LocalImage

__all__ = ['Request', ]


class Request:
    _headers: dict
    _session: Session

    def __init__(self, headers: dict):
        headers.update(default_headers())
        self._headers = headers
        default_adapter = HTTPAdapter(max_retries=3)
        self._session = Session()
        self._session.adapters = OrderedDict({
            'http://': default_adapter,
            'https://': default_adapter,
        })

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session: Session):
        self._session = session

    @property
    def headers(self) -> dict:
        return self._headers

    @headers.setter
    def headers(self, headers: dict):
        self._headers = headers

    def headers_update(self, headers: dict):
        self.headers.update(headers)

    @property
    def cookies(self) -> RequestsCookieJar:
        if not isinstance(self._session, Session):
            raise RuntimeError('Session error')
        return self._session.cookies

    @cookies.setter
    def cookies(self, cookies: dict):
        if not isinstance(self._session, Session):
            raise RuntimeError('Session error')
        c = self._session.cookies
        c.update(cookies)
        self._session.cookies = c

    def cookies_update(self, cookies: dict):
        if not isinstance(self._session, Session):
            raise RuntimeError('Session error')
        self._session.cookies.update(cookies)

    def request(self, method, url, has_referer: bool = True, **kwargs) -> Response:
        if not isinstance(self._session, Session):
            raise RuntimeError('Session error')
        kwargs.setdefault('headers', {})
        kwargs['headers'].update(self._headers)
        kwargs.setdefault('User-Agent', self.ua)
        if not has_referer and kwargs.get('headers', {}).get('Referer') is not None:
            del kwargs['headers']['Referer']
        return self._session.request(method=method, url=url, **kwargs)

    def get(self, url: str, **kwargs) -> Response:
        kwargs.setdefault('allow_redirects', True)
        return self.request(method='GET', url=url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        return self.request(method='POST', url=url, **kwargs)

    def download(self, url: str, path: Path, name: Union[str, Path] = None):
        """ path is directory """
        response = self.get(url)
        _path = path.resolve().joinpath(name or url2name(response.url))
        with open(str(_path), 'wb') as w:
            if not w.writable():
                raise CantWriteFileException(str(_path))
            w.write(response.content)
        return _path

    def download_image(self, image: Image, path: Path) -> LocalImage:
        _path = self.download(url=image.url, path=path, name=image.__str__())
        return LocalImage(
            image=image,
            path=_path,
        )

    @property
    def ua(self) -> Optional[str]:
        return self._headers.get('User-Agent', None)

    def cf_scrape(self, url: str, **kwargs):
        kwargs.setdefault('browser', {'browser': 'chrome', 'mobile': False})
        tokens = CloudScraper.get_tokens(url, **kwargs)  # type: Tuple[dict, str]
        self.cookies_update(tokens[0])
        self.headers.update({'User-Agent': tokens[1]})
