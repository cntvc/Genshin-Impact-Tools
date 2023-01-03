"""
data transform

- convert between gacha log and uigf
- merge gacha log
"""
import time
from operator import itemgetter
from pathlib import Path
from typing import List

from openpyxl import load_workbook

from genshin import APP_NAME
from genshin import __version__ as version
from genshin.core import logger
from genshin.core.function import dedupe, load_json
from genshin.module.gacha.metadata import GACHA_QUERY_TYPE_DICT, GACHA_QUERY_TYPE_IDS

UIGF_VERSION = "v2.2"


def merge_data(datas: List[dict]):
    """merge gacha data list

    Args:
        datas (List[dict]): gacha data list

    Returns:
        dict
    """
    gacha_type_data = {}
    for gacha_type in GACHA_QUERY_TYPE_DICT:
        gacha_type_data[gacha_type] = []
    for data in datas:
        for gacha_type in GACHA_QUERY_TYPE_DICT:
            gacha_type_data[gacha_type].extend(data["list"][gacha_type])
    for gacha_type in GACHA_QUERY_TYPE_DICT:
        gacha_type_data[gacha_type] = list(dedupe(gacha_type_data[gacha_type], lambda x: x["id"]))
        gacha_type_data[gacha_type] = sorted(gacha_type_data[gacha_type], key=itemgetter("id"))
    gacha_data = {}
    gacha_data["info"] = generator_info(datas[0]["info"]["uid"], datas[0]["info"]["lang"])
    gacha_data["list"] = gacha_type_data
    return gacha_data


def varify_data(gacha_data: dict):
    """Verify data consistency and add info

    Args:
        gacha_data (dict)

    Returns:
        bool: Returns True on success
    """
    uid = ""
    lang = ""

    for gacha_type in GACHA_QUERY_TYPE_DICT:
        for data in gacha_data["list"][gacha_type]:
            if not data:
                continue

            if not uid:
                uid = data["uid"]
            elif uid != data["uid"]:
                return False

            if not lang:
                lang = data["lang"]

    gacha_data["info"] = generator_info(uid, lang)
    return True


def generator_info(uid, lang):
    _time = time.time()
    info = {}
    info["uid"] = uid
    info["lang"] = lang
    info["export_timestamp"] = int(_time)
    info["export_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(_time))
    info["export_app"] = APP_NAME
    info["export_app_version"] = version
    return info


def load_gacha_data(path: str):
    """load UIGF from path, file suffix: [xlsx | json]

    Args:
        path (str): UIGF file path
    Returns:
        dict: app gacha log fromat or {}
    """
    # TODO 加载其他数据返回 {}
    file_path = Path(path)
    if not file_path.exists():
        logger.warning("文件 '{}' 不存在， 无法加载UIFG数据", file_path)
        return {}
    file_suffix = file_path.suffix
    if file_suffix == ".json":
        data = _load_uigf_json(file_path)
    elif file_suffix == ".xlsx":
        data = _load_uigf_xlsx(file_path)
    data = _convert_to_app(data)
    if not data:
        logger.error("文件 '{}' 数据读取失败，请检查文件格式类型", path)
    return data


def _load_uigf_xlsx(path: str):
    """load UIGF data from path, file suffix is .xlsx

    Args:
        path (str): UIGF file path

    Returns:
        dict: UIGF data
    """
    workbook = load_workbook(path, read_only=True)
    worksheet = workbook["原始数据"]
    rows = list(worksheet.rows)
    titles = [title.value for title in rows.pop(0)]
    gacha_data = {}
    gacha_data["list"] = []
    for row in rows:
        the_row_data = [cell.value for cell in row]
        the_row_data = ["" if x is None else x for x in the_row_data]
        gacha_data["list"].append(dict(zip(titles, the_row_data)))
    workbook.close()
    return gacha_data


def _load_uigf_json(path: str):
    """load UIGF data from path, file suffix is .json

    Args:
        path (str): UIGF file path

    Returns:
        dict: UIGF data
    """
    return load_json(path)


def _convert_to_app(data: dict):
    """convert uigf to app gacha log fromat

    Args:
        data (dict): uigf data

    Returns:
        dict: app gacha log format
    """

    # app自有格式直接返回
    if isinstance(data["list"], dict):
        return data
    if not isinstance(data["list"], list):
        return {}
    gacha_log = {}
    gacha_log["list"] = {}
    for gacha_type in GACHA_QUERY_TYPE_IDS:
        gacha_log["list"][gacha_type] = []
    for items in data["list"]:
        if items["gacha_type"] == "100":
            gacha_log["list"]["100"].append(items)
        elif items["gacha_type"] == "200":
            gacha_log["list"]["200"].append(items)
        elif items["gacha_type"] == "301":
            gacha_log["list"]["301"].append(items)
        elif items["gacha_type"] == "302":
            gacha_log["list"]["302"].append(items)
        elif items["gacha_type"] == "400":
            gacha_log["list"]["301"].append(items)
        else:
            logger.error("转换为UIGF格式失败")
            return {}
    if not varify_data(gacha_log):
        return {}
    for gacha_type in GACHA_QUERY_TYPE_IDS:
        sorted(gacha_log["list"][gacha_type], key=itemgetter("id"))
    return gacha_log


def convert_to_uigf(data: dict):
    """covert app gacha log data to UIGF format

    Args:
        data (dict): app gacha log format
    Returns:
        dict: UIGF data
    """
    uigf = {}
    info = data["info"]
    uigf["info"] = generator_info(info["uid"], info["lang"])
    uigf["info"]["uigf_version"] = UIGF_VERSION

    uigf["list"] = []

    temp = []
    for gacha_type in GACHA_QUERY_TYPE_IDS:
        gacha_log = data["list"][gacha_type]
        for gacha in gacha_log:
            gacha["uigf_gacha_type"] = gacha_type
        temp.extend(gacha_log)
    temp = sorted(temp, key=itemgetter("time"))

    id = _id_generator()
    for item in temp:
        if item.get("id", "") == "":
            item["id"] = next(id)

    temp = sorted(temp, key=itemgetter("id"))
    uigf["list"] = temp
    return uigf


def _id_generator():
    id = 1000000000000000000
    while True:
        id = id + 1
        yield str(id)
