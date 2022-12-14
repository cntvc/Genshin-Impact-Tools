"""clipboard tools"""
from typing import Optional

import win32api
import win32clipboard
import win32con

from genshin.core import logger


def get_clipboad_text_or_html() -> Optional[str]:
    """get str from clipboad"""
    logger.debug("尝试读取剪切板")
    try:
        formats = []
        win32clipboard.OpenClipboard(0)

        # 注册 CF_HTML 格式剪贴板
        # https://learn.microsoft.com/zh-cn/windows/win32/dataxchg/html-clipboard-format
        CF_HTML = win32clipboard.RegisterClipboardFormat("HTML Format")
        CF_TEXT = win32con.CF_TEXT
        logger.debug(f"CF_HTML={CF_HTML}")

        clipboard_format = win32clipboard.EnumClipboardFormats(0)
        while clipboard_format != 0:
            formats.append(clipboard_format)
            clipboard_format = win32clipboard.EnumClipboardFormats(clipboard_format)
        logger.debug(f"EnumClipboardFormats={formats}")

        if CF_HTML in formats:
            data = win32clipboard.GetClipboardData(CF_HTML)
        elif CF_TEXT in formats:
            data = win32clipboard.GetClipboardData(CF_TEXT)
        else:
            return None

        logger.debug(f"GetClipboardData={data}")
        if isinstance(data, bytes):
            data = data.decode(errors="ignore")
        if not isinstance(data, str):
            return None

        return data
    except win32api.error as err:
        logger.error(f"读取剪贴板错误 {err}")
        return None
    finally:
        win32clipboard.CloseClipboard()
