"""gacha module"""
import math
import os
from pathlib import Path
from typing import List

from genshin.config import settings
from genshin.core import logger
from genshin.core.function import load_json, save_json
from genshin.module.gacha.data_transform import merge_data, varify_data
from genshin.module.gacha.gacha_log import GachaLog
from genshin.module.gacha.gacha_url import UrlFactory, verify_url
from genshin.module.gacha.report_gengrator import report


class ExportManager:
    def __init__(self) -> None:
        self.data: dict = None
        self.uid: str = None
        self.url: str = None

    def export(self, url_source: int):
        url_product = UrlFactory.produce(url_source)
        self.url = url_product.get_url()
        if self.url == 0:
            return
        if not self.url or not verify_url(self.url):
            logger.warning("导出失败，请尝试其他方法")
            return
        gacha_log = GachaLog(self.url)
        self.data, self.uid = gacha_log.query()

        gacha_data_path = Path(settings.USER_DATA_PATH, self.uid, "gacha_data.json")
        self.merge_date(gacha_data_path)

        if not save_json(gacha_data_path, self.data):
            logger.warning("导出失败，请尝试其他方法")
            return
        logger.info("原始抽卡数据导出成功")
        self.save_user_config()
        self.generator_report()

    def merge_date(self, history_path):
        """
        If historical data is available, it will be merged with current data
        """
        if not settings.FLAG_AUTO_MERGE:
            return
        history = load_json(history_path)
        if history:
            logger.info("合并历史数据")
            self.data = merge_data(self.data, history)

    def save_user_config(self):
        config_path = Path(settings.USER_DATA_PATH, self.uid, "config.json")
        user_data = load_json(config_path)
        if not user_data:
            user_data = {}
        user_data["uid"] = self.uid
        user_data["gacha_url"] = self.url
        if not save_json(config_path, user_data):
            logger.warning("保存用户信息失败")

    def generator_report(self):
        report.data = self.data
        report.uid = self.uid
        report.generator_report()


def merge():
    """合并历史记录并生成报告（独立功能）

    默认扫描 ./Genshin_impact_tools/merge 目录的所有文件, 生成报告会保存到对应的 uid 目录
    """
    path = Path(settings.USER_DATA_PATH, "merge")
    if not path.exists():
        logger.warning("目录 {} 不存在\n请创建该文件夹后放入需要合并的数据文件", path)
        return False
    files = os.listdir(path)
    for file in files:
        file = Path(file)
        if file.suffix != ".json":
            files.remove(file)
    logger.info("共扫描到 {} 个文件", len(files))
    if len(files) < 2:
        logger.info("可合并文件数量低于2个，退出合并程序")
        return

    datas = []
    for file in files:
        data = load_json(Path(path, file))
        if not varify_data(data):
            logger.warning("文件 '{}' 中数据存在错误，此文件不会被合并", file)
            continue
        datas.append(data)

    logger.info("准备合并以下几个文件：\n{}\n", "\n".join(files))

    logger.info("合并数据中...")
    data = _merge_recursion(datas)[0]
    logger.info("合并数据完成")
    save_json(Path(settings.USER_DATA_PATH, data["info"]["uid"], "gacha_data.json"), data)
    report.data = data
    report.uid = data["info"]["uid"]
    report.generator_report()


def _merge_recursion(datas: List[dict]):
    length = len(datas)
    if length < 2:
        return datas
    if length == 2:
        return [merge_data(datas[0], datas[1])]

    middle = math.floor(length / 2)
    left = _merge_recursion(datas[0:middle])
    right = _merge_recursion(datas[middle:])
    return _merge_recursion(left + right)


export = ExportManager()
