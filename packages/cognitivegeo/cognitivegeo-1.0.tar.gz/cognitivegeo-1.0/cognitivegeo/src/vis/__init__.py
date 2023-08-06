#############################################################################################
#                                                                                           #
# Author:   GeoPy Team                                                                      #
# Date:     January 2019                                                                    #
#                                                                                           #
#############################################################################################

__version__ = '1.0.0'

__all__ = ['font', 'color', 'line', 'marker',
           'image', 'video', 'player', 'viewer3d']

import os, sys
sys.path.append(os.path.dirname(__file__)[:-4])
#
from vis.font import font as font
from vis.color import color as color
from vis.line import line as line
from vis.marker import marker as marker
from vis.colormap import colormap as cmap
from vis.image import image as image
from vis.video import video as video
from vis.player import player as player
from vis.viewer3d import viewer3d as viewer3d