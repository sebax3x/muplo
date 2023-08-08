import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import time
import json
import schedule
import threading
import re
import urllib.parse
import urllib.request

__addon__ = xbmcaddon.Addon()
__addon_id__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__addonpath__ = xbmc.translatePath(__addon__.getAddonInfo('path'))
__datapath__ = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/')
__path_img__ = os.path.join(__addonpath__, 'images')
__API__ = __addon__.getSetting('api')

class Start:

    def __init__(self):
        try:
            mode = str(sys.argv[1])
        except:
            mode = False

        if mode == 'run':
            Banners().main()
        else:
            Check().check()

class Check:

    def check(self):
        if __addon__.getSetting('m_uid') == '':
            __addon__.openSettings()
            return False
        else:
            url = __API__ + __addon__.getSetting('m_uid')
            test_con = {}
            print(url)
            start = time.time()
            opener = urllib.request.build_opener()
            try:
                response = opener.open(url)
                data = response.read().decode('utf-8')
            except:
                data = ''
                test_con['http'] = '[COLOR=red]error[/COLOR]'
            else:
                test_con['http'] = '[COLOR=green]ok[/COLOR]'

            url_open_time = time.time() - start
            match = re.compile('({[^<]+})').search(data)
            if match is not None:
                test_con['json'] = '[COLOR=green]ok[/COLOR]'
            else:
                test_con['json'] = '[COLOR=red]error[/COLOR]'
            xbmcgui.Dialog().ok('Muplo', 'Http: ' + test_con['http'] + '\nJSON: ' + test_con['json'] + '\ntime: ' + str(round(url_open_time, 2)))
            return

class Banners:

    def main(self):
        schedule.clear()
        try:
            banner_file = open(os.path.join(__datapath__, 'banners.json'), 'r', encoding='utf-8')
        except:
            return False

        json_res = banner_file.read()
        json_res = json.loads(json_res)
        self.createSchedule(json_res)

    def show(self, placement, img, duration):
        if len(xbmcgui.Window(10000).getProperty(placement)) == 0:
            xbmcgui.Window(10000).setProperty(placement, img)
            time.sleep(duration)
            xbmcgui.Window(10000).clearProperty(placement)

    def run_threaded(self, job_func, placement, img, duration):
        job_thread = threading.Thread(target=job_func, args=(placement, img, duration))
        job_thread.start()

    def int_conv(self, a):
        try:
            return int(a)
        except:
            return 0

    def createSchedule(self, json_res):
        xbmcgui.Window(10000).setProperty('muplo_run', 'true')
        schedule.clear()
        xbmcgui.Window(10000).setProperty('muplo_rss', json_res['footer']['text'])
        l_filename = os.path.basename(json_res['logo']['url'])
        l_img = os.path.join(__datapath__, l_filename)
        xbmcgui.Window(10000).setProperty('muplo_' + json_res['logo']['placement'] + '_logo', l_img)
        if json_res['logo']['placement'] == 'left_top':
            xbmcgui.Window(10000).clearProperty('muplo_right_top_logo')
        if json_res['logo']['placement'] == 'right_top':
            xbmcgui.Window(10000).clearProperty('muplo_left_top_logo')
        schedule.every(10).minutes.do(self.main)
        for v in json_res['adverts']:
            xbmcgui.Window(10000).clearProperty(v['placement'])
            placement = v['placement']
            duration = self.int_conv(v['duration'])
            interval = self.int_conv(v['schedule']['interval'])
            unit = v['schedule']['unit']
            at = str(v['schedule']['at'])
            ext = v['url'][-3:]
            img = os.path.join(__datapath__, v['uuid'] + '.' + ext)
            if unit == 'seconds':
                schedule.every(interval).seconds.do(self.run_threaded, self.show, placement, img, duration)
            if unit == 'minutes':
                schedule.every(interval).minutes.do(self.run_threaded, self.show, placement, img, duration)
            if unit == 'hours':
                schedule.every(interval).hours.do(self.run_threaded, self.show, placement, img, duration)
            if unit == 'day':
                schedule.every().day.at(at).do(self.run_threaded, self.show, placement, img, duration)
            if unit == 'monday':
                schedule.every().monday.at(at).do(self.run_threaded, self.show, placement, img, duration)
            if unit == 'tuesday':
                schedule.every().tuesday.at(at).do(self.run_threaded, self.show, placement, img, duration)
            if unit == 'wednesday':
                schedule.every().wednesday.at(at).do(self.run_threaded, self.show, placement, img, duration)
            if unit == 'thursday':
                schedule.every().thursday.at(at).do(self.run_threaded, self.show, placement, img, duration)
            if unit == 'friday':
                schedule.every().friday.at(at).do(self.run_threaded, self.show, placement, img, duration)
            if unit == 'saturday':
                schedule.every().saturday.at(at).do(self.run_threaded, self.show, placement, img, duration)
            if unit == 'sunday':
                schedule.every().sunday.at(at).do(self.run_threaded, self.show, placement, img, duration)

        while True:
            schedule.run_pending()
            time.sleep(1)
            if xbmcgui.Window(10000).getProperty('muplo_run') != 'true':
                schedule.clear()
                break

        schedule.clear()

Start()
