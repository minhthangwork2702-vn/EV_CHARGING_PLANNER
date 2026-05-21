import folium

import streamlit as st

from folium.plugins import HeatMap

from streamlit_folium import st_folium

from config import (

    ZOOM_START,

    MAP_TILES,

    CHARGER_TYPES
)

from core.heatmap_data import generate_heatmap_points


# =========================================================
# GET MAP CENTER
# =========================================================

def get_map_center(gdf):

    bounds = gdf.total_bounds

    minx, miny, maxx, maxy = bounds

    center_lat = (miny + maxy) / 2

    center_lon = (minx + maxx) / 2

    return [center_lat, center_lon]

# =========================================================
# CREATE MAP
# =========================================================

def create_map(

    gdf,

    existing_stations,

    candidate_points,

    candidate_metadata
):

    # =====================================================
    # MAP CENTER
    # =====================================================

    center = get_map_center(gdf)

    # =====================================================
    # CREATE MAP
    # =====================================================

    m = folium.Map(

        location=center,

        zoom_start=ZOOM_START,

        tiles=MAP_TILES,

        control_scale=True
    )

    # =====================================================
    # DISTRICT BOUNDARY
    # =====================================================

    folium.GeoJson(

        gdf,

        name="District 1 Boundary",

        style_function=lambda x: {

            "fillColor": "#00000000",

            "color": "blue",

            "weight": 2
        }

    ).add_to(m)

    # =====================================================
    # AUTO FIT BOUNDARY
    # =====================================================

    bounds = gdf.total_bounds

    minx, miny, maxx, maxy = bounds

    m.fit_bounds([

        [miny, minx],

        [maxy, maxx]
    ])

    # =====================================================
    # EXISTING EV STATIONS
    # =====================================================

    for lat, lon in existing_stations:

        folium.Marker(

            location=[lat, lon],

            tooltip="Existing EV Station",

            icon=folium.Icon(

                color="green",

                icon="flash"
            )

        ).add_to(m)

    # =====================================================
    # CANDIDATE LOCATIONS
    # =====================================================

    for point in candidate_points:

        lat, lon = point

        meta = candidate_metadata.get(
            point,
            {}
        )

        charger_type = meta.get(
            "charger_type",
            "AC_11KW"
        )

        num_chargers = meta.get(
            "num_chargers",
            1
        )

        charger_info = CHARGER_TYPES.get(
            charger_type,
            {}
        )

        color = charger_info.get(
            "color",
            "blue"
        )

        popup_text = f"""
        <b>{charger_type}</b><br>
        Chargers: {num_chargers}
        """

        folium.Marker(

            location=[lat, lon],

            tooltip=charger_type,

            popup=popup_text,

            icon=folium.Icon(

                color=color,

                icon="bolt"
            )

        ).add_to(m)

    # =====================================================
    # HEATMAP
    # =====================================================

    heat_data = generate_heatmap_points()

    HeatMap(

        heat_data,

        radius=18,

        blur=15,

        min_opacity=0.3

    ).add_to(m)

    # =====================================================
    # LAYER CONTROL
    # =====================================================

    folium.LayerControl().add_to(m)

    # =====================================================
    # RETURN STREAMLIT MAP
    # =====================================================

    return st_folium(

        m,

        width=1400,

        height=700,

        key="main_map",

        returned_objects=["last_clicked"]
    )