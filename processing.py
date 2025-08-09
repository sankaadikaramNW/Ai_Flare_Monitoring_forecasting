# processing.py

import pandas as pd

def process_flare_data(data):
    """
    Process raw solar flare data into a cleaned DataFrame for display.
    Expects a list of dicts or a DataFrame.
    """
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        raise ValueError("Unsupported data type for processing")

    # Example processing: convert time columns to datetime
    for col in ['beginTime', 'peakTime', 'endTime']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # Maybe rename columns or filter needed columns
    df = df.rename(columns={
        'flrID': 'Event ID',
        'classType': 'Class',
        'sourceLocation': 'Location',
        'activeRegionNum': 'Active Region',
    })

    # Select relevant columns to show
    cols_to_show = ['Event ID', 'beginTime', 'peakTime', 'endTime', 'Class', 'Location', 'Active Region']
    existing_cols = [col for col in cols_to_show if col in df.columns]

    return df[existing_cols]
