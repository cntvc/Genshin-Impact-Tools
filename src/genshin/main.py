import math
from typing import Callable

from genshin.config import settings
from genshin.config.user_setting import (update_auto_merge,
                                         update_generator_xlsx)
from genshin.core.function import clear_screen, input_int, pause
from genshin.module.gacha import export, merge


class Menu:
    def __init__(self, menu: dict) -> None:
        self.menu = menu
        self.stack = []
        self.stack.append(menu)

    def display(self):
        """
        show menu content
        """
        clear_screen()
        # 让标题打印在中间
        DEFAULT_LENGTH = 40
        description: str = self.menu["description"]
        space_size = math.floor((DEFAULT_LENGTH - len(description)) / 2)
        print(" " * space_size + description)
        print("========================================")
        options: list = self.menu["options"]
        for index, option in enumerate(options):
            print("{}.{}".format(index + 1, option["description"]))
        print("")
        if len(self.stack) > 1:
            print("0.返回上级菜单")
        else:
            print("0.退出程序")
        print("========================================")

    def run(self):
        while self.stack:
            # 获取当前菜单
            self.menu = self.stack[-1]
            self.display()
            options: list = self.menu["options"]
            print("请输入数字选择菜单项:")
            choice = input_int(0, len(options))

            # 根据当前菜单的内容的类型进行相应的处理
            if choice == 0:
                self.stack.pop()
                continue

            # option : (Callable | list)
            option = options[choice - 1]["options"]

            if isinstance(option, list):
                self.stack.append(options[choice - 1])
                self.display()
                self.run()
            elif isinstance(option, Callable):
                option()
                pause()
                self.display()


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
                    "description": "导出XLSX文件",
                    "options": [
                        {
                            "description": "打开导出XLSX文件",
                            "options": lambda: update_generator_xlsx(settings.OPEN),
                        },
                        {
                            "description": "关闭导出XLSX文件",
                            "options": lambda: update_generator_xlsx(settings.CLOSE),
                        },
                    ],
                },
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

menu = Menu(menu_item)

if __name__ == "__main__":
    menu.run()
