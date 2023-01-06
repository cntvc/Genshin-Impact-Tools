import math
from typing import Callable

from genshin.core.function import clear_screen, input_int, pause


class Menu:
    """
    Menu item eg:
    {
        "description": "main menu",
        "options": [
            {
                "description": "sub_menu_1",
                "options": [],
            },
            {
                "description": "sub_menu_2",
                "options": lambda: func_3(),
            },
        ]
    }
    """

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
            print("0.退出菜单")
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
