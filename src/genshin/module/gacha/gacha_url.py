"""gacha url"""
import abc
import json
import os
import re
import tempfile
from pathlib import Path
from shutil import copyfile
from typing import Optional

from genshin.config import settings
from genshin.core import logger
from genshin.core.function import request_get
from genshin.module.clipboard import get_clipboad_text_or_html
from genshin.module.user import user


def get_url_from_string(string: Optional[str]) -> Optional[str]:
    """get url from string"""
    if not string:
        return None
    res = re.search("https://.+?authkey.+?game_biz=hk4e_(?:cn|global)", string)

    return res.group() if res else None


def verify_url(url: str):
    """
    verify gacha url

    if url can't access, return False
    """
    logger.debug("验证链接有效性")
    logger.debug(url)
    res = request_get(url)
    if not res:
        return False

    res_json = json.loads(res)
    logger.debug(res_json)
    if not res_json["data"]:
        if res_json["message"] == "authkey timeout":
            logger.warning("链接过期")
        elif res_json["message"] == "authkey error":
            logger.warning("链接错误")
        else:
            logger.warning("数据为空，错误代码：" + res_json["message"])
        return False
    logger.debug("链接可用")
    return True


class AbstractUrl(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_url(self) -> Optional[str]:
        pass


class ClipboadUrl(AbstractUrl):
    def get_url(self):
        """
        get gacha url from clipboad
        """
        text = get_clipboad_text_or_html()
        logger.debug(f"get_clipboad_text_or_html {text}")
        url = get_url_from_string(text)
        logger.debug(f"url: {url}")
        return url


class CacheUrl(AbstractUrl):
    def get_cache_path(self):
        log_dir_name = "原神"
        data_path = "YuanShen_Data"
        if user.get_area() == "global":
            log_dir_name = "Genshin Impact"
            data_path = "GenshinImpact_Data"

        log_path = Path(settings.MIHOYO_CHAHE_PATH, log_dir_name, "output_log.txt")
        assert log_path.exists(), "日志文件不存在"
        try:
            log_text = log_path.read_text(encoding="utf8")
        except UnicodeDecodeError as err:
            logger.debug(f"日志文件编码不是utf8, 尝试默认编码 {err}")
            log_text = log_path.read_text(encoding=None)

        res = re.search("([A-Z]:/.+{})".format(data_path), log_text)

        game_path = res.group() if res else None
        assert game_path, "未找到游戏路径"

        data_2 = Path(game_path) / "webCaches/Cache/Cache_Data/data_2"
        assert data_2.is_file(), "缓存文件不存在"

        return data_2

    def get_url(self):
        """
        get gacha url from game cache file
        """
        cache_file = self.get_cache_path()
        if not cache_file:
            return ""
        with tempfile.NamedTemporaryFile("w+", delete=False) as tmp_file:
            tmp_file_name = tmp_file.name
        copyfile(str(cache_file), str(tmp_file_name))

        logger.info("开始读取缓存")
        with open(tmp_file_name, "rb") as file:
            results = file.read().split(b"1/0/")

        os.unlink(tmp_file_name)
        logger.debug(f"删除临时文件{tmp_file_name}")

        # reverse order traversal
        for result in results[::-1]:
            result = result.decode(errors="ignore")
            text = get_url_from_string(result)
            if text:
                url = text
                break
        return url


class ConfigUrl(AbstractUrl):
    def get_url(self):
        """
        get gacha url from config.json
        """
        data = {}
        if not user.get_gacha_url():
            data = user.load_config()
        if not data:
            return ""
        return data["gacha_url"]


class UrlFactory:
    @staticmethod
    def produce(url_source: int) -> AbstractUrl:
        """
        produce url by url source
        """
        if url_source == settings.URL_SOURCE_CONFIG:
            product = ConfigUrl()
        elif url_source == settings.URL_SOURCE_CLIPBOARD:
            product = ClipboadUrl()
        elif url_source == settings.URL_SOURCE_GAMECACHE:
            product = CacheUrl()
        else:
            raise ValueError("Unknown url source " + str(url_source))
        return product
