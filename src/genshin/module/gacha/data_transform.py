"""
data transform

- convert between gacha log and uigf
- merge gacha log
"""
import time
from pathlib import Path

from openpyxl import load_workbook

from genshin import APP_NAME
from genshin import __version__ as version
from genshin.core import logger
from genshin.core.function import load_json
from genshin.module.gacha.metadata import GACHA_QUERY_TYPE_DICT, GACHA_QUERY_TYPE_IDS

UIGF_VERSION = "v2.2"


def merge_data(first: dict, second: dict):
    """
    merge gacha log, sorted by id

    if can't merge, return {}
    """

    first_info = first["info"]
    second_info = second["info"]
    logger.debug(first_info)
    logger.debug(second_info)

    is_same_uid = first_info["uid"] == second_info["uid"]
    is_same_lang = first_info["lang"] == second_info["lang"]
    if not first or not second or not is_same_uid or not is_same_lang:
        logger.warning("数据信息不一致，无法合并")
        return {}

    logger.debug("开始合并数据")
    first["info"] = generator_info(first_info["uid"], first_info["lang"])

    for gacha_type in GACHA_QUERY_TYPE_DICT:
        second_log = second["list"][gacha_type]
        first_log = first["list"][gacha_type]
        first_ids = [x["id"] for x in first_log]
        temp_data = []
        if second_log:
            # get second not in first
            temp_data = [log for log in second_log if log["id"] not in first_ids]

        first_log.extend(temp_data)
        first["list"][gacha_type] = sorted(first_log, key=lambda data: data["id"])
        logger.debug(
            "数据合并 =====+> {} 共 {} \t条记录",
            GACHA_QUERY_TYPE_DICT[gacha_type],
            len(first_log),
        )
    logger.debug("数据合并完成")
    return first


def varify_data(gacha_data: dict):
    """
    验证数据一致性，并添加数据信息
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
                logger.warning("数据中存在不同用户抽卡记录")
                return False

            if not lang:
                lang = data["lang"]
            elif lang != data["lang"]:
                logger.warning("数据中存在不同语言抽卡记录")
                return False

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
        sorted(gacha_log["list"][gacha_type], key=lambda i: i["id"])
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
    temp = sorted(temp, key=lambda item: item["time"])

    id = _id_generator()
    for item in temp:
        if item.get("id", "") == "":
            item["id"] = next(id)

    temp = sorted(temp, key=lambda item: item["id"])
    uigf["list"] = temp
    return uigf


def _id_generator():
    id = 1000000000000000000
    while True:
        id = id + 1
        yield str(id)
