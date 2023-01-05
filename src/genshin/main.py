import platform
import time

from genshin import __version__ as version
from genshin.config import settings
from genshin.config.user_setting import set_auto_merge, set_generator_uigf
from genshin.core import logger
from genshin.module.gacha import export, generator_report, merge

menu_item = {
    "description": "主菜单",
    "options": [
        {
            "description": "导出抽卡数据",
            "options": [
                {
                    "description": "通过游戏缓存导出",
                    "options": lambda: export(settings.URL_SOURCE_GAMECACHE),
                },
                {
                    "description": "通过软件缓存链接导出",
                    "options": lambda: export(settings.URL_SOURCE_CONFIG),
                },
                {
                    "description": "通过剪切板导出",
                    "options": lambda: export(settings.URL_SOURCE_CLIPBOARD),
                },
            ],
        },
        {"description": "合并抽卡记录", "options": lambda: merge()},
        {"description": "生成抽卡报告", "options": lambda: generator_report()},
        {
            "description": "软件设置",
            "options": [
                {
                    "description": "自动合并历史记录",
                    "options": [
                        {
                            "description": "打开自动合并历史记录",
                            "options": lambda: set_auto_merge(settings.OPEN),
                        },
                        {
                            "description": "关闭自动合并历史记录",
                            "options": lambda: set_auto_merge(settings.CLOSE),
                        },
                    ],
                },
                {
                    "description": "导出UIGF格式数据",
                    "options": [
                        {
                            "description": "打开导出UIGF格式数据",
                            "options": lambda: set_generator_uigf(settings.OPEN),
                        },
                        {
                            "description": "关闭导出UIGF格式数据",
                            "options": lambda: set_generator_uigf(settings.CLOSE),
                        },
                    ],
                },
            ],
        },
    ],
}


def run():
    from genshin.module.menu import Menu

    logger.debug(
        ("start application\nsoftware version:{}\nstart time:{}\nsystem version:{}\n"),
        version,
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        platform.platform(),
    )
    menu = Menu(menu_item)
    menu.run()


if __name__ == "__main__":
    run()
