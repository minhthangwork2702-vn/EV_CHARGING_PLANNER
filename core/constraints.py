# =========================================================
# TOTAL DISTANCE CONSTRAINT
# =========================================================

def distance_constraint(
    total_distance,
    max_distance
):

    return total_distance <= max_distance


# =========================================================
# RADIUS CONSTRAINT
# =========================================================

def radius_constraint(
    distances,
    max_radius
):

    return all(
        d <= max_radius
        for d in distances
    )