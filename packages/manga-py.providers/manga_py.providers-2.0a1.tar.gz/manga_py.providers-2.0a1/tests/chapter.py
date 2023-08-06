import unittest

from manga_py.providers.types import Chapter
from ._test_variables import TestVariables


class TestChapter(unittest.TestCase, TestVariables):
    @classmethod
    def _chapter(cls, **kwargs):
        kwargs.setdefault('vol', '0')
        kwargs.setdefault('ch', '1')
        kwargs.setdefault('name', 'name')
        kwargs.setdefault('url', cls.default_chapter_url)
        return Chapter(**kwargs)

    def test_chapter_default(self):
        self.assertEqual('vol_000_ch_001-name', str(self._chapter()))

    def test_chapter_name_format(self):
        self.assertEqual('awesome-000_ch_001', str(self._chapter(name_format='awesome-{vol:>03}_ch_{ch:>03}')))
