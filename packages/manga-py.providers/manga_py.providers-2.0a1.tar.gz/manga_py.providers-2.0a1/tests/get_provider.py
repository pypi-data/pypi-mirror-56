import unittest

from manga_py.providers import get_providers
from manga_py.providers.exceptions import *
from manga_py.providers.providers import ReadMangaMe
from ._test_variables import TestVariables


class TestGetProviders(unittest.TestCase, TestVariables):
    def test_get_providers_has_data_is_valid(self):
        providers = get_providers(self.default_manga_url)
        self.assertGreater(len(providers), 0)
        self.assertIs(ReadMangaMe, providers[0])

    def test_get_providers_has_site_not_supported(self):
        with self.assertRaises(ProviderNotFoundError):
            get_providers('https://not-supported/')

