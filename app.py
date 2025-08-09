import streamlit as st
from streamlit_option_menu import option_menu
from pages.home_page import home_page
from pages.view_previous_events import view_previous_events # ✅ Import View History function

# Page config
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.set_page_config(
    page_title="Solar Flare Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
    
)

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", "Prediction", "View Previous Events","About", "Contact"],
        icons=["house", "activity","clock-history", "info-circle", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical"
    )

# Main page content based on selected option
st.markdown("<h1 style='text-align: center;'>AI-Based Solar Flare Monitoring & Forecasting System</h1>", unsafe_allow_html=True)

if selected == "Home":
    home_page()
elif selected == "Prediction":
    st.subheader("📈 Make a Prediction")
    st.write("Coming soon: Enter parameters or a date to predict solar flares.")
elif selected == "View Previous Events":
    view_previous_events()
elif selected == "About":
    st.subheader("ℹ️ About the Project")
    st.write("""
        This app was developed as part of a research project to forecast space weather events 
        using machine learning and deep learning models.
    """)

elif selected == "Contact":
    st.subheader("📧 Contact Us")
    st.write("Email: spaceai@research.org")

