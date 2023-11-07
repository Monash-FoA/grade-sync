from copy import copy

from sheets.modules.base import MapperSection, register
from sheets.workbook import Workbook, TableConfig

@register("Lookup")
class SheetLookup(MapperSection):

    def __init__(self, section_data: dict, id_data: str, table_config: TableConfig) -> None:
        super().__init__(section_data, id_data, table_config)
        self.workbooks = {}
        self.active_workbook = self.workbooks[section_data["sheet"]] = Workbook.from_options(section_data)
        self.sheet_lookup = section_data.get("sheet_lookup", id_data["dest"])
        self.ref_lookup = section_data.get("ref_lookup", id_data["source"])
        self.items = section_data["items"]


    def get_headers(self):
        return [
            item["dest"]
            for item in self.items
        ]

    def get_data(self, map_sheet: Workbook, id_values: list, sections: list):
        sheet_header_row = map_sheet.row_values(self.table_config.COLUMN_NAME_ROW)
        lookup_vals = map_sheet.col_values(sheet_header_row.index(self.sheet_lookup)+1)[int(self.table_config.COLUMN_NAME_ROW):]
        data = [
            ["" for _ in range(len(self.items))]
            for _ in range(len(lookup_vals))
        ]
        for y, item in enumerate(self.items):
            for j, val in enumerate(self.get_col_data(y, item, map_sheet)):
                data[j][y] = val
        return data

    def prepare_active_workbook(self, item):
        sheet = item.get("sheet", self.section_data["sheet"])
        if sheet not in self.workbooks:
            new_options = copy(self.section_data)
            new_options["sheet"] = sheet
            self.workbooks[sheet] = Workbook.from_options(new_options)
        self.active_workbook = self.workbooks[sheet]

    def get_col_data(self, item_index, item, map_sheet):
        sheet_header_row = map_sheet.row_values(self.table_config.COLUMN_NAME_ROW)
        header_row = item.get("header_row", self.section_data["header_row"])
        header_vals = self.active_workbook.row_values(header_row)

        sheet_lookup = item.get("sheet_lookup", self.sheet_lookup)
        ref_lookup = item.get("ref_lookup", self.ref_lookup)
        self.prepare_active_workbook(item)
        lookup_col_values = self.active_workbook.col_values(header_vals.index(ref_lookup)+1)[int(header_row):]
        read_col_values = self.active_workbook.col_values(header_vals.index(item["source"])+1)[int(header_row):]

        lookup_map = {
            l: r
            for l, r in zip(lookup_col_values, read_col_values)
        }
        # Keys are either ints or strings
        # For some reason once in a blue moon the type comes through wrong.
        # Find outliers and fix them.
        int_types = len([k for k in lookup_map.keys() if isinstance(k, int)])
        str_types = len([k for k in lookup_map.keys() if isinstance(k, str)])
        convert = None
        if int_types > len(lookup_map.keys()) / 2:
            convert = int
        elif str_types > len(lookup_map.keys()) / 2:
            convert = str
        else:
            # There is nothing in this column
            convert = lambda x:x

        for key in list(lookup_map.keys()):
            if convert is not None and not isinstance(key, convert):
                lookup_map[convert(key)] = lookup_map[key]

        data = []
        for v in (
            map_sheet
            .col_values(sheet_header_row.index(sheet_lookup)+1)
            [int(self.table_config.COLUMN_NAME_ROW):]
        ):
            data.append(lookup_map.get(convert(v), None))
        return data

    def update_data(self, map_sheet: Workbook, col_index: int, id_values: list, sections: list):
        map_sheet.update_values(self.table_config.VALUES_BEGIN_ROW-1, self.table_config.VALUES_BEGIN_ROW+len(id_values)-2, col_index, col_index + len(self.get_headers())-1, self.data)
        for workbook in self.workbooks.values():
            workbook.close()
