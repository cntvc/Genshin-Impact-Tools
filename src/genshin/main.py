"""Main"""
from genshin.config import settings
from genshin.module.gacha import ExportFactory
from genshin.module.menu import Menu, MenuItem

if __name__ == "__main__":
    export_factory = ExportFactory()
    app_setting = []
    export_op = [
        MenuItem(
            "通过游戏缓存文件导出",
            export_factory.export,
            [],
            None,
            url_source=settings.URL_SOURCE_GAMECACHE,
        ),
        MenuItem(
            "通过剪切板导出",
            export_factory.export,
            [],
            None,
            url_source=settings.URL_SOURCE_CLIPBOARD,
        ),
        MenuItem(
            "通过配置文件导出",
            export_factory.export,
            [],
            None,
            url_source=settings.URL_SOURCE_CONFIG
        ),
    ]
    main_op = [
        MenuItem("抽卡记录", None, export_op, None),
        MenuItem("软件设置", None, app_setting, None),
    ]
    root_op = MenuItem("Genshin Impact Tools", None, main_op, None)
    menu = Menu(root_op)
    menu.display()
    menu.select_option()
