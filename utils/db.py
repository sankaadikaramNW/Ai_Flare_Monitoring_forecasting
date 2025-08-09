import psycopg2
import pandas as pd

# ✅ Step 1: Connect to the database
def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="solar_flare_db",  # Replace with your DB name
            user="postgres",            # Replace with your DB username
            password="123",             # Replace with your DB password
            port=5432
        )
        print("✅ Database connection successful.")
        return conn
    except psycopg2.Error as e:
        print("❌ Failed to connect to the database.")
        print("Error details:", e)
        return None


# ✅ Step 2: Load solar flare data from the DB for selected date range
def get_flare_data_from_db(start_date, end_date):
    conn = get_connection()
    if conn is None:
        print("⚠️ Cannot fetch data. Database connection failed.")
        return pd.DataFrame()  # Return empty DataFrame if failed

    try:
        query = """
            SELECT * FROM solar_flare_events
            WHERE begin_time BETWEEN %s AND %s
            ORDER BY begin_time ASC;
        """
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        print(f"✅ Retrieved {len(df)} records from database.")
        return df
    except Exception as e:
        print("❌ Error while fetching data from DB:", e)
        return pd.DataFrame()
    finally:
        conn.close()


# ✅ Step 3: Save new solar flare API data into the DB
def save_flare_data_to_db(data):
    conn = get_connection()
    if conn is None:
        print("⚠️ Cannot insert data. Database connection failed.")
        return

    cursor = conn.cursor()
    inserted_count = 0

    for event in data:
        try:
            print(f"➡️ Inserting event: {event.get('flrID')}")
            cursor.execute("""
                INSERT INTO solar_flare_events (
                    event_id, begin_time, peak_time, end_time,
                    class_type, source_location, active_region_num, year
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (event_id) DO NOTHING
            """, (
                event.get('flrID'),
                event.get('beginTime'),
                event.get('peakTime'),
                event.get('endTime'),
                event.get('classType'),
                event.get('sourceLocation'),
                event.get('activeRegionNum'),
                pd.to_datetime(event.get('beginTime')).year
            ))
            inserted_count += 1
        except Exception as e:
            print(f"❌ Error inserting event {event.get('flrID')}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Database insert complete. {inserted_count} new records attempted.")
