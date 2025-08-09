# pages/view_previous_events.py
import streamlit as st
from db import save_flare_data_to_db, get_flare_data_from_db
from nasa_api import fetch_solar_flares
from processing import process_flare_data

def view_previous_events():
    st.subheader("🌞 View Previous Solar Flare Events")

    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Fetch from NASA API"):
        api_data = fetch_solar_flares(start_date, end_date)

        if api_data is not None and not api_data.empty:
            # ✅ Always convert DataFrame to list of dicts
            if hasattr(api_data, "to_dict"):
                api_data = api_data.to_dict(orient="records")

            save_flare_data_to_db(api_data)  # Always a list of dicts now
            flare_df = process_flare_data(api_data)
            st.success("✅ Data fetched from NASA API and stored in the database.")
            st.dataframe(flare_df)
        else:
            st.warning("⚠️ No solar flare data found for this period.")

    if st.button("View from Database"):
        db_data = get_flare_data_from_db(start_date, end_date)

        if not db_data.empty:
            st.dataframe(db_data)
        else:
            st.warning("⚠️ No records found in the database.")
