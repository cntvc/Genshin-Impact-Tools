"""gacha log"""
import json
import time
from random import random
from urllib import parse

from genshin.core import logger
from genshin.core.function import request_get
from genshin.module.gacha.gacha_data_struct import (GACHA_QUERY_TYPE_DICT,
                                                    GACHA_QUERY_TYPE_IDS)


class GachaLog:
    """
    query gacha log
    """

    def __init__(self, url: str) -> None:
        # gacha log
        self.data = {}
        self.uid = ""
        self.url = url

    def query(self):
        """
        Query the gacha log of the last 6 months
        """
        logger.info("开始获取抽卡记录")

        self.data["list"] = {}
        lang = ""
        uid_flg = False
        for gacha_type_id in GACHA_QUERY_TYPE_IDS:
            gacha_log = self._query_by_type_id(gacha_type_id)

            # 抽卡记录以时间顺序排列
            gacha_log.reverse()
            self.data["list"][gacha_type_id] = gacha_log
            if not uid_flg and gacha_log:
                # 以查询链接的uid为准，若查询无任何记录，则默认为当前登陆uid
                self.uid = gacha_log[-1]["uid"]
                uid_flg = True
            if not lang and gacha_log:
                lang = gacha_log[-1]["lang"]
        gacha_log = self.data["list"][gacha_type_id]

        # set info
        self.data["info"] = {}
        self.data["info"]["uid"] = self.uid
        self.data["info"]["lang"] = lang
        self.data["info"]["export_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # set gacha_type
        self.data["gacha_type"] = GACHA_QUERY_TYPE_DICT

    def _query_by_type_id(self, gacha_type_id):
        """
        Query gacha log by type
        """
        max_size = "20"
        gacha_list = []
        end_id = "0"
        for page in range(1, 9999):
            logger.info(f"正在获取 {GACHA_QUERY_TYPE_DICT[gacha_type_id]} 第 {page} 页")
            api = self._set_url_param(gacha_type_id, max_size, page, end_id)

            res = request_get(api)
            res_json = json.loads(res)
            gacha = res_json["data"]["list"]
            if not gacha:
                break
            for i in gacha:
                gacha_list.append(i)
            end_id = res_json["data"]["list"][-1]["id"]
            time.sleep(0.5 + random())
        return gacha_list

    def _set_url_param(self, gacha_type_id, size, page, end_id=""):
        """
        Set url parameters
        """
        parsed = parse.urlparse(self.url)
        querys = parse.parse_qsl(str(parsed.query))
        param_dict = dict(querys)

        param_dict["size"] = size
        param_dict["gacha_type"] = gacha_type_id
        param_dict["page"] = page
        param_dict["lang"] = "zh-cn"
        param_dict["end_id"] = end_id

        param = parse.urlencode(param_dict)
        path = str(self.url).split("?", maxsplit=1)[0]
        url = path + "?" + param
        return url
