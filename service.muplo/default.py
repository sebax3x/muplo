# -*- coding: utf-8 -*-

import os
import xbmc
import xbmcaddon
import xbmcgui
import schedule

__addon__ = xbmcaddon.Addon()
__addon_id__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
__addonpath__ = xbmc.translatePath(__addon__.getAddonInfo('path'))
__datapath__ = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/')

sys.path.append(os.path.join(__addonpath__, "resources", "lib"))

import serviceMuploMain

# name of script for this service work
serviceForScript = 'script.muplo'

check_server_time = 1  # minutes

class Player(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)

    def onPlayBackStarted(self):
        xbmc.executebuiltin('XBMC.RunScript(' + serviceForScript + ', run)')

    def onPlayBackStopped(self):
        xbmcgui.Window(10000).setProperty('muplo_run', 'false')

player = Player()

serviceMuploMain.Service().check()
schedule.every(check_server_time).minutes.do(serviceMuploMain.Service().check)

while not xbmc.abortRequested:
    xbmc.sleep(100)
    schedule.run_pending()
