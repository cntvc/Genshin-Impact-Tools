"""
Menu
"""
from typing import Callable, Optional

from genshin.core.function import clear_screen, input_int, pause


class MenuItem:
    """
    Menu item
    """

    def __init__(
        self,
        name: str,
        func: Optional[Callable],
        options: list,
        parent,  # parent Option
        *args,  # func parameter
        **kwargs,  # func parameter
    ) -> None:
        """
        Parameters
        ----------
        name : |str|    menu name
        func : |Callable, Optional|    select this item will call func
        options : |list[MenuItem]|  sub menu list
        parent : |MenuItem, Optional|   parent menu
        """
        self._name = name
        self._func = func
        self._options = []
        self.options = options
        self._parent = parent
        self._args = args
        self._kwargs = kwargs

    def __str__(self) -> str:
        return (
            f"name: {self.name}\n"
            f"func: {self.func}\n"
            f"options: {self.options}\n"
            f"parent: {self.parent}\n"
            f"args: {self._args}\n"
            f"kwargs: {self._kwargs}\n"
        )

    @property
    def name(self):
        """name"""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def func(self):
        """func"""
        return self._func

    @func.setter
    def func(self, func: Optional[Callable]):
        self._func = func

    @property
    def options(self):
        """options"""
        return self._options

    @options.setter
    def options(self, menus: list):
        for menu in menus:
            menu.parent = self
            self.options.append(menu)

    @property
    def parent(self):
        """parent"""
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def args(self):
        """*args"""
        return self._args

    @args.setter
    def args(self, *args):
        self._args = args

    @property
    def kwargs(self):
        """**kwargs"""
        return self._kwargs

    @kwargs.setter
    def kwargs(self, **kwargs):
        self._kwargs = kwargs


class Menu:
    """
    control MenuItem and show current MenuItem
    """

    def __init__(self, root_op: MenuItem) -> None:
        self._current_op = root_op

    def display(self):
        """
        show menu content
        """
        clear_screen()

        print("======================================")
        for index, option in enumerate(self._current_op.options):
            print(f"{index+1}.{option.name}")
        print("")
        print("0.返回上级菜单")
        print("======================================")

    def select_option(self):
        """
        jump between menu items based on actions
        """
        print("请输入数字选择菜单项:")
        while True:
            index = input_int(0, len(self._current_op.options))

            if index == 0:
                parent = self._current_op.parent
                if parent:
                    self._current_op = parent
                    self.display()
                    self.select_option()
                else:
                    print("当前已为主菜单，无父菜单项")
                    continue
            else:
                select_op: MenuItem = self._current_op.options[index - 1]

                # if op type is func, call func()
                if select_op.func:
                    select_op.func(*select_op.args, **select_op.kwargs)
                    pause()
                    self.display()

                # if op type is Option, display child list
                else:
                    self._current_op = select_op
                    self.display()
                    self.select_option()
