"""
test setting module
"""

from genshin.config import _remove_dict, is_user_setting, reload_config, settings, update_config


def test_get_value():
    """
    test get global setting var
    """
    assert settings.FLAG_EXPORT_XLSX is True


def test_fresh_reload():
    """
    test fresh reload setting var from source
    """
    settings.update(FLAG_CHECK_UPDATE=False)
    assert settings.FLAG_CHECK_UPDATE is False
    assert reload_config("FLAG_CHECK_UPDATE") is True


def test_remove_dict():
    """
    test user setting list
    remove another setting list
    """
    data = _remove_dict(settings.as_dict(), settings.USER_SETTING_LIST)
    user_settings = [key for key, _ in data.items()]
    assert user_settings.sort() == settings.USER_SETTING_LIST.sort()


def test_update_config():
    """
    test update user setting
    """
    key = "FLAG_CHECK_UPDATE"
    value = False
    update_config(key, value)
    assert False is settings[key]


def test_is_user_config():
    """test setting item is user config"""
    assert is_user_setting("TIMEOUT") is False
    assert is_user_setting("FLAG_CHECK_UPDATE") is True
