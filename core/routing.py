import osmnx as ox

import networkx as nx


# =========================================================
# NETWORK DISTANCE
# =========================================================

def network_distance_km(
    G,
    point_a,
    point_b
):

    lat1, lon1 = point_a

    lat2, lon2 = point_b

    node_a = ox.distance.nearest_nodes(
        G,
        lon1,
        lat1
    )

    node_b = ox.distance.nearest_nodes(
        G,
        lon2,
        lat2
    )

    try:

        length_m = nx.shortest_path_length(
            G,
            node_a,
            node_b,
            weight="length"
        )

        return length_m / 1000

    except:

        return 9999