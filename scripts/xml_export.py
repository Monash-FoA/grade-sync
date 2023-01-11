import argparse
import xml.etree.ElementTree as ET
import sys

from sheets.workbook import Workbook

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("input_sheet")
    parser.add_argument("assignment_id")
    parser.add_argument("output_path")
    parser.add_argument("-id", default="Student ID")
    parser.add_argument("-mark", default="Total Mark")
    parser.add_argument("-feedback", default="Feedback")

    args = parser.parse_args(sys.argv[1:])

    wb = Workbook.from_options({
        "path": args.input_path,
        "sheet": args.input_sheet,
    })
    headers = wb.row_values(3)
    student_ids = wb.col_values(headers.index(args.id)+1)[3:]
    marks = wb.col_values(headers.index(args.mark)+1)[3:]
    feedback = wb.col_values(headers.index(args.feedback)+1)[3:]

    results = ET.Element("results")

    for sid, m, f in zip(student_ids, marks, feedback):
        r = ET.SubElement(results, "result")
        a = ET.SubElement(r, "assignment")
        a.text = args.assignment_id
        s = ET.SubElement(r, "student")
        s.text = str(sid)
        p = ET.SubElement(r, "score")
        p.text = str(round(float(m or 0), 2))
        feed = ET.SubElement(r, "feedback")
        feed.text = f

    with open(args.output_path, "wb") as f:
        f.write(ET.tostring(results))

if __name__ == "__main__":
    main()
