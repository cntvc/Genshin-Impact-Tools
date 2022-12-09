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
from genshin.core.function import (clear_screen, input_int, load_json,
                                   request_get)
from genshin.module.clipboard import get_clipboad_text_or_html


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
    logger.info("验证链接有效性")
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
    logger.info("链接可用")
    return True


class AbstractUrl(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_url(self) -> Optional[str]:
        pass


class ClipboadUrl(AbstractUrl):
    def get_url(self) -> Optional[str]:
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
        log_path = Path(settings.MIHOYO_CHAHE_PATH, "原神", "output_log.txt")
        try:
            log_text = log_path.read_text(encoding="utf8")
        except UnicodeDecodeError as err:
            logger.debug(f"日志文件编码不是utf8, 尝试默认编码 {err}")
            log_text = log_path.read_text(encoding=None)

        res = re.search("([A-Z]:/.+(GenshinImpact_Data|YuanShen_Data))", log_text)
        game_path = res.group() if res else None
        if not game_path:
            logger.warning("未找到游戏路径")
            return None

        data_2 = Path(game_path) / "webCaches/Cache/Cache_Data/data_2"
        if not data_2.is_file():
            logger.warning("缓存文件不存在")
            return None
        return data_2

    def get_url(self) -> Optional[str]:
        """
        get gacha url from game cache file
        """
        cache_file = self.get_cache_path()
        if not cache_file:
            return None
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

    user_data_dir_re = re.compile("^[0-9]{9,}$")

    def get_user_list(self):
        if not os.path.isdir(settings.USER_DATA_PATH):
            return []
        file_list = os.listdir(settings.USER_DATA_PATH)
        # save folders with digit name
        for name in file_list:
            if os.path.isfile(name):
                file_list.remove(name)
            elif not ConfigUrl.user_data_dir_re.match(name):
                file_list.remove(name)

        user_list = []
        # read config.json
        for folder in file_list:
            path = Path(settings.USER_DATA_PATH, folder, "config.json")
            if not path.exists():
                continue

            config = load_json(path)
            if not config or ("uid" not in config):
                continue
            logger.debug("检测到 {} 配置文件", config["uid"])
            user_list.append(config)
        return user_list

    def get_url(self) -> Optional[str]:
        """
        get gacha url from config.json
        """
        user_list = self.get_user_list()
        user_count = len(user_list)
        if not user_count:
            logger.warning("未检测到有效配置文件")
            return None

        if user_count == 1:
            return user_list[0]["gacha_url"]

        clear_screen()
        print("检测到多位用户配置文件，请输入数字选择:")
        for index, user_data in enumerate(user_list):
            print(f"{index + 1}. {user_data['uid']}")
        print("\n输入 0 取消导出")
        index = input_int(0, len(user_list))

        if index == 0:
            return None

        return user_list[index - 1]["gacha_url"]


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
