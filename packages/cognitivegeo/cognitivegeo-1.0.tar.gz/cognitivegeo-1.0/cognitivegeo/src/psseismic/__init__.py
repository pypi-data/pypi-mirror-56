#############################################################################################
#                                                                                           #
# Author:   GeoPy Team                                                                      #
# Date:     January 2019                                                                    #
#                                                                                           #
#############################################################################################

__version__ = '1.0.0'

__all__ = ['io', 'ays', 'vis']

import os, sys
sys.path.append(os.path.dirname(__file__)[:-10])
#
from psseismic.inputoutput import inputoutput as io
from psseismic.analysis import analysis as ays
from psseismic.visualization import visualization as vis