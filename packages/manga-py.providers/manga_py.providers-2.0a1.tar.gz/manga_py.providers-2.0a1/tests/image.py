import unittest

from manga_py.providers.types import Image
from ._test_variables import TestVariables


class TestImage(unittest.TestCase, TestVariables):
    @classmethod
    def _image(cls, **kwargs):
        kwargs.setdefault('idx', 0)
        kwargs.setdefault('url', cls.default_image_url)
        kwargs.setdefault('alternative_urls', [])
        return Image(**kwargs)

    def test_image_one(self):
        self.assertEqual('000-sIz74wK_lq.mp4', str(self._image()))

    def test_image_two(self):
        self.assertEqual('000-video.jpeg', str(self._image(extension='jpeg', name='video')))

    def test_image_three(self):
        self.assertEqual('mp4/sIz74wK_lq', str(self._image(name_format='{extension}/{name}')))

    def test_image_without_extension(self):
        url = self.default_image_url[:self.default_image_url.rfind('.')]
        self.assertEqual('000-sIz74wK_lq.png', str(self._image(url=url)))
