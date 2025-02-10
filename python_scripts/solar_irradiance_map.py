import os
import pandas as pd
import folium
import numpy as np
import json
import plotly_express as px
from folium.plugins import HeatMapWithTime
from data_scraper_nasa import fetch_solar_data, save_data_to_json
from data_cleaner import load_data_from_folder_in_json, clean_solar_data_map, save_cleaned_data

def downloading_data(latitude, longitude, start_date, end_date,area_lat, area_long,interval):

    # Generate latitudes and longitudes with the given interval
    latitudes = np.arange(latitude - area_lat, latitude + area_lat + interval, interval)
    longitudes = np.arange(longitude - area_long, longitude + area_long + interval, interval)

    print(f"Fetching solar data from {start_date} to {end_date} for multiple locations...")

    # Loop through all latitude and longitude pairs
    for lat in latitudes:
        for lon in longitudes:
            print(f"\nFetching data for latitude: {lat:.2f}, longitude: {lon:.2f}...")
            try:
                # Fetch solar irradiance data using NASA POWER API
                solar_data = fetch_solar_data(lat, lon, start_date, end_date)

                # Save the raw data
                save_data_to_json(solar_data, lat, lon, start_date, end_date)
                print(f"Data saved for ({lat:.2f}, {lon:.2f})")

                # Load and clean the raw data
                raw_data = load_data_from_folder_in_json(lat, lon, start_date, end_date)
                cleaned_data = clean_solar_data_map(raw_data)

                # Save the cleaned data
                save_cleaned_data(cleaned_data, lat, lon, start_date, end_date)
                print(f"Cleaned data saved for ({lat:.2f}, {lon:.2f})")

            except Exception as e:
                print(f"Error fetching data for ({lat:.2f}, {lon:.2f}): {str(e)}")

    print("\nAll locations processed.")


def load_cleaned_solar_data(start_date, end_date):
    """
    Loads cleaned solar irradiance data from all available JSON files in the data folder.
    :param start_date: Start date of data (YYYYMMDD)
    :param end_date: End date of data (YYYYMMDD)
    :return: Combined DataFrame with latitude, longitude, DateTime, and Solar_Irradiance
    """
    data_folder = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'data')
    all_data = []

    # Loop through all cleaned solar data files in the folder
    for file in os.listdir(data_folder):
        if file.startswith("cleaned_solar_data") and file.endswith(f"_{start_date}_to_{end_date}.json"):
            file_path = os.path.join(data_folder, file)
            parts = file.split("_")
            lat = float(parts[4])  # Corrected index for latitude
            lon = float(parts[6])  # Corrected index for longitude

            # Load data
            with open(file_path, 'r') as f:
                raw_data = json.load(f)

            data = pd.DataFrame(raw_data)
            # Append latitude and longitude to the DataFrame
            data['Latitude'] = lat
            data['Longitude'] = lon
            all_data.append(data)

    if not all_data:
        raise FileNotFoundError(f"No cleaned data found for the given date range: {start_date} to {end_date}")

    # Combine all location data
    combined_df = pd.concat(all_data, ignore_index=True)

    # Convert DateTime to proper format
    combined_df['DateTime'] = pd.to_datetime(combined_df['DateTime'])
    print(combined_df.head())

    return combined_df

def generate_heatmap_with_time(data):
    """
    Generates a heatmap with a time slider.
    :param data: DataFrame containing Latitude, Longitude, DateTime, and Solar_Irradiance
    :param start_date: Start date (YYYYMMDD)
    :param end_date: End date (YYYYMMDD)
    :param interval: The interval step size used for grid creation.
    """

    data["DateTime"] = data["DateTime"].astype(str)
    fig = px.density_mapbox(
        data,
        lat= "Latitude",
        lon = "Longitude",
        z = "Solar_Irradiance",
        radius = 20,
        center = dict(lat=data.Latitude.mean(), lon=data.Longitude.mean()),
        zoom =4,
        mapbox_style = "open-street-map",
        height = 900,
        animation_frame="DateTime",
        color_continuous_scale="plasma",  # Use a visually appealing gradient (Options: viridis, plasma, inferno, etc.)
        range_color=[0, 100]  # Fix the color range from 0 to 100
    )

    heatmap_filename = f"solar_irradiance_heatmap_{start_date}_to_{end_date}.html"
    fig.write_html(heatmap_filename)

    print(f"✅ Heatmap saved as {heatmap_filename}. Open it in a browser to view.")


if __name__ == "__main__":
    try:
        # Step 1: User Inputs for Scraping Data
        """
        latitude = float(input("Enter latitude: "))
        longitude = float(input("Enter longitude: "))
        start_date = input("Enter start date (YYYYMMDD): ")
        end_date = input("Enter end date (YYYYMMDD): ")
        area_lat = float(input("Enter additional latitude (degree): "))
        area_long = float(input("Enter additional longitude (degree): "))
        interval = float(input("Enter interval step size for latitude/longitude (e.g., 0.1, 0.5): "))
        """
        #testing for central london
        latitude = float(51.54501)
        longitude = float(-0.00564)
        start_date = ("20230101")
        end_date = ("20230103")
        area_lat = float(0.0)
        area_long = float(0.0)
        interval = float(0.01)

        downloading_data(latitude, longitude, start_date, end_date, area_lat, area_long, interval)

        # Step 2: Load Cleaned Data
        solar_data = load_cleaned_solar_data(start_date, end_date)

        # Step 3: Generate Heatmap
        generate_heatmap_with_time(solar_data)

    except Exception as e:
        print(f"An error occurred: {str(e)}")