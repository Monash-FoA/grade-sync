from sheets.modules.base import MapperSection, register
from sheets.workbook import Workbook, TableConfig

@register("ID")
class IDSection(MapperSection):

    def __init__(self, section_data: dict, id_data: str, table_config: TableConfig) -> None:
        super().__init__(section_data, id_data, table_config)
        self.workbook = Workbook.from_options(section_data)
        self.header_row = section_data["header_row"]
        self.header_vals = self.workbook.row_values(self.header_row)
        self.source = section_data["source"]
        self.dest = section_data["dest"]

    def get_data(self, map_sheet: Workbook, id_values: list, sections: dict):
        return self.workbook.col_values(self.header_vals.index(self.source)+1)[self.header_row:]

    def get_headers(self):
        return [self.dest]

    def update_data(self, map_sheet: Workbook, col_index: int, id_values: list, sections: dict):
        map_sheet.update_values(self.table_config.VALUES_BEGIN_ROW-1, self.table_config.VALUES_BEGIN_ROW+len(self.data)-2, col_index, col_index, [[i] for i in self.data])
