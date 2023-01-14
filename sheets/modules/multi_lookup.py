import yaml
from sheets.modules.base import MapperSection, register
from sheets.workbook import Workbook, COLS, TableConfig
from sheets.util import eval_query

@register("MultiLookup")
class MultiLookup(MapperSection):

    DEF_LINK_OUTPUT = "data"

    def __init__(self, section_data: dict, id_data: str, table_config: TableConfig) -> None:
        super().__init__(section_data, id_data, table_config)
        self.items = section_data["items"]
        self.is_download = "link" in section_data
        if self.is_download:
            import gdown
            with open("secrets/folder_paths.yml", "r") as f:
                folders = yaml.load(f.read())
            output = section_data.get("output", self.DEF_LINK_OUTPUT)
            gdown.download_folder(url=folders[section_data["link"]], output=output)

    def get_headers(self):
        return [i["dest"] for i in self.items]

    def get_data(self, map_sheet: Workbook, id_values: list, sections: dict):
        import os
        import re
        data = [
            ["" for _ in range(len(self.items))]
            for _ in range(len(
                map_sheet
                    .col_values(1)
                    [int(self.table_config.COLUMN_NAME_ROW):]
                )
            )
        ]
        header = map_sheet.row_values(self.table_config.COLUMN_NAME_ROW)
        row_vals = map_sheet.get_values(self.table_config.VALUES_BEGIN_ROW-1, self.table_config.VALUES_BEGIN_ROW+len(id_values)-2, 0, self.col_index-1)
        form = re.compile(r"(?P<col>[A-Z]+)(?P<row>[0-9]+)")
        for idx in range(len(id_values)):
            vals = row_vals[idx]

            filepath = eval_query(self.section_data["path"], sections, header, vals, f_type=True)
            filepath = os.path.normpath(filepath)

            local_workbook = Workbook.from_xlsx(filepath)

            for j, item in enumerate(self.items):
                source = item["source"]
                if "!" in source:
                    local_workbook.set_worksheet(source.split("!")[0])
                    source = source.split("!", 1)[1]
                else:
                    local_workbook.set_worksheet(0)
                mat = form.match(source)
                col = COLS.index(mat.group("col"))
                row = int(mat.group("row"))-1
                data[idx][j] = local_workbook.get_values(row, row, col, col)[0][0]
                if data[idx][j] is None:
                    data[idx][j] = ""

            local_workbook.close()
        return data

    def update_data(self, map_sheet: Workbook, col_index: int, id_values: list, sections: dict):
        map_sheet.update_values(self.table_config.VALUES_BEGIN_ROW-1, self.table_config.VALUES_BEGIN_ROW+len(id_values)-2, col_index, col_index + len(self.get_headers())-1, self.data)
