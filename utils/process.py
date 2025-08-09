# utils/process.py

import pandas as pd

def process_flare_data(data):
    df = pd.DataFrame(data)
    
    if df.empty:
        return pd.DataFrame()
    
    df['year'] = pd.to_datetime(df['beginTime']).dt.year
    flare_counts = df.groupby('year').size().reset_index(name='flare_count')
    
    return flare_counts
