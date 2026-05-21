# =========================================================
# APP CONFIG
# =========================================================

PAGE_TITLE = "EV Charging Planner"

LAYOUT = "wide"

# =========================================================
# MAP CONFIG
# =========================================================

PLACE = "District 1, Ho Chi Minh City"

ZOOM_START = 14

MIN_ZOOM = 13

MAX_ZOOM = 20

MAP_TILES = "OpenStreetMap"

# =========================================================
# OPTIMIZATION WEIGHTS
# =========================================================

ALPHA = 0.4

BETA = 0.5

GAMMA = 0.1

# =========================================================
# TRAFFIC MODEL
# =========================================================

VMAX = 50

K2 = 0.3

DENSITY_HIGH = 3.00

DENSITY_MEDIUM = 2.50

K1_TH1 = 0.060

K1_TH2 = 0.035

K1_TH3 = 0.015

# =========================================================
# CONSTRAINTS
# =========================================================

MAX_TOTAL_DISTANCE = 15

MAX_RADIUS = 3

# =========================================================
# EXPORT
# =========================================================

EXPORT_CSV = "data/exports/optimization_results.csv"

# =========================================================
# CHARGER TYPES
# =========================================================

CHARGER_TYPES = {

    "AC_11KW": {

        "power": 11,

        "charging_time": "4-8 hours",

        "cars_per_hour": 2,

        "color": "blue"
    },

    "DC_60KW": {

        "power": 60,

        "charging_time": "1-2 hours",

        "cars_per_hour": 8,

        "color": "orange"
    },

    "SUPERCHARGER_250KW": {

        "power": 250,

        "charging_time": "15-30 minutes",

        "cars_per_hour": 20,

        "color": "red"
    }
}