import pandas as pd

# Load the .xlsx file
file_path = 'teachers.xlsx'
dataframe = pd.read_excel(file_path)

# Save it as a .csv file
csv_file_path = 'teachers.csv'
dataframe.to_csv(csv_file_path, index=False)
