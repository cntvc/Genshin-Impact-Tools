from genshin.config import update_and_save
from genshin.core import logger


def set_auto_merge(flg: bool):
    update_and_save("FLAG_AUTO_MERGE", flg)
    msg = "关闭"
    if flg:
        msg = "打开"
    logger.info("自动合并历史记录已{}", msg)


def set_generator_uigf(flg: bool):
    update_and_save("FLAG_GENERATOR_UIGF", flg)
    msg = "关闭"
    if flg:
        msg = "打开"
    logger.info("生成UIGF通用格式数据已{}", msg)


def set_check_update(flg: bool):
    update_and_save("FLAG_CHECK_UPDATE", flg)
    msg = "关闭"
    if flg:
        msg = "打开"
    logger.info("软件更新检测已{}", msg)
