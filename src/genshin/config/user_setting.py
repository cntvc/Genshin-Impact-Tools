from genshin.config import settings
from genshin.core import logger
from genshin.module.gacha.report_gengrator import xlsx_generator


__all__ = ["update_auto_merge", "update_generator_xlsx"]


def update_auto_merge(flg: bool):
    settings.FLAG_AUTO_MERGE = flg
    msg = "关闭"
    if flg:
        msg = "打开"
    logger.info("自动合并历史记录已{}", msg)


def update_generator_xlsx(flg: bool):
    if flg:
        xlsx_generator.open()
    else:
        xlsx_generator.close()
