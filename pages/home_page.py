import streamlit as st
import os
import requests

def home_page():
    # ✅ 1. Page Title Header
    

    # ✅ 2. NASA APOD Image Fetch Function (can also be outside function if you prefer)
    def get_apod_image(api_key="P9NIsBAeHZLAL2XQyb9tOgNXdGLvYwyLFzy3lFC2"):
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("url"), data.get("title"), data.get("explanation")
        else:
            return None, None, None
    
    # ✅ 3. Display NASA APOD Image
    
    st.markdown("### NASA Astronomy Picture of the Day ")
    apod_url, apod_title, apod_desc = get_apod_image()

    if apod_url:
        col1,col2=st.columns([1,2])
        with col1:
            st.image(apod_url, caption=apod_title, width=250)
        with col2:
            st.markdown(f"**📝 Description:** {apod_desc}")
    else:
        st.warning("Failed to fetch NASA APOD image.")

    # ✅ 4. Local Image Gallery Section
    image_folder = "images"
    image_files = [f for f in os.listdir(image_folder) if f.endswith((".jpg", ".png", ".jpeg"))]
    image_files.sort()

    # Setup session state index
    if "img_index" not in st.session_state:
        st.session_state.img_index = 0

    # Navigation functions
    def prev_img():
        if st.session_state.img_index > 0:
            st.session_state.img_index -= 1

    def next_img():
        if st.session_state.img_index < len(image_files) - 1:
            st.session_state.img_index += 1

    # ✅ 5. Local Image Gallery UI
    st.markdown("###  Local Solar Image Gallery")

    if image_files:
        image_path = os.path.join(image_folder, image_files[st.session_state.img_index])
        st.image(image_path, caption=image_files[st.session_state.img_index], width=600)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ Previous"):
                prev_img()
        with col2:
            if st.button("Next ➡️"):
                next_img()
    else:
        st.warning("No local images found in the 'images' folder.")
