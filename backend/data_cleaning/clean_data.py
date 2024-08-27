import os
import pandas as pd

def clean_data(input_file: str, output_file: str):
    # Use absolute paths for input and output files
    input_file = os.path.abspath(input_file)
    output_file = os.path.abspath(output_file)
    
    # Check current working directory
    print("Current working directory:", os.getcwd())
    print("Looking for:", input_file)
    
    # Load the CSV file
    df = pd.read_csv(input_file)

    # Remove unnecessary columns
    unnecessary_columns = ['X', 'Y', 'Official_French_Waterbody_Name', 'Waterbody_Location_Identifier', 
                           'ObjectId', 'Developmental_Stage', 'MNRF_District', 'Stocking_Year',
                           'Unoffcial_Waterbody_Name', 'Geographic_Township']
    df_cleaned = df.drop(unnecessary_columns, axis=1)

    # Handle missing Official_Waterbody_Name
    missing_name_mask = df_cleaned['Official_Waterbody_Name'].isnull() | (df_cleaned['Official_Waterbody_Name'].str.strip() == '')
    df_cleaned.loc[missing_name_mask, 'Official_Waterbody_Name'] = (
        'Unnamed Waterbody ' + df_cleaned.loc[missing_name_mask].apply(
            lambda row: f"({row['Latitude']}, {row['Longitude']})", axis=1
        )
    )

    # Save the cleaned data to the output file
    df_cleaned.to_csv(output_file, index=False)
    return df_cleaned

if __name__ == '__main__':
    input_file = r'C:\Users\danie\OneDrive\Desktop\Ontario_Fish_Stocking_Finder\data\Fish_Stocking_Data_for_Recreational_Purposes.csv'
    output_file = r'C:\Users\danie\OneDrive\Desktop\Ontario_Fish_Stocking_Finder\data\cleaned_data.csv'

    cleaned_df = clean_data(input_file, output_file)
    print("Data cleaned and saved to", output_file)
