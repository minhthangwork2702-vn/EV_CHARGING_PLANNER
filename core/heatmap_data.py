import random

import streamlit as st


# =========================================================
# HEATMAP DATA
# =========================================================

@st.cache_data
def generate_heatmap_points():

    random.seed(42)

    points = []

    center_lat = 10.775

    center_lon = 106.700

    for _ in range(300):

        lat = center_lat + random.uniform(-0.015, 0.015)

        lon = center_lon + random.uniform(-0.015, 0.015)

        weight = random.randint(1, 10)

        points.append([

            lat,

            lon,

            weight
        ])

    return points