import json
import re
from typing import List, Union, Iterable

from ..base_provider import BaseProvider
from ..exceptions import ImagesNotFoundException, ChaptersNotFoundException, ProviderError
from ..types import *


class ReadMangaMe(BaseProvider):
    _url_re = re.compile(r'(.*//[^/]+/[^/])')
    _chapters_re = re.compile(r'/[^/]+/(?:vol)?([^/]+/[^/]+)(?:/|\?ma?t)?')
    _images_re = re.compile(r'rm_h\.init.+?(\[\[.+\]\])')
    _servers_re = re.compile(r'servers\s?=\s?(\[.+\])')

    @staticmethod
    def supported_urls() -> List[str]:
        return [r'//readmanga\.me/\w']

    def _url(self, url: str) -> str:
        match = self._url_re.search(url)
        if match is None:
            raise ProviderError()
        return match.group(1)

    def prepare(self):
        self.init_content()

    def get_chapters(self) -> Iterable[Chapter]:
        self.images_count = -1  # force reset it
        items = self.html.parse(self.content, '.table tr > td > a')

        if len(items) < 1:
            self.handle_error(ChaptersNotFoundException())
            return []

        self.chapters_count = len(items)
        for i in items:
            url = i.get('url')
            found = self._chapters_re.search(url)
            if found is None:
                self.warning("Chapter url has broken: \"{}\"".format(url))
                continue
            sub_str = found.group(1)
            if ~sub_str.find('?'):
                sub_str = sub_str[:sub_str.find('?')]
            vol, ch = sub_str.split('/')
            yield Chapter(
                vol=vol,
                ch=ch,
                url=url,
                name=self.html.text(i),
                # name_format=''
            )

    def get_chapter_files(self, chapter: Chapter) -> Iterable[Union[Image, Archive]]:
        content = self.request.get(chapter.url).text
        images = self._images_re.search(content)

        if images is None:
            self.handle_error(ImagesNotFoundException(chapter))
            return []

        urls: List[list] = json.loads(images.group(1).replace("'", '"'))
        _re_servers = self._servers_re.search(content)

        servers: List[str] = []
        if _re_servers is not None:
            _text = _re_servers.group(1).replace("'", '"')
            servers = json.loads(_text) if servers else []

        self.images_count = len(urls)

        # ['','https://t7.mangas.rocks/',"auto/33/88/46/One-piece.ru_Credits.png_res.jpg",1250,850]
        for i, u in enumerate(urls):
            yield Image(
                idx=i,
                url='{1}{2}'.format(*u),
                extension='extension',
                alternative_urls=['{}{}'.format(s, u[2]) for s in servers],
            )

    def get_meta(self) -> Meta:
        dom = self.html.parse(self.content)
        orig_name = self.html.select(dom, '.names .original-name')
        score = self.html.select_one(dom, 'input[name="score"]', 0)
        return Meta(
            url=self.url,
            author=self.html.text(self.html.select_one(dom, '.elem_author a.person-link', 0)),
            author_original='',
            title=self.html.text(self.html.select_one(dom, '.names .name', 0)),
            title_original='' if len(orig_name) < 1 else self.html.text(orig_name[0]),
            annotation=self.html.text_full(self.html.select_one(dom, '.manga-description', 0)),
            keywords=[],
            cover=self.html.cover(dom, '.picture-fotorama > img'),
            rating=(float(score.get('value')), 5.0),
        )
