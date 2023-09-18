from __future__ import annotations

from abc import ABC, abstractmethod
from sheets.workbook import Workbook, TableConfig

SECTIONS: dict[str, MapperSection] = {}

def register(name):
    def func(klass):
        SECTIONS[name] = klass
        return klass
    return func

class MapperSection(ABC):

    def __init__(self, section_data: dict, id_data: str, table_config: TableConfig) -> None:
        self.section_data = section_data
        self.table_config = table_config

    @abstractmethod
    def get_data(self, map_sheet: Workbook, id_values: list, sections: dict):
        pass

    @abstractmethod
    def update_data(self, map_sheet: Workbook, col_index: int, id_values: list, sections: dict):
        pass

    @abstractmethod
    def get_headers(self):
        pass

    def action(self, map_sheet: Workbook, col_index: int, id_values: list, sections: dict):
        headers = self.get_headers()
        display = [self.section_data["display"] for _ in range(len(headers))]
        self.col_index = col_index
        self.data = self.get_data(map_sheet, id_values, sections)
        map_sheet.update_values(self.table_config.COLUMN_NAME_ROW-1, self.table_config.COLUMN_NAME_ROW-1, col_index, col_index + len(headers)-1, [headers])
        map_sheet.update_values(self.table_config.DISPLAY_ROW-1, self.table_config.DISPLAY_ROW-1, col_index, col_index + len(display)-1, [display])
        self.update_data(map_sheet, col_index, id_values, sections)
        return col_index + len(headers)

    def set_user(self, header, row_vals):
        self.user_header = header
        self.user_row_vals = row_vals

    def __getitem__(self, key):
        my_headers = self.get_headers()
        if key not in my_headers:
            raise KeyError(key)
        return self.user_row_vals[self.col_index + my_headers.index(key)]

    def __iter__(self):
        return iter([self.user_row_vals[self.col_index:self.col_index+len(self.get_headers())]])
