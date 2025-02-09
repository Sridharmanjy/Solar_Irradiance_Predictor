import os
import pandas as pd
import folium
import geopandas as gpd
from shapely.geometry import Point
from data_scraper_nasa import fetch_solar_data, save_data_to_json
from data_cleaner import load_data_from_folder_in_json, clean_solar_data, save_cleaned_data

if __name__ == "__main__":
    # Step 1: User Inputs for Scraping Data
    latitude = float(input("Enter latitude: "))
    longitude = float(input("Enter longitude: "))
    start_date = input("Enter start date (YYYYMMDD): ")
    end_date = input("Enter end date (YYYYMMDD): ")
    area_lat = float(input("Enter additional latitude (degree): "))
    area_long = float(input("Enter additional longitude (degree): "))
    interval = float(input("Enter interval step size for latitude/longitude (e.g., 0.1, 0.5): "))

    try:
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

                except Exception as e:
                    print(f"Error fetching data for ({lat:.2f}, {lon:.2f}): {str(e)}")

        print("\nAll locations processed.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")