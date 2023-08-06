from ddcmaker import __version__

import os
def get_eq_type():
    if os._exists("/home/pi/human")==True:
        return 0
    elif os._exists("/home/pi/Car")==True:
        return 1
    elif os._exists("/home/pi/human_code")==True:
        return 2
    elif os._exists("/home/pi/spider")==True:
        return 3
    else:
        return -1