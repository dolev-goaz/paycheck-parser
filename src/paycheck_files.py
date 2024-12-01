import os
import re

def get_paychecks_paths(base_directory: str):
    file_paths: list[str] = []
    for year_directory in os.listdir(base_directory):
        year_directory_path = os.path.join(base_directory, year_directory)
        if not os.path.isdir(year_directory_path) and year_directory.isdigit(): continue
        file_paths.extend([os.path.join(year_directory_path, filename) for filename in os.listdir(year_directory_path)])
    
    return file_paths
    
def get_paychecks(base_directory: str):
    file_paths = get_paychecks_paths(base_directory)
    pattern = r'תלוש שכר (\d{2}\.\d{2})\.pdf'
    
    out: dict[str, str] = {}
    
    for path in file_paths:
        m = re.search(pattern, path)
        out[m.group(1)] = path
    
    return out
