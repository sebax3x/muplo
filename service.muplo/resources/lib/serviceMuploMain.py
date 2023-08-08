import os
import xbmcaddon
import xbmcgui
import schedule
import urllib.parse
import urllib.request
import re
import json

__addon__ = xbmcaddon.Addon()
__addon_id__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
__addonpath__ = xbmc.translatePath(__addon__.getAddonInfo('path'))
__datapath__ = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/')
serviceForScript = 'script.muplo'

class Service:
    def check(self):
        skinJson = '{"jsonrpc":"2.0","method":"Settings.GetSettings", "params":{"level": "basic", "filter": {"section":"appearance", "category":"lookandfeel"}}, "id":1}'
        skinJson = xbmc.executeJSONRPC(skinJson)
        skinJson = json.loads(skinJson)
        if 'result' in skinJson and 'settings' in skinJson['result']:
            for j in skinJson['result']['settings']:
                if 'id' in j and 'value' in j and 'lookandfeel.skin' in j['id']:
                    skin = j['value']
                    break
        else:
            skin = ''

        if skin != 'skin.confluence_muplo':
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Settings.SetSettingValue", "params": {"setting": "lookandfeel.enablerssfeeds", "value": false}, "id": 1}')
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Settings.SetSettingValue", "params": {"setting": "lookandfeel.skin", "value": "skin.confluence_muplo"}, "id": 1}')
        addonJson = '{"jsonrpc":"2.0", "method":"Addons.GetAddonDetails", "params": {"addonid": "script.muplo", "properties": ["enabled"]}, "id":1}'
        addonJson = xbmc.executeJSONRPC(addonJson)
        addonJson = json.loads(addonJson)
        if 'result' in addonJson and 'addon' in addonJson['result'] and 'enabled' in addonJson['result']['addon'] and addonJson['result']['addon']['enabled'] is False:
            xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled", "params": {"addonid": "service.muplo", "enabled": false}, "id":1}')
            return False
        else:
            try:
                __addon__2 = xbmcaddon.Addon(serviceForScript)
            except:
                return False

            __addon_id__2 = __addon__2.getAddonInfo('id')
            __datapath__2 = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__2)).replace('\\', '/')
            __API__ = __addon__2.getSetting('api')
            url = __API__ + __addon__2.getSetting('m_uid')
            try:
                response = urllib.request.urlopen(url)
                data = response.read()
            except:
                return False

            match = re.compile('({[^<]+})').findall(data)
            try:
                output = match[0]
                output = json.loads(output)
            except:
                return False

            uuids = []
            for b in output['adverts']:
                if not os.path.isdir(__datapath__2):
                    os.makedirs(__datapath__2)
                URLext = b['url'][-3:]
                if not os.path.isfile(os.path.join(__datapath__2, b['uuid'] + '.' + URLext)):
                    try:
                        img = urllib.request.urlopen(b['url']).read()
                        with open(os.path.join(__datapath__2, b['uuid'] + '.' + URLext), 'wb') as downloaded_image:
                            downloaded_image.write(img)
                    except:
                        pass

                uuids.append(b['uuid'])

            for file in os.listdir(__datapath__2):
                match = re.compile('^[0-9]+\\.').search(file)
                if match is not None and file[:-4] not in uuids:
                    os.remove(os.path.join(__datapath__2, file))

            logo_filename = os.path.basename(output['logo']['url'])
            if not os.path.isfile(os.path.join(__datapath__2, logo_filename)):
                try:
                    img = urllib.request.urlopen(output['logo']['url']).read()
                    with open(os.path.join(__datapath__2, logo_filename), 'wb') as downloaded_logo:
                        downloaded_logo.write(img)
                except:
                    pass

            with open(os.path.join(__datapath__2, 'banners.json'), 'w') as downloaded_json:
                downloaded_json.write(json.dumps(output))
            return
