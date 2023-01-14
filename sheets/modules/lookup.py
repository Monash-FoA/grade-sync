from sheets.modules.base import MapperSection, register
from sheets.workbook import Workbook, TableConfig

@register("Lookup")
class SheetLookup(MapperSection):

    def __init__(self, section_data: dict, id_data: str, table_config: TableConfig) -> None:
        super().__init__(section_data, id_data, table_config)
        self.workbook = Workbook.from_options(section_data)
        self.header_row = section_data["header_row"]
        self.header_vals = self.workbook.row_values(self.header_row)
        self.sheet_lookup = section_data.get("sheet_lookup", id_data["dest"])
        self.ref_lookup = section_data.get("sheet_lookup", id_data["source"])
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
            sheet_lookup = item.get("sheet_lookup", self.sheet_lookup)
            ref_lookup = item.get("ref_lookup", self.ref_lookup)
            source_col = self.header_vals.index(item["source"])
            sheet_lookup_col = [
                (v, i+1)
                for i, v in
                enumerate(
                    map_sheet
                        .col_values(sheet_header_row.index(sheet_lookup)+1)
                        [int(self.table_config.COLUMN_NAME_ROW):]
                )
            ]
            sheet_lookup_col.sort()

            ref_lookup_col = [
                (v, i+1, y)
                for i, (v, y) in
                enumerate(
                    # Select all column values from the reference col in sheet.
                    zip(
                        self.workbook
                            .col_values(self.header_vals.index(ref_lookup)+1)
                            [int(self.header_row):],
                        self.workbook
                            .col_values(source_col+1)
                            [int(self.header_row):]
                    )
                )
            ]
            ref_lookup_col.sort()

            # Now that these are sorted by value, we can efficiently match them up.
            cur_ref_lookup = 0
            for v, i in sheet_lookup_col:
                while cur_ref_lookup < len(ref_lookup_col) and ref_lookup_col[cur_ref_lookup][0] < v:
                    cur_ref_lookup += 1
                if cur_ref_lookup >= len(ref_lookup_col):
                    break
                if ref_lookup_col[cur_ref_lookup][0] > v:
                    # No matching entry.
                    continue
                # We found a match!
                # Read from source sheet.
                data[i-1][y] = ref_lookup_col[cur_ref_lookup][2]
        return data

    def update_data(self, map_sheet: Workbook, col_index: int, id_values: list, sections: list):
        map_sheet.update_values(self.table_config.VALUES_BEGIN_ROW-1, self.table_config.VALUES_BEGIN_ROW+len(id_values)-2, col_index, col_index + len(self.get_headers())-1, self.data)
