import os

import pandas as pd

import streamlit as st

from core.gis_loader import (

    load_boundary,

    load_graph,

    load_existing_stations
)

from map.map_builder import create_map

from core.optimization import find_best_location

from config import (

    PAGE_TITLE,

    LAYOUT,

    CHARGER_TYPES
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(

    page_title=PAGE_TITLE,

    layout=LAYOUT
)

# =========================================================
# LOAD GIS DATA
# =========================================================

try:

    with st.spinner("Loading GIS data..."):

        gdf = load_boundary()

        G = load_graph()

except Exception as e:

    st.error(f"GIS loading failed: {e}")

    st.stop()

# =========================================================
# EXISTING STATIONS
# =========================================================

existing_stations = load_existing_stations()

# =========================================================
# SESSION STATE
# =========================================================

if "candidate_points" not in st.session_state:

    st.session_state.candidate_points = []

if "candidate_metadata" not in st.session_state:

    st.session_state.candidate_metadata = {}

if "optimization_results" not in st.session_state:

    st.session_state.optimization_results = None

if "last_processed_click" not in st.session_state:

    st.session_state.last_processed_click = None

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Charger Configuration")

selected_charger = st.sidebar.selectbox(

    "Select Charger Type",

    list(CHARGER_TYPES.keys())
)

number_of_chargers = st.sidebar.slider(

    "Number of Chargers",

    min_value=1,

    max_value=20,

    value=4
)

# =========================================================
# TITLE
# =========================================================

st.title("EV Charging Optimization Model")

st.markdown("""

Click on the map to add candidate EV charging locations.

The model evaluates:
- road routing
- travel time
- congestion
- charger configuration
""")

# =========================================================
# MAP
# =========================================================

map_data = create_map(

    gdf=gdf,

    existing_stations=existing_stations,

    candidate_points=st.session_state.candidate_points,

    candidate_metadata=st.session_state.candidate_metadata
)

# =========================================================
# HANDLE MAP CLICK
# =========================================================

if map_data is not None:

    clicked = map_data.get("last_clicked")

    if clicked is not None:

        lat = round(clicked["lat"], 6)

        lng = round(clicked["lng"], 6)

        point = (lat, lng)

        # =================================================
        # PREVENT DUPLICATE PROCESSING
        # =================================================

        if point != st.session_state.last_processed_click:

            st.session_state.last_processed_click = point

            if point not in st.session_state.candidate_points:

                st.session_state.candidate_points.append(point)

                st.session_state.candidate_metadata[point] = {

                    "charger_type": selected_charger,

                    "num_chargers": number_of_chargers
                }

# =========================================================
# BUTTONS
# =========================================================

col_run, col_clear = st.columns([1, 1])

with col_run:

    run_clicked = st.button(

        "Run Optimization",

        use_container_width=True
    )

with col_clear:

    clear_clicked = st.button(

        "Clear Candidates",

        use_container_width=True
    )

# =========================================================
# CLEAR LOGIC
# =========================================================

if clear_clicked:

    st.session_state.candidate_points = []

    st.session_state.candidate_metadata = {}

    st.session_state.optimization_results = None

    st.session_state.last_processed_click = None

# =========================================================
# RUN OPTIMIZATION
# =========================================================

if run_clicked:

    if len(st.session_state.candidate_points) == 0:

        st.warning(

            "Please add at least one candidate point."
        )

    else:

        with st.spinner("Running optimization..."):

            best_point, best_score, results = find_best_location(

                G=G,

                candidate_points=st.session_state.candidate_points,

                existing_stations=existing_stations,

                candidate_metadata=st.session_state.candidate_metadata
            )

        st.session_state.optimization_results = {

            "best_point": best_point,

            "best_score": best_score,

            "results": results
        }

# =========================================================
# SHOW RESULTS
# =========================================================

if st.session_state.optimization_results is not None:

    res = st.session_state.optimization_results

    best_point = res["best_point"]

    best_score = res["best_score"]

    results = res["results"]

    st.subheader("Optimization Result")

    if best_point is None:

        st.error(

            "No valid location found."
        )

    else:

        st.success(

            f"Best Location: {best_point}"
        )

        st.metric(

            "Optimization Score",

            round(best_score, 4)
        )

        df = pd.DataFrame(results)

        st.subheader("All Candidate Results")

        st.dataframe(

            df,

            use_container_width=True
        )

        # =================================================
        # EXPORT CSV
        # =================================================

        os.makedirs(

            "data/exports",

            exist_ok=True
        )

        export_path = (

            "data/exports/optimization_results.csv"
        )

        df.to_csv(

            export_path,

            index=False
        )

        st.caption(

            f"Results exported to {export_path}"
        )

# =========================================================
# CANDIDATE TABLE
# =========================================================

st.subheader("Candidate Locations")

if len(st.session_state.candidate_points) == 0:

    st.info(

        "No candidate locations added yet."
    )

else:

    rows = []

    for point in st.session_state.candidate_points:

        meta = st.session_state.candidate_metadata.get(

            point,

            {}
        )

        rows.append({

            "Latitude": point[0],

            "Longitude": point[1],

            "Charger Type": meta.get(
                "charger_type"
            ),

            "Number of Chargers": meta.get(
                "num_chargers"
            )
        })

    st.dataframe(

        pd.DataFrame(rows),

        use_container_width=True
    )