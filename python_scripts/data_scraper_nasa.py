import requests
import json

def fetch_solar_data(latitude, longitude, start_date, end_date):
    """
    Fetch solar irradiance (kW-hr/m^2/day) and temperature at 2m (C) data from NASA POWER API
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
        'parameters': 'ALLSKY_SFC_SW_DWN,T2M',
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


# to test script when running it directly, location : london, Period : 30days in june
if __name__ == "__main__":
    try:
        solar_data = fetch_solar_data(51.54501, -0.00564, '20240601', '20240630')
        print(json.dumps(solar_data, indent=3))
    except Exception as e:
        print(str(e))