"""
gacha_transform

json->xlsx
xlsx->json
"""
from genshin.core import logger
from genshin.module.gacha.gacha_data_struct import GACHA_QUERY_TYPE_DICT


def load_xlsx() -> dict:
    """load data from xlsx"""
    pass


def merge_data(first: dict, second: dict):
    """
    merge gacha log, sorted by id

    data struct:

    {
        "list": {
            "100": [
                {
                    "uid": "",
                    "gacha_type": "",
                    "item_id": "",
                    "count": "",
                    "time": "2021-12-10 21:31:58",
                    "name": "",
                    "lang": "",
                    "item_type": "",
                    "rank_type": "",
                    "id": ""
                },
                ...
            ],
        }
    }
    """

    first_info = varify_data(first)
    second_info = varify_data(second)
    logger.debug(first_info)
    logger.debug(second_info)

    is_same_uid = first_info["uid"] == second_info["uid"]
    is_same_lang = first_info["lang"] == second_info["lang"]
    if not first or not second or not is_same_uid or not is_same_lang:
        logger.warning("数据信息不一致，无法合并")
        return None

    logger.info("开始合并数据")

    for gacha_type in GACHA_QUERY_TYPE_DICT:
        second_log = second["list"][gacha_type]
        first_log = first["list"][gacha_type]

        temp_data = []
        if second_log:
            # get second not in first
            temp_data = [log for log in second_log if log not in first_log]

        first_log.extend(temp_data)
        sorted(first_log,  key=lambda data: data["id"])
        logger.info(
            "数据合并 =====+> {} 共 {} \t条记录",
            GACHA_QUERY_TYPE_DICT[gacha_type],
            len(first_log),
        )
    logger.info("数据合并完成")
    return first


def varify_data(gacha_data: dict):
    """
    验证数据一致性
    """
    info = {}
    info["uid"] = ""
    info["lang"] = ""
    info["start_time"] = ""
    info["end_time"] = ""
    for gacha_type in GACHA_QUERY_TYPE_DICT:
        for data in gacha_data["list"][gacha_type]:
            if not data:
                continue

            if not info["uid"]:
                info["uid"] = data["uid"]
            elif info["uid"] != data["uid"]:
                logger.warning("数据中存在其他用户抽卡记录")
                return False

            if not info["lang"]:
                info["lang"] = data["lang"]
            elif info["lang"] != data["lang"]:
                logger.warning("数据中存在其他语言抽卡记录")
                return False

            if (not info["end_time"]) or (info["end_time"] < data["time"]):
                info["end_time"] = data["time"]

            if (not info["start_time"]) or (info["start_time"] > data["time"]):
                info["start_time"] = data["time"]

    return info
