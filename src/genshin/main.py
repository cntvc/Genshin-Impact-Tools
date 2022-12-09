from genshin.config import settings
from genshin.config.user_setting import (update_auto_merge,
                                         update_generator_xlsx)
from genshin.module.gacha import ExportManager, merge
from genshin.module.menu import Menu, MenuItem


def init_menu():
    export_manager = ExportManager()
    xlsx_op = [
        MenuItem("打开 导出XLSX文件", update_generator_xlsx, [], None, True),
        MenuItem("关闭 导出XLSX文件", update_generator_xlsx, [], None, False),
    ]
    auto_merge = [
        MenuItem("打开 自动合并历史抽卡记录", update_auto_merge, [], None, True),
        MenuItem("关闭 自动合并历史抽卡记录", update_auto_merge, [], None, False),
    ]
    user_setting = [
        MenuItem("设置导出XLSX文件", None, xlsx_op, None),
        MenuItem("设置自动合并历史抽卡记录", None, auto_merge, None),
    ]
    export_menu = [
        MenuItem(
            "通过游戏缓存文件导出",
            export_manager.export,
            [],
            None,
            url_source=settings.URL_SOURCE_GAMECACHE,
        ),
        MenuItem(
            "通过剪切板导出",
            export_manager.export,
            [],
            None,
            url_source=settings.URL_SOURCE_CLIPBOARD,
        ),
        MenuItem(
            "通过配置文件导出",
            export_manager.export,
            [],
            None,
            url_source=settings.URL_SOURCE_CONFIG
        ),
    ]
    main_op = [
        MenuItem("导出抽卡记录", None, export_menu, None),
        MenuItem("合并抽卡记录", merge, [], None),
        MenuItem("软件设置", None, user_setting, None),
    ]
    root_op = MenuItem("Genshin Impact Tools", None, main_op, None)
    menu = Menu(root_op)
    return menu


if __name__ == "__main__":
    menu = init_menu()
    menu.display()
    menu.select_option()
