from typing import Union, List, Dict, Any, Optional

from lxml.html import document_fromstring, HtmlElement
from tinycss2 import parser, tokenizer

from ..exceptions import BackgroundImageExtractException, InfoException


__all__ = ['HtmlParser']


class HtmlParser:
    __slots__ = ()
    __dict__: Dict[str, Any] = dict()
    DEFAULT_TRANSLATOR: str = 'html'

    @classmethod
    def select(cls, content: HtmlElement, selector: str) -> List[HtmlElement]:
        return content.cssselect(selector)

    @classmethod
    def select_one(cls, content: HtmlElement, selector: str, idx: int) -> HtmlElement:
        items = cls.select(content, selector)
        return items[idx]

    @classmethod
    def parse(cls, content: str, selector: str = None) -> Union[HtmlElement, List[HtmlElement]]:
        dom = document_fromstring(content)  # type: HtmlElement
        if selector is None:
            return dom
        return cls.select(dom, selector)

    @classmethod
    def background_image(cls, element: HtmlElement) -> str:
        style = element.get('style')
        url = [i for i in parser.parse_component_value_list(style) if isinstance(i, tokenizer.URLToken)]
        if len(url) < 1 or len(url[-1].value) < 1:
            raise BackgroundImageExtractException(style)
        return url[-1].value

    @classmethod
    def extract_attribute(cls, items: List[HtmlElement], attribute: str, strip: bool = True) -> List[str]:
        return [(i.get(attribute).strip() if strip else i.get(attribute)) for i in items]

    @classmethod
    def __check_min_text_length(cls, text: str, min_length: int = 1):
        if len(text) < min_length:
            raise InfoException('Text is too short')

    @classmethod
    def text(cls, element: HtmlElement, strip: bool = True):
        text_or_none = element.text
        if text_or_none is None:
            raise InfoException('Element not have text')
        text = text_or_none.strip() if strip else text_or_none
        cls.__check_min_text_length(text)
        return text

    @classmethod
    def text_full(cls, element: HtmlElement, strip: bool = True):
        text = element.text_content().strip() if strip else element.text_content()
        cls.__check_min_text_length(text)
        return text

    @classmethod
    def cover(cls, element: HtmlElement, selector: str, attr: str = 'src', idx: int = 0) -> str:
        _el = cls.select_one(element, selector, idx)
        value = _el.get(attr)
        cls.__check_min_text_length(value)
        return value
