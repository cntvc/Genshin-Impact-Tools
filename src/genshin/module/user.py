import os
import re
from pathlib import Path

from genshin.config import settings
from genshin.core import logger, singleton
from genshin.core.function import input_int, load_json, save_json


@singleton
class User:
    uid_re = re.compile("^[0-9]{9}$")

    def __init__(self) -> None:
        self._uid: str = ""
        self._area: str = ""
        self._gacha_url: str = ""

    def _get_user_list(self):
        """
        扫描程序预定路径下的目录，找到为9位数字的目录，读取config文件，如果存在uid，即为一个有效账户
        """
        if not os.path.isdir(settings.USER_DATA_PATH):
            return []
        file_list = os.listdir(settings.USER_DATA_PATH)
        # save folders with digit name
        for name in file_list:
            if os.path.isfile(name):
                file_list.remove(name)
            elif None is self.uid_re.match(name):
                file_list.remove(name)

        user_list = []
        # read config.json
        for folder in file_list:
            path = Path(settings.USER_DATA_PATH, folder, "config.json")
            if not path.exists():
                continue

            config = load_json(path)
            if not config or ("uid" not in config):
                continue
            logger.debug("检测到 {} 配置文件", config["uid"])
            user_list.append(config)
        return user_list

    def _set_uid_by_input(self):
        """接收用户输入以初始化uid"""
        while True:
            print("请输入您的uid，输入0取消输入")
            input_uid = input()
            if len(input_uid) == 1 and input_uid == "0":
                return
            if self.set_uid(input_uid):
                break

    def init(self):
        """
        扫描目录初始化uid和area
        """
        user_config_list = self._get_user_list()
        self._choose_user(user_config_list)

    def _choose_user(self, user_config_list):
        """
        提供菜单选择用户以初始化
        """
        length = len(user_config_list)
        print("========================================")
        for index in range(length):
            print("{}.{}".format(index + 1, user_config_list[index]["uid"]))
        print("{}.{}".format(length + 1, "输入新用户"))
        print("0.退出选择")
        print("========================================")
        choose = input_int(0, length + 1)
        if choose == 0:
            return
        elif choose == length + 1:
            self._set_uid_by_input()
        else:
            self.set_uid(user_config_list[choose - 1]["uid"])

    def reset(self):
        """reset user data"""
        self._uid = ""
        self._area = ""
        self._gacha_url = ""

    def get_uid(self):
        return self._uid

    def set_uid(self, uid: str):
        if not self._verify_uid(uid):
            return False
        self._uid = uid
        self._set_area()
        return True

    def _verify_uid(self, uid: str):
        if len(uid) != 9 or (None is self.uid_re.fullmatch(uid)):
            logger.warning("UID格式错误")
            return False
        return True

    def _set_area(self):
        """
        根据uid开头编号设置地区
        """
        # TODO 范围需考证
        if self._uid[0] <= "9" and self._uid[0] >= "6":
            self._area = "global"
        else:
            self._area = "cn"

    def get_area(self):
        """get server area"""
        return self._area

    def set_gacha_url(self, url):
        self._gacha_url = url

    def get_gacha_url(self):
        return self._gacha_url

    def save_config(self):
        """缓存用户信息"""
        if not self._uid:
            logger.warning("UID为空，缓存用户信息失败")
            return False
        config_path = Path(settings.USER_DATA_PATH, self._uid, "config.json")
        user_data = load_json(config_path)
        if not user_data:
            user_data = {}
        user_data["uid"] = self._uid
        user_data["gacha_url"] = self._gacha_url
        user_data["area"] = self._area
        if not save_json(config_path, user_data):
            logger.warning("文件无法写入，缓存用户信息失败")
            return False
        return True

    def load_config(self):
        config_path = Path(settings.USER_DATA_PATH, self._uid, "config.json")
        if not config_path.exists():
            return {}
        return load_json(config_path)


user = User()
