#############################################################################################
#                                                                                           #
# Author:   GeoPy Team                                                                      #
# Date:     March 2018                                                                      #
#                                                                                           #
#############################################################################################

__version__ = '1.0.0'

__all__ = ['io', 'ays', 'vis', 'attrib']

import os, sys
sys.path.append(os.path.dirname(__file__)[:-8])
#
from seismic.inputoutput import inputoutput as io
from seismic.analysis import analysis as ays
from seismic.visualization import visualization as vis
from seismic.attribute import attribute as attrib