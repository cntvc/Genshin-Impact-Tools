"""Main"""
from genshin.config import settings
from genshin.module.gacha import export_manager, xlsx_generator
from genshin.module.menu import Menu, MenuItem


def create_user_setting():
    xlsx_op = [
        MenuItem("关闭导出XLSX文件", xlsx_generator.close, [], None),
        MenuItem("打开导出XLSX文件", xlsx_generator.open, [], None)
    ]
    user_setting = [
        MenuItem("设置导出XLSX文件", None, xlsx_op, None),
    ]
    return user_setting


def create_export_menu():
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
    return export_menu


def init_menu():
    main_op = [
        MenuItem("抽卡记录", None, create_export_menu(), None),
        MenuItem("生成抽卡报告", None, [], None),
        MenuItem("软件设置", None, create_user_setting(), None),
    ]
    root_op = MenuItem("Genshin Impact Tools", None, main_op, None)
    menu = Menu(root_op)
    return menu


if __name__ == "__main__":
    menu = init_menu()
    menu.display()
    menu.select_option()
