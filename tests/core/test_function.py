"""Test core function"""
import os
import tempfile
import unittest

from genshin.core.function import load_json, save_json


class TestLoadJson(unittest.TestCase):
    """test load_json function"""

    def test_load_json(self):
        """测试正常情况"""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as file:
            file.write('{"foo": "bar"}')
            file.seek(0)
        data = load_json(file.name)
        self.assertIsNotNone(data)
        os.unlink(file.name)

    def test_load_json_nonexistent(self):
        """test file is not exist"""
        data = load_json("nonexistent.json")
        self.assertIsNone(data)

    def test_load_json_invalid(self):
        """test JSON data format is not correct"""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as file:
            file.write('{"foo": "bar", ')
            file.seek(0)
        data = load_json(file.name)
        self.assertIsNone(data)
        os.unlink(file.name)


class TestSaveJson(unittest.TestCase):
    """test save_json function"""

    tmp_path = tempfile.gettempdir()
    data = {"key": "value"}
    path = tmp_path + "/aa.json"

    def test_save_json(self):
        """test save_json success"""
        res = save_json(self.path, self.data)
        self.assertTrue(res)
        os.unlink(self.path)

    def test_save_json_failed(self):
        """test can't open file"""
        with tempfile.NamedTemporaryFile(mode="w+") as file:
            file.write('{"foo": "bar", ')
            file.seek(0)
            res = save_json(file.name, self.data)
            self.assertFalse(res)
