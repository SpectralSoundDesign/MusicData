import pandas as pd

def createExcel(playlist_data, save_directory, excel_file_name):
    df = pd.DataFrame(playlist_data)
    
    full_path = f"{save_directory}/{excel_file_name}"
    
    df.to_excel(full_path, index=False)
    
    print(f"Excel file '{excel_file_name}' created successfully.")    
