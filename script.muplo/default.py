# -*- coding: utf-8 -*-

import os
import sys
import xbmc
import xbmcaddon

__addon__ = xbmcaddon.Addon()
__addonpath__ = xbmc.translatePath(__addon__.getAddonInfo('path'))

sys.path.append(os.path.join(__addonpath__, "resources", "lib"))

import scriptMuploMain