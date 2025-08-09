# nasa_api.py
import requests
import pandas as pd

NASA_API_KEY = "kmAjLw0H7060eOqaT4IC3Yss41XQgsuo1zOaegJT"  # replace with your key from https://api.nasa.gov/

def fetch_solar_flares(start_date, end_date):
    """
    Fetch solar flare data from NASA's DONKI API.
    Returns a pandas DataFrame.
    """
    url = "https://api.nasa.gov/DONKI/FLR"
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "api_key": NASA_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data)
