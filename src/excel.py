import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment
import os

def month_str_to_period(month: str):
    return pd.Period(f"20{month[-2:]}-{month[:2]}", freq="M")

def open_or_create_dataframe(excel_file_path: str, sheet_name: str):
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

    return df

def column_fit_width(worksheet, column_id: str):
    component_column = worksheet[column_id]
    max_length = 0
    for cell in component_column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    worksheet.column_dimensions[column_id].width = max_length + 2 # padding

def centralize_cells(worksheet):
    for row in worksheet.iter_rows():
        for cell in row:
            # Set horizontal and vertical alignment to center
            cell.alignment = Alignment(horizontal="center", vertical="center")



def update_paycheck_log(excel_file_path: str, month: str, paycheck_data: dict[str, ], sheet_name="main_sheet"):
    df = open_or_create_dataframe(excel_file_path, sheet_name)
    
    df.columns = pd.to_datetime(df.columns).to_period("M")
    month_period = month_str_to_period(month)
    if month_period in df.columns:
        print(f"{month}: Nothing to update")
        return 
    if month_period not in df.columns:
        df[month_period] = 0.0
    
    # Update the DataFrame with paycheck data for the given month
    for component, value in paycheck_data.items():
        if component not in df.index:
            df.loc[component] = [0.0] * len(df.columns)  # Add new row with NaN values
        df.loc[component, month_period] = pd.to_numeric(value, errors='coerce')
    
    # Write back to Excel
    write_mode = "a" if os.path.exists(excel_file_path) else "w"
    with pd.ExcelWriter(excel_file_path, engine="openpyxl", mode=write_mode) as writer:
        if sheet_name in writer.book.sheetnames:
            del writer.book[sheet_name]
        df.to_excel(writer, sheet_name=sheet_name)
        # Align all cells in the sheet to the center
        worksheet = writer.sheets[sheet_name]  # Get the worksheet object
        
        centralize_cells(worksheet)
        column_fit_width(worksheet, 'A')
        