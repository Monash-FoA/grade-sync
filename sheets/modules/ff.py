from sheets.modules.base import register
from sheets.workbook import Workbook, TableConfig
from sheets.modules.lookup import SheetLookup

@register("FeedbackFruits")
class FFLookup(SheetLookup):

    NUM_STUDENTS = "#Students Rated"
    CUSTOM_LOGIC = [
        NUM_STUDENTS,
    ]

    def __init__(self, section_data: dict, id_data: str, table_config: TableConfig) -> None:
        # Apply some reasonable defaults for FF.
        section_data["sheet"] = section_data.get("sheet", "Analytics per student")
        section_data["items"] = section_data.get("items", [
            {"source": "Overall grade", "dest": "Peer Evaluation Grade", "sheet": "Analytics per student"},
            {"source": self.NUM_STUDENTS, "dest": self.NUM_STUDENTS, "sheet": "Ratings"},
        ])
        super().__init__(section_data, id_data, table_config)

    def get_col_data(self, item_index, item, map_sheet):
        if item["source"] not in self.CUSTOM_LOGIC:
            return super().get_col_data(item_index, item, map_sheet)
        if item["source"] == self.NUM_STUDENTS:
            # Count the number of rows for which you appear in "The rated work of student name"
            map_data = {}
            student_details = self.workbooks["Analytics per student"]
            self.prepare_active_workbook(item)

            active_workbook_header_row = self.active_workbook.row_values(1)
            details_workbook_header_row = student_details.row_values(1)
            sheet_header_row = map_sheet.row_values(self.table_config.COLUMN_NAME_ROW)
            sheet_lookup = item.get("sheet_lookup", self.sheet_lookup)
            ref_lookup = item.get("ref_lookup", self.ref_lookup)
            print(active_workbook_header_row)
            for marking_student, rated_student, mark in zip(
                self.active_workbook
                    .col_values(active_workbook_header_row.index("Student name")+1)
                    [1:],
                self.active_workbook
                    .col_values(active_workbook_header_row.index("The rated work of student name")+1)
                    [1:],
                self.active_workbook
                    .col_values(active_workbook_header_row.index("Contributing to the Team's work")+1)
                    [1:],
            ):
                if rated_student not in map_data:
                    map_data[rated_student] = 0
                if mark is not None and marking_student != rated_student:
                    map_data[rated_student] += 1

            final_data = {}
            for sname, lookup_field in zip(
                student_details
                    .col_values(details_workbook_header_row.index("Student name")+1)
                    [1:],
                student_details
                    .col_values(details_workbook_header_row.index(ref_lookup)+1)
                    [1:]
            ):
                final_data[lookup_field] = map_data.get(sname, 0)

            return [
                final_data.get(lookup_field, 0)
                for lookup_field in map_sheet.col_values(sheet_header_row.index(sheet_lookup)+1)
                [int(self.table_config.COLUMN_NAME_ROW):]
            ]
