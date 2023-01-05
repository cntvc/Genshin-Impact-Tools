"""update"""
import json

from genshin import __version__ as version
from genshin.core.function import clear_screen, request_get
from genshin.core.log import logger

GITHUB_RELEASE_URL = "https://api.github.com/repos/cntvc/Genshin-Impact-Tools/releases/latest"


def get_latest_tag(url: str):
    """
    获取最后的Release信息
    """
    response = request_get(url)
    if not response:
        return ""
    data = json.loads(response)
    if "tag_name" not in data:
        return ""
    return data["tag_name"]


def check_update():
    """
    check app is need update
    """
    logger.info("检测软件更新中...")
    tag = get_latest_tag(GITHUB_RELEASE_URL)
    if not tag:
        logger.warning("检测更新失败\n")
        return
    if tag != version:
        clear_screen()
        logger.info("软件有新版本，可前往以下链接下载最新版本")
        logger.info(GITHUB_RELEASE_URL)
    else:
        logger.info("软件已是最新版本\n")
