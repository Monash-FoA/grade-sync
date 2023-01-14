from sheets.workbook import Workbook, TableConfig
from sheets.modules import SECTIONS


def create_sheet(map_info, config=TableConfig()):
    sheet = Workbook.from_options(map_info)
    sheet.clear()

    # This variable keeps track of what column we are currently writing to.
    col_index = 0
    sections = {}

    # Start by asserting that the first key is an ID row.
    section_keys = list(map_info["sections"].keys())
    first_key = section_keys[0]
    assert map_info["sections"][first_key]["type"] == "ID"
    id_data = map_info["sections"][first_key]

    sections[first_key] = SECTIONS[map_info["sections"][first_key]["type"]](map_info["sections"][first_key], None, config)
    col_index = sections[first_key].action(sheet, col_index, None, sections)
    id_values = sections[first_key].data

    try:
        for section_name in section_keys[1:]:
            section_data = map_info["sections"][section_name]
            sections[section_name] = SECTIONS[section_data["type"]](section_data, id_data, config)
            col_index = sections[section_name].action(sheet, col_index, id_values, sections)
    except Exception as e:
        sheet.close()
        raise e

    sheet.close()
