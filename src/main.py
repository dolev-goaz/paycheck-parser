import fitz
from read_rects import read_rects
from excel import update_paycheck_log
from excel_rect import generate_rects
import os
from paycheck_files import get_paychecks

OUTPUT_FILE_PATH = "output/out.xlsx"
BASE_DIRECTORY = "paychecks"

directory = os.path.dirname(OUTPUT_FILE_PATH)
if directory and not os.path.exists(directory):
    os.makedirs(directory)

# remove previous file if exists
if os.path.exists(OUTPUT_FILE_PATH):
    os.remove(OUTPUT_FILE_PATH)

files = get_paychecks(BASE_DIRECTORY)

paycheck_rects = generate_rects()
for rect in paycheck_rects:    
    for month, path in files.items():
        doc = fitz.open(path)
        page = doc[0]
        d = {f'{rect.header} - {line[0]}': line[-1] for line in read_rects(page, rect.rect)}
        update_paycheck_log(OUTPUT_FILE_PATH, month, d)