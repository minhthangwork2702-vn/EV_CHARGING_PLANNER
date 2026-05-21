import random

from core.traffic import traffic_speed

from core.objective_functions import (

    total_distance,

    total_travel_time,

    congestion_penalty,

    ideal_location_score
)

from core.constraints import (

    distance_constraint,

    radius_constraint
)

from config import (

    ALPHA,

    BETA,

    GAMMA,

    VMAX,

    K2,

    K1_TH1,

    K1_TH2,

    K1_TH3,

    DENSITY_HIGH,

    DENSITY_MEDIUM,

    MAX_TOTAL_DISTANCE,

    MAX_RADIUS
)


# =========================================================
# SELECT K1
# =========================================================

def select_k1(density):

    if density >= DENSITY_HIGH:

        return K1_TH1

    elif density >= DENSITY_MEDIUM:

        return K1_TH2

    return K1_TH3


# =========================================================
# FIND BEST LOCATION
# =========================================================

def find_best_location(
    G,
    candidate_points,
    existing_stations,
    candidate_metadata
):

    best_point = None

    best_score = float("inf")

    results = []

    for point in candidate_points:

        meta = candidate_metadata.get(point, {})

        charger_type = meta.get(
            "charger_type",
            "AC_11KW"
        )

        num_chargers = meta.get(
            "num_chargers",
            1
        )

        # =================================================
        # TRAFFIC SIMULATION
        # =================================================

        density = round(
            random.uniform(1.5, 4.0),
            2
        )

        weather = round(
            random.uniform(0, 1),
            2
        )

        accidents = random.randint(0, 2)

        # =================================================
        # SELECT K1
        # =================================================

        k1 = select_k1(density)

        # =================================================
        # SPEED
        # =================================================

        speed = traffic_speed(

            vmax=VMAX,

            density=density,

            weather_factor=weather,

            k1=k1,

            k2=K2
        )

        # =================================================
        # DISTANCE
        # =================================================

        total_d, distances = total_distance(

            G,

            point,

            existing_stations
        )

        # =================================================
        # CONSTRAINTS
        # =================================================

        if not distance_constraint(

            total_d,

            MAX_TOTAL_DISTANCE
        ):

            continue

        if not radius_constraint(

            distances,

            MAX_RADIUS
        ):

            continue

        # =================================================
        # TIME
        # =================================================

        total_t = total_travel_time(

            total_d,

            speed
        )

        # =================================================
        # CONGESTION
        # =================================================

        congestion = congestion_penalty(

            density,

            accidents
        )

        # =================================================
        # SCORE
        # =================================================

        score = ideal_location_score(

            total_d,

            total_t,

            congestion,

            ALPHA,

            BETA,

            GAMMA
        )

        # =================================================
        # SAVE RESULTS
        # =================================================

        results.append({

            "Latitude": point[0],

            "Longitude": point[1],

            "Charger Type": charger_type,

            "Chargers": num_chargers,

            "Density": density,

            "Speed": round(speed, 2),

            "Total Distance": round(total_d, 2),

            "Travel Time": round(total_t, 2),

            "Congestion": round(congestion, 2),

            "Score": round(score, 2)
        })

        # =================================================
        # BEST
        # =================================================

        if score < best_score:

            best_score = score

            best_point = point

    return best_point, best_score, results