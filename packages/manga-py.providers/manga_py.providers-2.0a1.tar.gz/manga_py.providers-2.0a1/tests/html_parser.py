import unittest

from lxml.html import HtmlElement

from manga_py.providers.exceptions import *
from manga_py.providers.utils.html_parser import HtmlParser
from ._test_variables import TestVariables


class TestHtmlParser(unittest.TestCase, TestVariables):
    def test_parser(self):
        html = HtmlParser.parse(self.default_html)
        self.assertEqual(len(HtmlParser.parse(self.default_html, 'a')), 1)
        title = HtmlParser.select_one(html, 'title', 0)
        self.assertEqual(HtmlParser.text(title), 'Title')
        self.assertIsInstance(html, HtmlElement)

    def test_background_image(self):
        html = HtmlParser.parse(self.default_html)
        self.assertEqual(
            self.default_image_url,
            HtmlParser.background_image(HtmlParser.select_one(html, 'div.image', 0))
        )
        with self.assertRaises(BackgroundImageExtractException) as e:
            HtmlParser.background_image(HtmlParser.select_one(html, 'div.bad-image', 0))
        self.assertEqual('background: url()', e.exception.style)

    def test_get_empty_text(self):
        html = HtmlParser.parse(self.default_html)

        with self.assertRaises(InfoException) as e:
            HtmlParser.text(HtmlParser.select_one(html, 'div.empty-element', 0))
        self.assertEqual(('Element not have text',), e.exception.args)

        with self.assertRaises(InfoException) as e:
            HtmlParser.text(HtmlParser.select_one(html, 'div.inner-element-text', 0))
        self.assertEqual(('Element not have text',), e.exception.args)

        with self.assertRaises(InfoException) as e:
            HtmlParser.text(HtmlParser.select_one(html, 'div.space-only-element', 0))
        self.assertEqual(('Text is too short',), e.exception.args)

        with self.assertRaises(InfoException) as e:
            HtmlParser.text_full(HtmlParser.select_one(html, 'div.space-only-element', 0))
        self.assertEqual(('Text is too short',), e.exception.args)

        self.assertEqual('text', HtmlParser.text_full(HtmlParser.select_one(html, 'div.inner-element-text', 0)))

    def test_attributes(self):
        elements = HtmlParser.parse(self.default_html, '.empty-element')
        self.assertEqual(['element-title'], HtmlParser.extract_attribute(elements, 'title'))

    def test_cover(self):
        html = HtmlParser.parse(self.default_html)
        self.assertEqual(self.default_image_url, HtmlParser.cover(html, '.image > img'))


