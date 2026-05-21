import osmnx as ox

PLACE = "District 1, Ho Chi Minh City, Vietnam"

gdf = ox.geocode_to_gdf(PLACE)

gdf.to_file(

    "data/district1_boundary.geojson",

    driver="GeoJSON"
)

print("Boundary saved")