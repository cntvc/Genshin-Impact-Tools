"""
Configuration center.
Use https://www.dynaconf.com/
""" ""
import os
from pathlib import Path

from dynaconf import Dynaconf, loaders

# Load default config.
_settings_files = [Path(__file__).parent / "global_setting.py"]

# Load user config, will cover default setting item
_user_config_path = Path(
    os.getenv("LocalAppData"), "Genshin-Impact-Tools", "config", "settings.toml"
)

# custom configuration. It will be cover default config
_external_files = [_user_config_path]

settings = Dynaconf(
    core_loaders=["TOML", "PY"],
    # Loaded at the first
    preload=[],
    # Loaded second (the main file)
    settings_files=_settings_files,
    # Loaded at the end
    includes=_external_files,
    # If False, can't use `settings.foo`, but can only use `settings.FOO`
    lowercase_read=False,
    # Always reloaded from source without the need to reload the application
    # eg: fresh_vars=["password"]
    fresh_vars=[],
)


def reload_config(key):
    """
    this setting is being freshly reloaded from source
    """
    return settings.get_fresh(key)


def is_user_setting(key: str):
    """
    verify setting item in user setting list
    """
    if key not in settings.USER_SETTING_LIST:
        return False
    return True


def update_config(key: str, value):
    """
    update user setting
    """
    if not is_user_setting(key):
        return
    settings.update({key: value})


def update_and_save(key: str, value):
    """
    update and save user setting to file
    """
    update_config(key, value)
    save_config()


def _remove_dict(data: dict, save_list: list) -> dict:
    """
    from data remove key/value if key in save_list
    """
    return {key: val for key, val in data.items() if key in save_list}


def save_config(path=_user_config_path, environment=None):
    """
    save user setting
    """
    if not path.parent.exists():
        os.makedirs(path.parent)
    if not path.exists():
        path.touch()
    data = settings.as_dict(env=environment)
    data = _remove_dict(data, settings.USER_SETTING_LIST)
    loaders.write(path.as_posix(), data, env=environment)
