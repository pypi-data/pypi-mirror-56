import unittest

from manga_py.providers.utils.request_utils import url2name
from ._test_variables import TestVariables


class TestUrlToName(unittest.TestCase, TestVariables):
    def test_url2name_url_one(self):
        name = url2name(self.default_image_url)
        self.assertEqual('sIz74wK_lq.mp4', name)

    def test_url2name_url_two(self):
        name = url2name(self.default_image_url + '/')
        self.assertEqual('sIz74wK_lq.mp4', name)

    def test_url2name_url_three(self):
        url = 'https://i.imgur.com/'
        with self.assertRaises(RuntimeError):
            url2name(url)

    def test_url2name_url_four(self):
        url = self.default_image_url + '/?abc=&def=123'
        name = url2name(url)
        self.assertEqual('sIz74wK_lq.mp4', name)
