import pandas as pd
from openpyxl import load_workbook
import os
import numpy as np

def month_str_to_period(month: str):
    return pd.Period(f"20{month[-2:]}-{month[:2]}", freq="M")

def update_paycheck_log(excel_file_path: str, month: str, paycheck_data: dict[str, ], sheet_name="main_sheet"):
    # Load existing file or create a new DataFrame
    try:
        # Load the existing workbook and the specific sheet
        workbook = load_workbook(excel_file_path)
        if sheet_name in workbook.sheetnames:
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name, index_col=0, engine="openpyxl")
        else:
            df = pd.DataFrame()  # If sheet doesn't exist, create a new DataFrame
    except:
        workbook = None
        df = pd.DataFrame()  # If file doesn't exist, create a new DataFrame
    
    month_period = month_str_to_period(month)
    if month_period not in df.columns:
        df[month_period] = None
    
    # Update the DataFrame with paycheck data for the given month
    for component, value in paycheck_data.items():
        if component not in df.index:
            df.loc[component] = [np.nan] * len(df.columns)  # Add new row with NaN values
        df.loc[component, month_period] = pd.to_numeric(value, errors='coerce')
    
    # Write back to Excel
    write_mode = "a" if os.path.exists(excel_file_path) else "w"
    with pd.ExcelWriter(excel_file_path, engine="openpyxl", mode=write_mode) as writer:
        if sheet_name in writer.book.sheetnames:
            del writer.book[sheet_name]
        df.to_excel(writer, sheet_name=sheet_name)
        