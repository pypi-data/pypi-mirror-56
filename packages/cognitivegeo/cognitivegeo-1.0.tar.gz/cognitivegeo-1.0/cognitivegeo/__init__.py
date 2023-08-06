#############################################################################################
#                                                                                           #
# Author:   GeoPy Team                                                                      #
# Date:     March 2018                                                                      #
#                                                                                           #
#############################################################################################

__version__ = '1.0.0'

__all__ = ['basic', 'core', 'vis', 'seismic', 'psseismic', 'pointset', 'gui']

import os, sys
#
sys.path.append(os.path.dirname(__file__))

import src.basic as basic
import src.core as core
import src.vis as vis
import src.seismic as seismic
import src.psseismic as psseismic
import src.pointset as pointset
from src.gui import gui

if __name__ == "__main__":
    gui.start()