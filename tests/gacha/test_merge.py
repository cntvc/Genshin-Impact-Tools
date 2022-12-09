import os
from pathlib import Path
from genshin.module.gacha import merge
from genshin.config import settings
from genshin.core import logger

from genshin.module.gacha.data_struct import GACHA_QUERY_TYPE_IDS
from genshin.core.function import load_json

def test_merge():
    merge()
    path = Path(settings.USER_DATA_PATH, "123456788", "gacha_data.json")
    assert path.exists()
    data = load_json(path)
    assert len(data["list"]["100"]) == 2
    assert len(data["list"]["200"]) == 0
    assert len(data["list"]["301"]) == 3
    assert len(data["list"]["302"]) == 5