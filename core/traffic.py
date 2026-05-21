import numpy as np


# =========================================================
# TRAFFIC SPEED MODEL
# =========================================================

def traffic_speed(
    vmax,
    density,
    weather_factor,
    k1,
    k2
):

    speed = vmax * np.exp(

        -k1 * density

        -k2 * weather_factor
    )

    return max(speed, 5)