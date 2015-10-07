import kivy
kivy.require('1.9.0')

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', '0')
#Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.write()

from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock
from mpd import MPDClient
from kivy.uix.settings import SettingsWithNoMenu
import time
import sys
import math


class ScrollButton(Button):
    album = "default"


class ControlButton(Button):
    pass


class Album:
    name = ""
    artist = ""


class KivyMpd2(App):

    client = MPDClient(use_unicode=True)
    track_pos_is_touched = False

    def connect_client(self):
        connected = False
        ip = self.config.get('main', 'ip')

        #while not connected:
        try:
            self.client.connect(ip, 6600)
            self.refresh_albums_tab()

            connected = True
        except:
            pass

    def get_albums(self):

        albums = []

        try:
            for sAlbum in self.client.list("album"):
                album = Album()
                album.name = sAlbum
                artists = self.client.list("artist", "album", sAlbum)
                if len(artists) == 1:
                    album.artist = artists[0]
                elif len(artists) > 1:
                    album.artist = "VA"
                elif len(artists) == 0:
                    album.artist = "Unknown"
                albums.append(album)

            albums.sort(key=lambda x: (x.artist, x.name))

            for x in range(100):
                albums.append(Album())
        except:
            pass

        return albums

    def album_btn_press(self, instance):
        try:
            print instance.album
            self.client.clear()
            for x in self.client.find('album', instance.album):
                self.client.add(x['file'])
            self.client.play(0)
        except:
            pass

    def update_status(self, dt):
        try:
            if not self.track_pos_is_touched:
                stat = self.client.status()

                if "songid" in stat:
                    song = self.client.playlistid(stat['songid'])[0]
                    duration = int(song['time'])
                    m, s = divmod(duration, 60)

                    if "artist" in song and "title" in song:
                        self.root.ids.now_playing.text = song['artist'] + ' - ' + song["title"] + ' ' + str(m) + ":" + str(s).zfill(2)
                    elif "file" in song:
                        self.root.ids.now_playing.text = song['file']

                    self.root.ids.track_pos.max = duration

                    if "elapsed" in stat:
                        elapsed = int(math.floor(float(stat['elapsed'])))
                        self.root.ids.track_pos.value = elapsed
                    else:
                        self.root.ids.track_pos.value = 0

                else:
                    self.root.ids.now_playing.text = ""
        except:
            print sys.exc_info()
            self.connect_client()

    def vol_slider_change(self, instance, value):
        try:
            self.client.setvol(int(value))
        except:
            pass

    def back_btn_press(self, instance):
        try:
            self.client.previous()
        except:
            print sys.exc_info()

    def next_btn_press(self, instance):
        try:
            self.client.next()
        except:
            print sys.exc_info()

    def pause_btn_press(self, instance):
        try:
            self.client.pause(1)
        except:
            print sys.exc_info()

    def play_btn_press(self, instance):
        try:
            self.client.pause(0)
        except:
            print sys.exc_info()

    def format_track_elapsed(self, value):
        m, s = divmod(int(value), 60)
        return str(m) + ":" + str(s).zfill(2)

    def track_pos_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
           self.track_pos_is_touched = True

    def track_pos_touch_up(self, instance, touch):
        if self.track_pos_is_touched:
            try:
                self.client.seekcur(int(math.floor(instance.value)))
            except:
                pass
            self.track_pos_is_touched = False

    def refresh_albums_tab(self):
        container = self.root.ids.container
        container.clear_widgets()

        for a in self.get_albums():
            sb = ScrollButton(text=a.artist + ' - ' + a.name)
            sb.album = a.name
            container.add_widget(sb)

    def build(self):

        super(KivyMpd2, self).build()

        # self.use_kivy_settings = False
        # self.settings_cls = SettingsWithNoMenu

        self.connect_client()

        try:
            stat = self.client.status()
            self.root.ids.vol_slider.value = int(stat['volume'])
            self.root.ids.vol_slider.bind(value=self.vol_slider_change)
        except:
            pass

        Clock.schedule_interval(self.update_status, 1)

        #self.open_settings()

        return self.root

    def build_config(self, config):
        config.setdefaults('main', {
            'ip': '192.168.56.101'
        })

#    def build_settings(self, settings):
 #       settings.add_json_panel('Settings', self.config, 'settings.json')

    # def display_settings(self, settings):
    #     if self.root.ids.settings_tab.content is not settings:
    #         self.root.ids.settings_tab.add_widget(settings)
    #         return True
    #     return False

if __name__ == '__main__':
    KivyMpd2().run()