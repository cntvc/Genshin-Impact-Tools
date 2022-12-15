"""
common function
"""
import json
import os
import traceback
from pathlib import Path

import requests
from requests import RequestException, Timeout

from genshin.config import settings
from genshin.core.log import logger


def touch(full_path: str):
    path = Path(full_path)
    if not path.parent.exists():
        os.makedirs(path.parent)
    if not path.exists():
        path.touch()
    logger.debug("创建文件{}", path)


def save_json(full_path: str, data):
    """
    save json data to full_path
    """
    touch(full_path)
    try:
        with open(full_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, sort_keys=False, indent=4)
    except IOError as err:
        logger.error("{}\n{}", err, full_path)
        return False
    except json.JSONDecodeError as err:
        logger.error("{}\n{}", err, full_path)
        return False
    return True


def load_json(full_path: str):
    """
    load json data from file
    """
    if not Path(full_path).exists():
        return None
    try:
        with open(full_path, "r", encoding="UTF-8") as file:
            data = json.load(file)
            return data
    except IOError as err:
        logger.error("{}\n{}", err, full_path)
        return None
    except json.JSONDecodeError as err:
        logger.error("{}\n{}", err, full_path)
        return None


def save_data(full_path: str, data):
    """
    save data to full_path
    """
    touch(full_path)
    try:
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(data)
    except IOError as err:
        logger.error("{}\n{}", err, full_path)
        return False
    except ValueError as err:
        logger.error("{}\n{}", err, full_path)
        return False
    return True


def clear_screen():
    """clean screen"""
    os.system("cls")


def pause():
    """pause"""
    os.system("pause")


def input_int(left: int, rigth: int):
    """
    input a integer, and the range of integers is in the interval [left, right]
    """
    while True:
        index = input()
        try:
            index = int(index)
        except (TypeError, ValueError):
            logger.warning("'{}' 为非法输入，请重试", index)
            continue

        if index > rigth or index < left:
            logger.warning("'{}' 为非法输入，请重试", index)
            continue
        return index


def request_get(url: str, timeout=settings.TIMEOUT):
    if not url:
        return None
    try:
        res = requests.get(url, timeout=timeout).content.decode("utf-8")
    except Timeout:
        logger.warning("链接请求超时, 请检查网络连接状态")
        return None
    except RequestException:
        logger.error("链接请求解析出错\n{}", traceback.format_exc())
        return None
    return res

def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton
