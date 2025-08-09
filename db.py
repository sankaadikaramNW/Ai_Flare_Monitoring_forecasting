import json
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Database config
DB_USER = "postgres"
DB_PASSWORD = "123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "solar_flare_db"

# Create SQLAlchemy engine
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def get_flare_data_from_db(start_date, end_date):
    """Fetch solar flare events between start_date and end_date from DB."""
    query = text("""
        SELECT * FROM solar_flare_events
        WHERE begin_time >= :start_date AND end_time <= :end_date
        ORDER BY begin_time ASC
    """)
    try:
        df = pd.read_sql_query(query, con=engine, params={"start_date": start_date, "end_date": end_date})
        return df
    except SQLAlchemyError as e:
        print("Error fetching data:", e)
        return pd.DataFrame()

def save_flare_data_to_db(data):
    """Save a list of solar flare event dicts into the database."""
    insert_query = text("""
        INSERT INTO solar_flare_events (
            event_id, begin_time, peak_time, end_time,
            class_type, source_location, active_region_num
        ) VALUES (
            :event_id, :begin_time, :peak_time, :end_time,
            :class_type, :source_location, :active_region_num
        )
        ON CONFLICT (event_id) DO NOTHING
    """)

    def ensure_dict(event):
        """Ensure event is a dictionary, parse JSON strings if needed."""
        if isinstance(event, dict):
            return event
        if isinstance(event, str):
            try:
                return json.loads(event)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid event JSON string: {event}")
        raise TypeError(f"Unsupported event type: {type(event)}")

    with engine.connect() as conn:
        for event in data:
            try:
                event = ensure_dict(event)  # ✅ Ensure it's always a dict

                params = {
                    "event_id": event.get("flrID"),
                    "begin_time": event.get("beginTime"),
                    "peak_time": event.get("peakTime"),
                    "end_time": event.get("endTime"),
                    "class_type": event.get("classType"),
                    "source_location": event.get("sourceLocation"),
                    "active_region_num": event.get("activeRegionNum"),
                }

                conn.execute(insert_query, params)
            except (SQLAlchemyError, ValueError, TypeError) as e:
                print(f"Error inserting event: {e}")

        conn.commit()
