import pandas as pd
from openpyxl import load_workbook

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
    
    if month not in df.columns:
        df[month] = None
    
    # Update the DataFrame with paycheck data for the given month
    for component, value in paycheck_data.items():
        if component not in df.index:
            df.loc[component] = [None] * len(df.columns)  # Add new row with NaN values
        df.loc[component, month] = pd.to_numeric(value, errors='coerce')
    
    # Write back to Excel
    with pd.ExcelWriter(excel_file_path, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer)
        