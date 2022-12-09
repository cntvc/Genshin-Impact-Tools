"""
gacha data export
"""
import abc
from pathlib import Path
from typing import List, Optional

from genshin.config import settings, update_and_save
from genshin.core import logger
from genshin.module.gacha.data_struct import (GACHA_QUERY_TYPE_IDS,
                                              GACHA_TYPE_DICT)


class AbstractGenerator(metaclass=abc.ABCMeta):
    def __init__(self, data: Optional[dict], uid: Optional[str]) -> None:
        self.data = data
        self.uid = uid

    @abc.abstractmethod
    def generator(self):
        pass

    @abc.abstractmethod
    def open(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    def status(self):
        pass


class XLSXGenerator(AbstractGenerator):
    def __init__(self, data: Optional[dict], uid: Optional[str]) -> None:
        super().__init__(data, uid)

    def open(self):
        update_and_save("FLAG_EXPORT_XLSX", True)
        logger.info("导出为XLSX文件已打开")

    def close(self):
        update_and_save("FLAG_EXPORT_XLSX", False)
        logger.info("导出为XLSX文件已关闭")

    def status(self):
        return settings.FLAG_EXPORT_XLSX

    def get_xlsx_path(self):
        """
        return XLSX file fullpath
        """
        return Path(settings.USER_DATA_PATH, self.uid, "抽卡数据总览.xlsx").as_posix()

    def generator(self):
        try:
            from xlsxwriter import Workbook
        except ImportError as e:
            logger.error("module Workbook import error", e)
            raise

        workbook_path = self.get_xlsx_path()
        logger.debug("创建工作簿: " + workbook_path)
        workbook = Workbook(workbook_path)

        # init title and content format
        content_css = workbook.add_format(
            {
                "align": "left",
                "font_name": "微软雅黑",
                "border_color": "#c4c2bf",
                "bg_color": "#ebebeb",
                "border": 1,
            }
        )
        title_css = workbook.add_format(
            {
                "align": "left",
                "font_name": "微软雅黑",
                "color": "#757575",
                "bg_color": "#dbd7d3",
                "border_color": "#c4c2bf",
                "border": 1,
                "bold": True,
            }
        )

        star_5 = workbook.add_format({"color": "#bd6932", "bold": True})
        star_4 = workbook.add_format({"color": "#a256e1", "bold": True})
        star_3 = workbook.add_format({"color": "#8e8e8e"})

        for gacha_type_id in GACHA_QUERY_TYPE_IDS:
            gacha_type_List = self.data["list"][gacha_type_id][:]
            gacha_type_name = GACHA_TYPE_DICT[gacha_type_id]

            logger.debug("开始写入 {}, 共 {} 条数据", gacha_type_name, len(gacha_type_List))
            worksheet = workbook.add_worksheet(gacha_type_name)
            excel_header = ["总次数", "时间", "名称", "类别", "星级", "祈愿类型", "保底内抽数"]

            worksheet.set_column("B:B", 22)
            worksheet.set_column("C:C", 14)
            worksheet.set_column("F:F", 16)

            worksheet.write_row(0, 0, excel_header, title_css)

            worksheet.freeze_panes(1, 0)

            total_counter = 0
            pity_counter = 0
            for gacha in gacha_type_List:
                time_str = gacha["time"]
                name = gacha["name"]
                item_type = gacha["item_type"]
                rank_type = int(gacha["rank_type"])
                gacha_type = gacha["gacha_type"]
                gacha_type_name = GACHA_TYPE_DICT.get(gacha_type, "")
                total_counter = total_counter + 1
                pity_counter = pity_counter + 1
                excel_data = [
                    total_counter,
                    time_str,
                    name,
                    item_type,
                    rank_type,
                    gacha_type_name,
                    pity_counter,
                ]
                worksheet.write_row(total_counter, 0, excel_data, content_css)
                if rank_type == 5:
                    pity_counter = 0

            first_row = 1  # 不包含表头第一行 (zero indexed)
            first_col = 0  # 第一列
            last_row = len(gacha_type_List)  # 最后一行
            last_col = len(excel_header) - 1  # 最后一列，zero indexed 所以要减 1
            worksheet.conditional_format(
                first_row,
                first_col,
                last_row,
                last_col,
                {"type": "formula", "criteria": "=$E2=5", "format": star_5},
            )
            worksheet.conditional_format(
                first_row,
                first_col,
                last_row,
                last_col,
                {"type": "formula", "criteria": "=$E2=4", "format": star_4},
            )
            worksheet.conditional_format(
                first_row,
                first_col,
                last_row,
                last_col,
                {"type": "formula", "criteria": "=$E2=3", "format": star_3},
            )

        workbook.close()
        logger.debug("工作簿写入完成")
        return True


class ReportManager:
    def __init__(self, data: Optional[dict], uid: Optional[str]) -> None:
        self.data = data
        self.uid = uid
        self.generators: List[AbstractGenerator] = []

    def generator_report(self):
        for generator in self.generators:
            if not generator.status():
                continue
            generator.data = self.data
            generator.uid = self.uid
            generator.generator()

    def add_generator(self, generator: AbstractGenerator):
        self.generators.append(generator)


xlsx_generator = XLSXGenerator(None, None)

report = ReportManager(None, None)
report.add_generator(xlsx_generator)