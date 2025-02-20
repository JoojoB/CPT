import pandas as pd

def calculate_cumulative_depth(df, total_depth=8):

   # Groups by soil behavior type (SBTn) and calculates the cumulative depth occupied by each type.
    df_sorted = df.sort_values(by='Depth (m)')
    df_sorted['depth_interval'] = df_sorted['Depth (m)'].diff().fillna(df_sorted['Depth (m)'])
    
    cumulative_depth = df_sorted.groupby('SBTn')['depth_interval'].sum().reset_index()
    cumulative_depth.columns = ['SBTn', 'Cumulative Depth (m)']
    
    # Add percentage contribution
    cumulative_depth['Percentage (%)'] = (cumulative_depth['Cumulative Depth (m)'] / total_depth) * 100
    
    return cumulative_depth

def process_multiple_files(file_paths):
   #Processes multiple CSV files, ensuring proper formatting.
    results = {}
    for file_path in file_paths:
        try:
            # Read CSV, skipping unnecessary rows and setting correct headers
            df = pd.read_csv(file_path, skiprows=1, usecols=[1, 2, 3, 4])
            df.columns = ['Depth (m)', 'qc (MPa)', 'fs (kPa)', 'SBTn']


            
            # Ensure depth column is numeric
            df['Depth (m)'] = pd.to_numeric(df['Depth (m)'], errors='coerce')
            
            # Drop any rows where Depth is NaN
            df = df.dropna(subset=['Depth (m)'])

            # Compute cumulative depth
            cumulative_depth_df = calculate_cumulative_depth(df)
            results[file_path] = cumulative_depth_df
            
            print(f"Results for {file_path}:")
            print(cumulative_depth_df)
            print("-" * 40)
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return results

# List of file paths
file_paths = [
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C1_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C2_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C3_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C4_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C5_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C6_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C7_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C8_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C9_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C10_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C11_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C12_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C13_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C14_Data.csv",
    "C:/Users/Kwadwo Addo-Brako/Desktop/CPT/C15_Data.csv"
]

# Run the script
process_multiple_files(file_paths)
