"""gacha module"""
from pathlib import Path
from typing import List

from genshin.config import settings
from genshin.core import logger
from genshin.core.function import load_json, save_json
from genshin.module.gacha.data_transform import merge_data
from genshin.module.gacha.gacha_log import GachaLog
from genshin.module.gacha.gacha_url import UrlFactory, verify_url
from genshin.module.gacha.report_gengrator import (AbstractGenerator,
                                                   XLSXGenerator)


class ExportManager:
    def __init__(self) -> None:
        self.gacha_log: GachaLog = None
        self.generators: List[AbstractGenerator] = []

    def export(self, url_source: int):
        url_product = UrlFactory.produce(url_source)
        url = url_product.get_url()
        if not verify_url(url):
            logger.warning("导出失败，请尝试其他方法")
            return
        self.gacha_log = GachaLog(url)
        self.gacha_log.query()

        gacha_data_path = Path(settings.USER_DATA_PATH, self.gacha_log.uid, "gacha_data.json")
        self.merge_date(gacha_data_path)

        if not save_json(gacha_data_path, self.gacha_log.data):
            logger.warning("导出失败，请尝试其他方法")
            return
        logger.info("抽卡数据导出成功")
        self.save_user_config()
        self.generator_report()

    def merge_date(self, history_path):
        """
        If historical data is available, it will be merged with current data
        """
        history = load_json(history_path)
        if history:
            logger.info("合并历史数据")
            self.gacha_log.data = merge_data(self.gacha_log.data, history)

    def generator_report(self):
        for generator in self.generators:
            if not generator.status():
                continue
            generator.data = self.gacha_log.data
            generator.uid = self.gacha_log.uid
            generator.generator()

    def add_generator(self, generator: AbstractGenerator):
        self.generators.append(generator)

    def save_user_config(self):
        config_path = Path(settings.USER_DATA_PATH, self.gacha_log.uid, "config.json")
        user_data = load_json(config_path)
        if not user_data:
            user_data = {}
        user_data["uid"] = self.gacha_log.uid
        user_data["gacha_url"] = self.gacha_log.url
        if not save_json(config_path, user_data):
            logger.warning("保存用户信息失败")


xlsx_generator = XLSXGenerator(None, None)

export_manager = ExportManager()

export_manager.add_generator(xlsx_generator)
