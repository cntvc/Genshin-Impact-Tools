from genshin.config import update_and_save
from genshin.core import logger


def update_auto_merge(flg: bool):
    update_and_save("FLAG_AUTO_MERGE", flg)
    msg = "关闭"
    if flg:
        msg = "打开"
    logger.info("自动合并历史记录已{}", msg)
