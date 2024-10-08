import os
import json
import pandas as pd
import numpy as np

def load_data_from_folder_in_json(start_date, end_date):
    """
        Loads the raw solar data from a JSON file based on the start and end date.
        :param start_date: The start date of the data (format 'YYYYMMDD').
        :param end_date: The end date of the data (format 'YYYYMMDD').
        :return: The raw solar data as a dictionary.
    """
    data_folder = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'data')
    filename = f"solar_data_{start_date}_to_{end_date}.json"
    file_path = os.path.join(data_folder, filename)
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data

def clean_solar_data(data):
    """
    Cleans the solar irradiance and temperature data, converting invalid solar irradiance (-999) to NaN
    and performing basic checks.
    :param data: Dictionary containing raw solar data
    :return: Cleaned pandas DataFrame.
    """
    # Convert the JSON data to pandas DataFrames
    # converts dictionary items into a pandas DataFrame with two columns
    df_irradiance = pd.DataFrame(list(data['ALLSKY_SFC_SW_DWN'].items()), columns=['DateTime', 'Solar_Irradiance'])
    df_temperature = pd.DataFrame(list(data['T2M'].items()), columns=['DateTime', 'Temperature'])
    df_solar_zenith_angle = pd.DataFrame(list(data['SZA'].items()), columns=['DateTime', 'Solar_zenith_angle'])

    # Merge the three DataFrames on the DateTime column
    df = pd.merge(df_irradiance, df_temperature, on='DateTime')
    df = pd.merge(df, df_solar_zenith_angle, on='DateTime')
    # Convert DateTime to a proper datetime object. To note that the data is hourly. eg 2024052401
    df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y%m%d%H')

    # Replace invalid data (-999) with NaN to recognise it as missing data and check if data is numeric
    # NASA uses -999 for dates which have not been uploaded

    for column in ['Solar_Irradiance', 'Temperature', 'Solar_zenith_angle']:
        df[column] = df[column].replace(-999, np.nan)
        if not pd.api.types.is_numeric_dtype(df[column]):
            try:
                df[column] = pd.to_numeric(df[column], errors='coerce')  # Convert invalid entries to NaN
            except Exception as e:
                raise ValueError(f"Error: Non-numeric data found in {column}: {str(e)}")

    return df

def check_data_availability(df):
    """
    Checks the cleaned solar data for missing values in the Solar Irradiance column and temperature column and
    identifies when data becomes unavailable.
    :param df: Cleaned pandas DataFrame.
    :return: A message indicating the first date when data became unavailable.
    """
    # Check for rows where Solar Irradiance is NaN
    missing_data_solar = df[df['Solar_Irradiance'].isna()]
    missing_data_temperature = df[df['Temperature'].isna()]

    if not missing_data_solar.empty or not missing_data_temperature.empty:
        # Get the first occurrence of missing data
        all_missing_date = pd.concat([missing_data_solar['DateTime'],missing_data_temperature['DateTime']])
        first_missing_date = all_missing_date.min()
        print(f"Warning: Some data is unavailable starting from {first_missing_date}")
    else:
        print("No missing data found was found.")

    return df

def save_cleaned_data(df, start_date, end_date):
    """
    Saves the cleaned solar data to a JSON file in the data directory with start and end date in the filename.
    :param df: The cleaned pandas DataFrame containing solar data.
    :param start_date: The start date of the data (format 'YYYYMMDD').
    :param end_date: The end date of the data (format 'YYYYMMDD').
    """
    data_folder = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),'data')
    filename = f"cleaned_solar_data_{start_date}_to_{end_date}.json"
    file_path = os.path.join(data_folder, filename)

    with open(file_path, 'w') as file:
        df.to_json(file, orient='records', date_format='iso')
    print(f"Data is saved to {file_path}")

if __name__ == "__main__":
    try:
        start_date , end_date = '20230101', '20240101'
        raw_data = load_data_from_folder_in_json(start_date, end_date)
        cleaned_data = clean_solar_data(raw_data)
        first_missing_date = check_data_availability(cleaned_data)
        save_cleaned_data(cleaned_data, start_date, end_date)
    except Exception as e:
        print(f"An error occurred: {str(e)}")