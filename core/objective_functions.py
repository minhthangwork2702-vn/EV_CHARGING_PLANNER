from core.routing import network_distance_km


# =========================================================
# TOTAL DISTANCE
# =========================================================

def total_distance(
    G,
    point,
    existing_stations
):

    distances = []

    for station in existing_stations:

        d = network_distance_km(
            G,
            point,
            station
        )

        distances.append(d)

    return sum(distances), distances


# =========================================================
# TOTAL TRAVEL TIME
# =========================================================

def total_travel_time(
    total_distance_km,
    speed_kmh
):

    if speed_kmh <= 0:

        return 9999

    return total_distance_km / speed_kmh * 60


# =========================================================
# CONGESTION PENALTY
# =========================================================

def congestion_penalty(
    density,
    accidents
):

    return density * 2 + accidents * 5


# =========================================================
# FINAL SCORE
# =========================================================

def ideal_location_score(
    total_distance,
    travel_time,
    congestion,
    alpha,
    beta,
    gamma
):

    return (

        alpha * total_distance +

        beta * travel_time +

        gamma * congestion
    )