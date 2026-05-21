import os

import osmnx as ox
import geopandas as gpd
import streamlit as st

from config import PLACE


GRAPH_PATH = "data/district1.graphml"
BOUNDARY_PATH = "data/district1_boundary.geojson"


# =========================================================
# CHECK FILES
# =========================================================

def check_data_files():

    missing = []

    if not os.path.exists(GRAPH_PATH):
        missing.append(GRAPH_PATH)

    if not os.path.exists(BOUNDARY_PATH):
        missing.append(BOUNDARY_PATH)

    return missing


# =========================================================
# LOAD BOUNDARY
# =========================================================

@st.cache_data
def load_boundary():

    # ============================================
    # LOAD LOCAL FILE IF EXISTS
    # ============================================

    if os.path.exists(BOUNDARY_PATH):

        gdf = gpd.read_file(BOUNDARY_PATH)

        if gdf.crs is None:

            gdf.set_crs(epsg=4326, inplace=True)

        return gdf

    # ============================================
    # OTHERWISE DOWNLOAD FROM OSM
    # ============================================

    st.warning(
        "Boundary file not found. Downloading from OpenStreetMap..."
    )

    gdf = ox.geocode_to_gdf(PLACE)

    os.makedirs("data", exist_ok=True)

    gdf.to_file(
        BOUNDARY_PATH,
        driver="GeoJSON"
    )

    return gdf


# =========================================================
# LOAD GRAPH
# =========================================================

@st.cache_resource
def load_graph():

    # ============================================
    # LOAD LOCAL GRAPH
    # ============================================

    if os.path.exists(GRAPH_PATH):

        return ox.load_graphml(GRAPH_PATH)

    # ============================================
    # DOWNLOAD GRAPH
    # ============================================

    st.warning(
        "Road graph not found. Downloading from OpenStreetMap..."
    )

    G = ox.graph_from_place(
        PLACE,
        network_type="drive"
    )

    os.makedirs("data", exist_ok=True)

    ox.save_graphml(
        G,
        GRAPH_PATH
    )

    return G


# =========================================================
# EXISTING STATIONS
# =========================================================

def load_existing_stations():

    return [

        (10.7765, 106.7009),
        (10.7738, 106.6981),
        (10.7712, 106.6954),
        (10.7685, 106.7023)
    ]