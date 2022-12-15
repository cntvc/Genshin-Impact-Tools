from genshin.config import settings
from genshin.config.user_setting import update_auto_merge
from genshin.module.gacha import export, merge


menu_item = {
    "description": "主菜单",
    "options": [
        {
            "description": "导出抽卡数据",
            "options": [
                {
                    "description": "通过游戏缓存导出",
                    "options": lambda: export.export(settings.URL_SOURCE_GAMECACHE),
                },
                {
                    "description": "通过软件缓存链接导出",
                    "options": lambda: export.export(settings.URL_SOURCE_CONFIG),
                },
                {
                    "description": "通过剪切板导出",
                    "options": lambda: export.export(settings.URL_SOURCE_CLIPBOARD),
                },
            ],
        },
        {"description": "合并抽卡记录", "options": lambda: merge()},
        {
            "description": "软件设置",
            "options": [
                {
                    "description": "自动合并历史记录",
                    "options": [
                        {
                            "description": "打开自动合并历史记录",
                            "options": lambda: update_auto_merge(settings.OPEN),
                        },
                        {
                            "description": "关闭自动合并历史记录",
                            "options": lambda: update_auto_merge(settings.CLOSE),
                        },
                    ],
                },
            ],
        },
    ],
}


if __name__ == "__main__":
    from genshin.module.menu import Menu
    menu = Menu(menu_item)
    menu.run()
