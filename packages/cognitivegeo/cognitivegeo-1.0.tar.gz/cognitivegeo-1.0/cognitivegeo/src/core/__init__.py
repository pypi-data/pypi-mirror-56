#############################################################################################
#                                                                                           #
# Author:   GeoPy Team                                                                      #
# Date:     March 2018                                                                      #
#                                                                                           #
#############################################################################################

__version__ = '1.0.0'

__all__ = ['keyboard', 'settings']


import os, sys
sys.path.append(os.path.dirname(__file__)[:-5])
#
from core.keyboard import keyboard as keyboard
from core.settings import settings as settings