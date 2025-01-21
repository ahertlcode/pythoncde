import os
import pandas as pd

def count_rows_in_directory(directory_path):
    total_rows = 0
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith((".xlsx", ".xls")):  # Check for Excel files
                file_path = os.path.join(root, file)
                try:
                    excel_file = pd.ExcelFile(file_path)  # Load the Excel file
                    for sheet in excel_file.sheet_names:
                        sheet_data = excel_file.parse(sheet)  # Read the sheet
                        total_rows += sheet_data.shape[0]  # Add the row count
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    return total_rows

# Replace with the path to your directory
directory_path = "EXAM_SCORE"
total_rows = count_rows_in_directory(directory_path)
print(f"Total number of rows in all sheets: {total_rows}")
