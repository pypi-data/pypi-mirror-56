#############################################################################################
#                                                                                           #
# Author:   GeoPy Team                                                                      #
# Date:     March 2018                                                                      #
#                                                                                           #
#############################################################################################

__version__ = '1.0.0'

__all__ = ['data', 'mdict', 'curve', 'image', 'video']


import os, sys
sys.path.append(os.path.dirname(__file__)[:-6])
#
from basic.data import data as data
from basic.matdict import matdict as mdict
from basic.curve import curve as curve
from basic.image import image as image
from basic.video import video as video