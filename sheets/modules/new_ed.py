import csv
import json

from sheets.modules.base import MapperSection, register
from sheets.workbook import Workbook, TableConfig

@register("NewEd")
class NewEdSection(MapperSection):

    def __init__(self, section_data: dict, id_data: str, table_config: TableConfig) -> None:
        super().__init__(section_data, id_data, table_config)
        with open(section_data["criterion"], "r") as f:
            self.criterion_data = json.load(f)
        with open(section_data["path"], "r", encoding="utf-8-sig") as csvfile:
            reader = csv.reader(csvfile)
            self.source_data = list(reader)
            self.test_name_headers = self.source_data[0]
            self.csv_headers = self.source_data[1]

    def get_headers(self):
        return [
            o["name"] for o in self.criterion_data
        ] + ["submitted", "feedback_text", "ed_mark"] + (["marked_user"] if "group_lookup" in self.section_data else [])

    def get_data(self, map_sheet: Workbook, id_values: list, sections: dict):
        lookup_col = self.csv_headers.index(self.section_data["grade_lookup"])
        mark_mapping = {
            o["name"]: self.test_name_headers.index(o["name"]) + 1
            for o in self.criterion_data
        }
        feedback_index = self.csv_headers.index("FEEDBACK COMMENT")
        submitted_index = self.csv_headers.index("SUBMITTED")

        data = {}

        for row in self.source_data[2:]:
            data[row[lookup_col]] = {}
            for map_name, map_index in mark_mapping.items():
                data[row[lookup_col]][map_name] = row[map_index]
            data[row[lookup_col]]["ed_mark"] = sum(
                float(item or '0')
                for key, item in data[row[lookup_col]].items()
            )
            data[row[lookup_col]]["feedback_text"] = row[feedback_index]
            data[row[lookup_col]]["submitted"] = row[submitted_index]


        # Group Assignments
        if self.section_data.get("group_mark_lookup", None):
            cur_header = map_sheet.row_values(self.table_config.COLUMN_NAME_ROW)
            row_vals = map_sheet.get_values(self.table_config.VALUES_BEGIN_ROW-1, self.table_config.VALUES_BEGIN_ROW+len(id_values)-2, 0, self.col_index-1)
            grade_lookup_col = cur_header.index(self.section_data["group_mark_lookup"])
            sheet_lookup_col = cur_header.index(self.section_data["sheet_lookup"])

            for row in row_vals:
                sheet = row[sheet_lookup_col]
                grade_look = row[grade_lookup_col]
                if grade_look:
                    data[sheet] = data[grade_look]

        return data

    def update_data(self, map_sheet: Workbook, col_index: int, id_values: list, sections: dict):
        cur_header = map_sheet.row_values(self.table_config.COLUMN_NAME_ROW)
        data = [
            ["" for _ in range(len(self.get_headers()))]
            for _ in range(len(
                    map_sheet
                    .col_values(cur_header.index(self.section_data["sheet_lookup"])+1)
                    [int(self.table_config.COLUMN_NAME_ROW):]
                )
            )
        ]
        if self.section_data.get("group_lookup", ""):
            emails_to_group_ids = {}
            group_ids_to_emails = {}
            group_index = cur_header.index(self.section_data["group_lookup"])
            for i, lookup in enumerate((
                map_sheet
                .col_values(cur_header.index(self.section_data["sheet_lookup"])+1)
                [int(self.table_config.COLUMN_NAME_ROW):]
            ), start=int(self.table_config.COLUMN_NAME_ROW)):
                group_val = map_sheet.get_values(i, i, group_index, group_index)[0][0]
                group_ids_to_emails[group_val] = group_ids_to_emails.get(group_val, []) + [lookup]
                emails_to_group_ids[lookup] = group_val

            # Now, copy the maximum mark between students in a group
            for email_set in group_ids_to_emails.values():
                best = -1
                best_submitted = False
                best_info = None
                for email in email_set:
                    try:
                        total = self.data[email]["ed_mark"]
                        if (
                            (not best_submitted and self.data[email]["submitted"]) or
                            total > best
                        ):
                            best_info = email
                            best = total
                            best_submitted = self.data[email]["submitted"]
                    except KeyError:
                        continue
                self.data[best_info]["marked_user"] = best_info
                for email in email_set:
                    self.data[email] = self.data[best_info]

        for i, look in enumerate(
            map_sheet
            .col_values(cur_header.index(self.section_data["sheet_lookup"])+1)
            [int(self.table_config.COLUMN_NAME_ROW):]
        ):
            for j, header in enumerate(self.get_headers()):
                try:
                    data[i][j] = self.data[look][header]
                except:
                    # No student data
                    pass

        map_sheet.update_values(self.table_config.VALUES_BEGIN_ROW-1, self.table_config.VALUES_BEGIN_ROW+len(data)-2, col_index, col_index+len(self.get_headers())-1, data)
