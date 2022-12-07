"""gacha module"""
from pathlib import Path

from genshin.config import settings
from genshin.core import logger
from genshin.core.function import load_json, save_json
from genshin.module.gacha.gacha_log import GachaLog
from genshin.module.gacha.gacha_url import UrlFactory, verify_url


class ExportFactory:
    gacha_log: dict = {}

    def export(self, url_source: int):
        url_product = UrlFactory.produce(url_source)
        url = url_product.get_url()
        if not verify_url(url):
            logger.warning("导出失败，请尝试其他方法")
            return
        self.gacha_log = GachaLog(url)
        self.gacha_log.query()

        gacha_data_path = Path(settings.USER_DATA_PATH, self.gacha_log.uid, "gacha_data.json")
        history = load_json(gacha_data_path)
        if history:
            # If historical data is available, it will be merged with current data
            self.gacha_log.data = GachaLog.merge(self.gacha_log.data, history)

        if not save_json(gacha_data_path, self.gacha_log.data):
            logger.warning("导出失败，请尝试其他方法")
            return
        logger.info("抽卡数据导出成功")
        self.save_user_config()

    def save_user_config(self):
        config_path = Path(settings.USER_DATA_PATH, self.gacha_log.uid, "config.json")
        user_data = load_json(config_path)
        if not user_data:
            user_data = {}
        user_data["uid"] = self.gacha_log.uid
        user_data["gacha_url"] = self.gacha_log.url
        if not save_json(config_path, user_data):
            logger.warning("保存用户信息失败")
