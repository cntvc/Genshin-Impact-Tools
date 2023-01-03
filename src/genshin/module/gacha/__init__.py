"""gacha module"""
import os
from pathlib import Path

from genshin.config import settings
from genshin.core import logger
from genshin.core.function import load_json, save_json
from genshin.module.gacha.data_transform import load_gacha_data, merge_data, varify_data
from genshin.module.gacha.gacha_log import GachaLog
from genshin.module.gacha.gacha_url import UrlFactory, verify_url
from genshin.module.gacha.report_gengrator import report
from genshin.module.user import user


def export(url_source: int):
    url_product = UrlFactory.produce(url_source)
    if url_source != settings.URL_SOURCE_CLIPBOARD:
        if url_source == settings.URL_SOURCE_CONFIG:
            # 从配置文件导出数据，不打印新建用户选项
            user.init(False)
        else:
            user.init()
        if not user.get_uid():
            logger.warning("未设置UID，无法导出")
            return
        else:
            logger.info("当前UID为: {}", user.get_uid())

    user.set_gacha_url(url_product.get_url())

    if not user.get_gacha_url() or not verify_url(user.get_gacha_url()):
        logger.warning("导出失败，请尝试其他方法")
        user.reset()
        return
    gacha_log = GachaLog(user.get_gacha_url())
    data, uid = gacha_log.query()
    if user.get_uid() != uid:
        logger.warning("UID与预设不同，当前数据UID:{}", uid)
        user.set_uid(uid)

    gacha_data_path = Path(settings.USER_DATA_PATH, user.get_uid(), "gacha_data.json")
    if settings.FLAG_AUTO_MERGE:
        history = load_json(gacha_data_path)
        if history:
            logger.info("合并历史数据")
            data = merge_data([data, history])

    if not save_json(gacha_data_path, data):
        logger.warning("保存抽卡数据失败，请尝试其他方法")
        user.reset()
        return
    logger.info("原始抽卡数据导出成功")
    user.save_config()
    report.data = data
    report.uid = user.get_uid()
    report.generator_report()
    user.reset()


def merge():
    """合并抽卡数据，支持UIGF，默认扫描目录: "./Genshin_impact_tools/merge"

    支持的文件格式: [xlsx | json]
    """
    path = Path(settings.USER_DATA_PATH, "merge")
    if not path.exists():
        os.makedirs(path)
        logger.warning("目录 {} 不存在，已为您创建该目录\n请将需要合并的数据文件放入'merge'文件夹，再运行此功能", path)
        return False

    file_suffix = ["xlsx", "json"]
    files = [file for file in os.listdir(path) if any(file.endswith(ext) for ext in file_suffix)]

    if not files:
        logger.warning("未检测到可合并文件")
        return
    logger.info("共扫描到 {} 个可合并文件", len(files))

    datas = []
    for file in files:
        data = load_gacha_data(Path(path, file))
        if not varify_data(data):
            logger.warning("文件 '{}' 中数据异常，此文件不会被合并", file)
            continue

        # 校验数据，存在不同用户的数据，打印并退出合并
        if not user.get_uid():
            user.set_uid(data["info"]["uid"])
        elif user.get_uid() != data["info"]["uid"]:
            logger.warning("数据中存在不同用户抽卡记录，无法继续合并，请检查数据文件后重试")
            user.reset()
            return
        datas.append(data)

    logger.info("合并数据中...")
    data = merge_data(datas)
    user_gacha_path = Path(settings.USER_DATA_PATH, user.get_uid(), "gacha_data.json")
    history_data = load_json(user_gacha_path)
    # 如果有原数据，则与原数据合并
    if history_data:
        data = merge_data([data, history_data])
    logger.info("合并数据完成")
    save_json(user_gacha_path, data)
    user.save_config()
    report.data = data
    report.uid = data["info"]["uid"]
    report.generator_report()
    user.reset()


def generator_report():
    user.init(False)
    if not user.get_uid():
        logger.warning("未设置UID，无法生成报告")
        return
    gacha_data_path = Path(settings.USER_DATA_PATH, user.get_uid(), "gacha_data.json")
    if not gacha_data_path.exists():
        logger.warning("无原始数据文件，无法生成报告")
        user.reset()
        return
    gacha_data = load_json(gacha_data_path)
    if not gacha_data:
        logger.error("数据错误，无法生成报告")
        user.reset()
        return
    report.data = gacha_data
    report.uid = user.get_uid()
    report.generator_report()
    user.reset()
