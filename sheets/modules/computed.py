from sheets.modules.base import MapperSection, register
from sheets.workbook import Workbook
from sheets.util import eval_query

@register("Computed")
class ComputedSection(MapperSection):

    def get_headers(self):
        return [
            i["dest"]
            for i in self.section_data["items"]
        ]

    def get_data(self, map_sheet: Workbook, id_values: list, sections: dict):
        data = [
            ["" for _ in range(len(self.section_data["items"]))]
            for _ in range(len(id_values))
        ]
        cur_header = map_sheet.row_values(self.table_config.COLUMN_NAME_ROW)
        row_vals = map_sheet.get_values(self.table_config.VALUES_BEGIN_ROW-1, self.table_config.VALUES_BEGIN_ROW+len(id_values)-2, 0, self.col_index-1)

        for idx in range(len(id_values)):
            vals = row_vals[idx]

            for i, item in enumerate(self.section_data["items"]):
                data[idx][i] = eval_query(item["source"], sections, cur_header, vals)
        return data

    def update_data(self, map_sheet: Workbook, col_index: int, id_values: list, sections: dict):
        map_sheet.update_values(self.table_config.VALUES_BEGIN_ROW-1, self.table_config.VALUES_BEGIN_ROW+len(id_values)-2, col_index, col_index + len(self.section_data["items"])-1, self.data)
