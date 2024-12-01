import fitz
from read_rects import read_rects
import os

OUTPUT_FILE = "output/out.txt"
file_name = "paychecks/2024/תלוש שכר 11.24.pdf"

doc = fitz.open(file_name)
page = doc[0]

details_rects = [
    [234.1651611328125, 184.30874633789062, 418.9469909667969, 391.8227844238281], # right rect
    [18.012704849243164, 184.30874633789062, 202.95132446289062, 391.2220916748047] # left rect
]
payment_rect = [234.1651611328125, 416.1496276855469, 418.9443054199219, 600.3687744140625]
clean_rect = [18.012704849243164, 416.1496276855469, 202.794189453125, 600.3687744140625]

payment_diff_rect = [234.1651611328125, 646.8284912109375, 418.9443359375, 800.889404296875]
clean_diff_rect = [18.012704849243164, 648.5716552734375, 203.37294006347656, 800.889404296875]

directory = os.path.dirname(OUTPUT_FILE)
if directory and not os.path.exists(directory):
    os.makedirs(directory)

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    for line in read_rects(page, *details_rects):
        out.write(" ".join(line) + "\n")
    out.write('------------------------------------------------\n')
    for line in read_rects(page, payment_rect):
        out.write(f"{line[0]} - {line[-1]}" + "\n")
    out.write('------------------------------------------------\n')
    for line in read_rects(page, clean_rect):
        out.write(f"{line[0]} - {line[-1]}" + "\n")
    out.write('------------------------------------------------\n')
    for line in read_rects(page, payment_diff_rect):
        out.write(f"{line[0]} - {line[-1]}" + "\n")
    out.write('------------------------------------------------\n')
    for line in read_rects(page, clean_diff_rect):
        out.write(f"{line[0]} - {line[-1]}" + "\n")