import numpy as np
import math

import serial
import time
def calculate_steer(x_mean_frame, x_mean_bott, x_mean_top, min_y, max_y):
    delta_x = x_mean_top - x_mean_bott
    delta_y = abs(min_y-max_y)
    alpha = int(math.degrees(math.atan(delta_x/delta_y)))
    #### delta treshold ###
    direction, angle = None, None
    ### turn right
    if 10 < delta_x :
        direction, angle = 'right', alpha
    elif delta_x < -10:
        direction, angle = 'left', alpha
    else:
        direction, angle = 'straight', alpha
    return direction, angle

