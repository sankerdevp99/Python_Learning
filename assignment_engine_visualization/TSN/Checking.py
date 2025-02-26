import pandas as pd
import os


if os.path.exists(os.path.join("Common_Files", 'distance_matrix.xlsx')):
    distance_matrix = pd.read_excel(os.path.join("Common_Files", 'distance_matrix.xlsx'))
else:
    print("File not found.")
