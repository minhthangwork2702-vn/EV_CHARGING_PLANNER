import osmnx as ox

PLACE = "District 1, Ho Chi Minh City, Vietnam"

print("Downloading graph...")

G = ox.graph_from_place(

    PLACE,

    network_type="drive",

    simplify=True
)

print("Saving graph...")

ox.save_graphml(

    G,

    "data/district1.graphml"
)

print("Done!")