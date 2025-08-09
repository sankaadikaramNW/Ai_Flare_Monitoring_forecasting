
import requests
import pandas as pd

def fetch_solar_flares(start_date, end_date):
    url = f"https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/FLR?startDate={start_date}&endDate={end_date}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        return pd.DataFrame()