"""clipboard tools"""
from typing import Optional

import win32clipboard
import win32con

from genshin.core import logger


def get_clipboad_text_or_html() -> Optional[str]:
    """get str from clipboad"""
    try:
        formats = []
        win32clipboard.OpenClipboard(0)

        # 注册 CF_HTML 格式剪贴板
        CF_HTML = win32clipboard.RegisterClipboardFormat("HTML Format")
        CF_TEXT = win32con.CF_TEXT
        logger.debug(f"CF_HTML={CF_HTML}")

        cf = win32clipboard.EnumClipboardFormats(0)
        while cf != 0:
            formats.append(cf)
            cf = win32clipboard.EnumClipboardFormats(cf)
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
    except Exception as err:
        logger.error(f"读取剪贴板错误 {err}")
        return None
    finally:
        win32clipboard.CloseClipboard()
