import argparse
import csv
import shutil
import os
import zipfile

from sheets.workbook import Workbook

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("input_sheet")
    parser.add_argument("input_header_row", type=int)
    parser.add_argument("grading_csv")
    parser.add_argument("submissions_path")
    parser.add_argument("source_filepath")
    parser.add_argument("final_filepath")
    parser.add_argument("-input_lookup", default="Student ID")
    parser.add_argument("-grading_lookup", default="ID number")

    args = parser.parse_args()

    wb = Workbook.from_options({
        "path": args.input_path,
        "sheet": args.input_sheet,
    })
    input_header = wb.row_values(args.input_header_row)

    with open(args.grading_csv, "r", encoding="utf-8-sig") as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    grading_header = data[0]

    ids = list(map(str, wb.col_values(input_header.index(args.input_lookup)+1)[args.input_header_row:]))

    input_map = {}
    for i, identifier in enumerate(ids):
        my_data = wb.row_values(i + args.input_header_row + 1)
        input_map[identifier] = {}
        for key, value in zip(input_header, my_data):
            input_map[identifier][key] = value

    grading_map = {}
    for i, row in enumerate(data[1:]):
        identifier = row[grading_header.index(args.grading_lookup)]
        if identifier == "":
            continue
        grading_map[identifier] = {}
        for key, value in zip(grading_header, row):
            # Some hacky replacements that need to be made to fit the usual format.
            if key == "Identifier":
                # Extract the ID number
                value = value.split(" ")[1]
            if key == "Group":
                # WHAT THE FUCK
                value = value.replace("_", " ")
            if key == "Full name":
                # Try to rearrange so of the format input[Last] + input[First]
                value = value.split(" ")
                target_string = (input_map[identifier]["Last Name"] + " " + input_map[identifier]["First Name"]).lower()
                for x in range(1, len(value)):
                    # Try swapping the first half with second half
                    new_val = " ".join(value[x:]) + " " + " ".join(value[:x])
                    if new_val.lower() == target_string:
                        value = new_val
                        break
                    elif value[x-1].lower() == input_map[identifier]["First Name"].split(" ")[0].lower():
                        # If preferred name is the first space separated word.
                        value = new_val
                        break
                else:
                    raise ValueError("Bad Name:", " ".join(value))
            grading_map[identifier][key] = value


    if os.path.exists(args.submissions_path):
        shutil.rmtree(args.submissions_path)
    os.mkdir(args.submissions_path)
    zipfiles = []
    for identifier in ids:
        if identifier not in grading_map:
            continue
        id_map = {
            "input": input_map[identifier],
            "grading": grading_map[identifier],
        }
        source_file = os.path.normpath(args.source_filepath.format(**id_map))
        final_folder = os.path.normpath(args.final_filepath.format(**id_map))
        folderpath = os.path.normpath(os.path.join(args.submissions_path, final_folder))
        print(source_file, "->", folderpath)
        os.mkdir(folderpath)
        final_filepath = os.path.join(folderpath, os.path.basename(source_file))
        shutil.copy(source_file, final_filepath)
        zipfiles.append(final_filepath)
    if os.path.exists("data/feedback.zip"):
        os.remove("data/feedback.zip")
    with zipfile.ZipFile("data/feedback.zip", mode="w") as archive:
        for filename in zipfiles:
            print(os.path.relpath(filename, args.submissions_path))
            archive.write(filename, arcname=os.path.relpath(filename, args.submissions_path))

if __name__ == "__main__":
    main()
