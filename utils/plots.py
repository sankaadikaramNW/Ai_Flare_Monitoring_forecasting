# utils/plots.py

import matplotlib.pyplot as plt
import streamlit as st

def show_histogram(data):
    if data.empty:
        st.warning("No data to plot.")
        return

    fig, ax = plt.subplots()
    ax.bar(data['year'], data['flare_count'])
    ax.set_title("Year-wise Solar Flare Events")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Events")
    st.pyplot(fig)
