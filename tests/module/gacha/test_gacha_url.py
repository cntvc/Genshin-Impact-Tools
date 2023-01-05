"""
test url factory
"""

import pytest

from genshin.config import settings
from genshin.module.gacha.gacha_url import CacheUrl, ClipboadUrl, ConfigUrl, UrlFactory


class TestUrlFactory:
    def test_url_factory_config(self):
        url = UrlFactory.produce(settings.URL_SOURCE_CONFIG)
        assert isinstance(url, ConfigUrl)

    def test_url_factory_clipboad(self):
        url = UrlFactory.produce(settings.URL_SOURCE_CLIPBOARD)
        assert isinstance(url, ClipboadUrl)

    def test_url_factory_cache(self):
        url = UrlFactory.produce(settings.URL_SOURCE_GAMECACHE)
        assert isinstance(url, CacheUrl)

    def test_url_factory_error(self):
        with pytest.raises(ValueError, match="Unknown url source -10"):
            UrlFactory.produce(-10)


class TestCacheUrl:
    pass
