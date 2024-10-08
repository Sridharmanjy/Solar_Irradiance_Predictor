import requests
import json
import os

def fetch_solar_data(latitude, longitude, start_date, end_date):
    """
    Fetch solar irradiance (kW-hr/m^2/day), Solar Zenith Angle and temperature at 2m (C) data from NASA POWER API
    https://power.larc.nasa.gov/#resources
    :param community : Agroclimatology (ag) /Sustainable Buildings(sb) / Renewable Energy (re)
    :param latitude: Latitude of the location
    :param longitude: Longitude of the location
    :param start_date: Start date for data in 'YYYYMMDD' format
    :param end_date: End date for data in 'YYYYMMDD' format
    :return: Dictionary containing solar data
    """
    base_url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
    params = {
        'parameters': 'ALLSKY_SFC_SW_DWN,T2M,SZA',
        'community': 'RE',
        'longitude': longitude,
        'latitude': latitude,
        'start': start_date,
        'end': end_date,
        'format': 'JSON'
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200: # 200 = success , https://power.larc.nasa.gov/docs/services/api/
        data = response.json()
        return data['properties']['parameter']
    else:
        raise Exception(f"Error fetching data: {response.status_code}")


def save_data_to_json(data, start_date, end_date):
    data_folder = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),'data')
    os.makedirs(data_folder, exist_ok=True)
    filename = f"solar_data_{start_date}_to_{end_date}.json"
    file_path = os.path.join(data_folder, filename)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data is saved to {file_path}")

# to test script when running it directly, location : london, Period : year 2023
if __name__ == "__main__":
    try:
        latitude, longitude = 51.54501, -0.00564
        start_date , end_date = '20230101', '20240101'
        solar_data = fetch_solar_data(latitude, longitude, start_date, end_date)
        save_data_to_json(solar_data, start_date, end_date)
    except Exception as e:
        print(f"An error occurred: {str(e)}")