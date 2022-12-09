"""
Default settings.
"""
from pathlib import Path

#####################################################
# Core                                              #
#####################################################

# Application running directory
APP_RUN_PATH = Path.cwd().as_posix()

# Application data directory, include config, log ...
APP_DATA_PATH = Path(Path.home(), "AppData", "Local", "Genshin-Impact-Tools").as_posix()

# Application config directory
APP_CONFIG_PATH = Path(APP_DATA_PATH, "config").as_posix()

# Application log directory
APP_LOG_PATH = Path(APP_DATA_PATH, "log", "log_{time:YYYY-MM}.log").as_posix()

# Application temporary files
APP_TMP_PATH = Path(APP_DATA_PATH, "tmp").as_posix()

# Game data cache path
MIHOYO_CHAHE_PATH = Path(Path.home(), "AppData", "LocalLow", "miHoYo").as_posix()

# Request timeout limit
TIMEOUT = 10

OPEN = True

CLOSE = False

#####################################################
# Export gacha log URL source type                  #
#####################################################

URL_SOURCE_CONFIG = 1

URL_SOURCE_CLIPBOARD = 2

URL_SOURCE_GAMECACHE = 3


#####################################################
# User Setting                                      #
#                                                   #
# user modifiable options                           #
#####################################################

USER_DATA_PATH = APP_RUN_PATH + "/Genshin_Impact_tools"

# Check update application
FLAG_CHECK_UPDATE = True

# generator xlsx report
FLAG_EXPORT_XLSX = True

# auto merge history data
FLAG_AUTO_MERGE = True

# List of user configurable options
USER_SETTING_LIST = [
    "FLAG_CHECK_UPDATE",
    "FLAG_EXPORT_XLSX",
    "FLAG_AUTO_MERGE",
]
