import streamlit as st
import requests
#branch for solar - testing
API_BASE_URL = "https://images-api.nasa.gov/search"

def search_nasa_media(query, media_type="image", year_start=None, year_end=None):
    params = {
        "q": query,
        "media_type": media_type,
    }
    if year_start:
        params["year_start"] = year_start
    if year_end:
        params["year_end"] = year_end

    response = requests.get(API_BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def display_results(data, query):
    items = data.get("collection", {}).get("items", [])

    if not items:
        st.warning("No results found.")
        return

    st.write(f"Found {len(items)} results for '{query}'")

    num_cols = 3
    rows = (len(items[:20]) + num_cols - 1) // num_cols

    for row_idx in range(rows):
        cols = st.columns(num_cols)
        for col_idx in range(num_cols):
            item_idx = row_idx * num_cols + col_idx
            if item_idx >= len(items[:20]):
                break
            item = items[item_idx]
            data_item = item.get("data", [{}])[0]
            links = item.get("links", [{}])
            title = data_item.get("title", "No Title")
            description = data_item.get("description", "")
            nasa_id = data_item.get("nasa_id", "")
            media_link = None

            for link in links:
                if link.get("rel") == "preview" or link.get("render") == "image":
                    media_link = link.get("href")
                    break

            with cols[col_idx]:
                if media_link:
                    st.image(media_link, caption=title, use_container_width=True)
                else:
                    st.write(f"**{title}**")

                short_desc = description if len(description) < 150 else description[:147] + "..."
                st.write(short_desc)

                st.markdown(f"[View Details on NASA](https://images.nasa.gov/details-{nasa_id})")
                st.markdown("---")

def home_page():
    st.set_page_config(page_title="Home", page_icon="🪐", layout="wide")
    st.title("Learning about the universe")

    query = st.text_input("Search NASA media", value="sun", max_chars=50)
    media_type = st.selectbox("Media type", options=["image", "video", "audio"], index=0)
    col1, col2 = st.columns(2)
    with col1:
        year_start = st.number_input("Year start", min_value=1920, max_value=2025, value=2010)
    with col2:
        year_end = st.number_input("Year end", min_value=1920, max_value=2025, value=2025)

    # Auto-load sun images when page loads
    if "initial_load_done" not in st.session_state:
        try:
            data = search_nasa_media("sun", "image", year_start, year_end)
            display_results(data, "sun")
        except Exception as e:
            st.error(f"Error fetching NASA media: {e}")
        st.session_state.initial_load_done = True

# Manual search button
    if st.button("Search"):
        try:
            data = search_nasa_media(query, media_type, year_start, year_end)
            display_results(data, query)
        except Exception as e:
            st.error(f"Error fetching NASA media: {e}")

if __name__ == "__main__":
    home_page()
