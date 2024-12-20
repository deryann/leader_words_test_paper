import json
import random
import datetime
from docx import Document
from docx.shared import Inches
import os
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=str, required=True ,help="Please enter a input json in cfg folder"
    )
    args = parser.parse_args()
    _main(args.input)


def _main(read_from_filename="1A-P12.json"):

    if read_from_filename.endswith(".json"):
        read_from_filename = read_from_filename
    else:
        read_from_filename = read_from_filename + ".json"

    base_filename = read_from_filename.split(".")[0]

    file_path = os.path.join(os.getcwd(), "cfg", read_from_filename)
    with open(file_path, "r", encoding="utf8") as f:
        data = json.load(f)
    lst_explain = data.get("explain", [])
    lst_statement = data["statement"]

    # 將 lst_explain 與 lst_statement 的打亂

    random.seed(datetime.datetime.now().timestamp())

    random.shuffle(lst_explain)
    random.shuffle(lst_statement)
    print(lst_explain)
    print(lst_statement)

    ans_doc = Document()
    document = Document()

    headings = ["1st", "2nd"]
    # document.add_heading('TEST', 0)
    heading_count = 0
    if len(lst_explain) > 0:
        document.add_heading(headings[heading_count], 1)
        ans_doc.add_heading(headings[heading_count], 1)
        heading_count += 1
        i = 0
        for e, w in lst_explain:
            i += 1
            document.add_paragraph(f"{i} ____________________: {e}")
        i = 0
        for e, w in lst_explain:
            i+=1
            ans_doc.add_paragraph(f"{i} {w} : {e}")

    if len(lst_statement) > 0:
        document.add_heading(headings[heading_count], 1)
        ans_doc.add_heading(headings[heading_count], 1)
        heading_count += 1
        i = 0
        for s, w in lst_statement:
            i += 1
            document.add_paragraph(f'{i} {s.replace(w, "______________________")}')
        i = 0
        for s, w in lst_statement:
            i += 1
            ans_doc.add_paragraph(f"{i} {w} : {s}")

    def change_font_size(doc, font_size):
        # Change the font size of all paragraphs in the document
        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(font_size)
                font_name = "Comic Sans MS"
                run.font.name = font_name
        return doc

    change_font_size(document, 12)

    # Set document margins to 2 cm
    sections = document.sections
    for section in sections:
        section.top_margin = Inches(1 / 2.54)
        section.bottom_margin = Inches(1 / 2.54)
        section.left_margin = Inches(2 / 2.54)
        section.right_margin = Inches(2 / 2.54)

    k = 0

    # 將 doc
    while True:
        filename = f"{base_filename}_test-{k}.docx"
        ans_filename = f"{base_filename}_test-{k}-ans.docx"
        filepath = os.path.join("output", filename)
        ans_filepath = os.path.join("output", ans_filename)

        if not os.path.exists(filepath):
            break
        k += 1
    # 將頁首加上 hello world
    header = document.sections[0].header
    header.paragraphs[0].text = filename

    header = ans_doc.sections[0].header
    header.paragraphs[0].text = ans_filename

    ans_doc.save(ans_filepath)
    document.save(filepath)
    os.startfile(filepath, "print")


if __name__ == "__main__":
    main()
