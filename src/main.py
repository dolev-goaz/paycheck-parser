import fitz
from read_rects import read_rects
from excel import update_paycheck_log, insert_header, mark_color_changes
from excel_rect import generate_rects, ExcelRect
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

# from rect type to month, from month to records
excel_data: dict[str, dict[str, dict[str, str]]] = {
    rect.header: {} for rect in paycheck_rects
}

# preload all excel data
for month, path in files.items():
    doc = fitz.open(path)
    page = doc[0]
            
    for rect in paycheck_rects:
        excel_data[rect.header][month] = {line[0]: line[-1] for line in read_rects(page, rect.rect)}
        
def get_components(rect: ExcelRect):
    items = excel_data[rect.header]
    item_set = set()
    for values in items.values():
        item_set.update(values.keys())
    return item_set

# initialize non-existing fields
for rect in paycheck_rects:
    components = get_components(rect)
    for items in excel_data[rect.header].values():
        for element in components:
            if element not in items:
                items[element] = 0 # default value
        
for header, months in excel_data.items():
    for month, paycheck_data in months.items():
        data_mapped = {f"{header} - {key}": value for key, value in paycheck_data.items()}
        update_paycheck_log(OUTPUT_FILE_PATH, month, data_mapped)

# add headers
offset = 1 # ignore month headers
running_component_count_sum = offset + 1 # index starts from 1
for rect in paycheck_rects:
    component_count = len(get_components(rect))
    mark_color_changes(OUTPUT_FILE_PATH, running_component_count_sum,\
        running_component_count_sum + component_count,\
        prefer_increasing=rect.increase)
    insert_header(OUTPUT_FILE_PATH, rect.header, running_component_count_sum)
    running_component_count_sum += component_count + 1 # include the header row