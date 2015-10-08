
import kivy
kivy.require('1.9.0')

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', '0')
Config.write()

from kivy.app import App
from kivy.uix.label import Label
from mpd import MPDClient
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.widget import  Widget

import time
import math
import sys

class Album:
    name = ""
    artist = ""

class KivyMpd(App):

    trackpos_is_touched = False
    running = False
    client = MPDClient(use_unicode=True)

    _vol_label = None
    _track_elapsed = None
    _trackpos = None
    _nowplaying = None

    p = None

    def build_config(self, config):
        config.setdefaults('main', {
            'ip': '192.168.56.101'
        })

    def on_start(self):
        self.running = True

    def on_stop(self):
        self.running = False

    def connect_client(self):
        connected = False
        ip = self.config.get('main', 'ip')

        while not connected:
            try:
                self.client.connect(ip, 6600)
                connected = True
            except:
                time.sleep(1)

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
            self.client.clear()
            for x in self.client.find('album', instance.id):
                self.client.add(x['file'])
            self.client.play(0)
        except:
            pass

    def vol_slider_change(self, instance, value):
        try:
            self.client.setvol(int(value))
            self._vol_label.text = str(int(value))
        except:
            pass

    def trackpos_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
           self.trackpos_is_touched = True

    def trackpos_touch_up(self, instance, touch):
        if self.trackpos_is_touched:
            try:
                self.client.seekcur(int(math.floor(instance.value)))
            except:
                pass
            self.trackpos_is_touched = False

    def trackpos_changed(self, instance, value):
        m, s = divmod(int(value), 60)
        self._track_elapsed.text = str(m) + ":" + str(s).zfill(2)

    def update_status(self, dt):
        try:
            if not self.trackpos_is_touched:

                stat = self.client.status()

                if "songid" in stat:
                    song = self.client.playlistid(stat['songid'])[0]
                    duration = int(song['time'])
                    m, s = divmod(duration, 60)

                    if "artist" in song and "title" in song:
                        self._nowplaying.text = song['artist'] + ' - ' + song["title"] + ' ' + str(m) + ":" + str(s).zfill(2)
                    elif "file" in song:
                        self._nowplaying.text = song['file']

                    self._trackpos.max = duration

                    if "elapsed" in stat:
                        elapsed = int(math.floor(float(stat['elapsed'])))
                        m, s = divmod(elapsed, 60)
                        self._trackpos.value = elapsed
                    else:
                        self._trackpos.value = 0
                else:
                    self._nowplaying.text = ""
        except:
            print sys.exc_info()
            self.connect_client()

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

    def build(self):

        self.connect_client()

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for a in self.get_albums():
            btn = Button(text=a.artist + " - " + a.name, id=a.name, size_hint_y=None, height=40)
            btn.bind(on_press=self.album_btn_press)
            layout.add_widget(btn)
        root = ScrollView(size_hint=(None, None), size=(400, 400), pos_hint={'x': 0.3, 'top':1})
        root.add_widget(layout)

        hdivider = FloatLayout()

        volume = FloatLayout()
        vol_slider = Slider(orientation='vertical', size_hint=(None, None), width=100, height=400, pos_hint={'top': 0.95}, step=1)
        self._vol_label = Label(text="0", size_hint=(None, None), pos_hint={'top': 0.2})

        vol_slider.bind(value=self.vol_slider_change)
        vol_slider.value = int(self.client.status()['volume'])

        volume.add_widget(vol_slider)
        volume.add_widget(self._vol_label)

        back = Button(background_normal="media_skip_backward.png", size_hint=(None,None), height=50, width=50)
        next = Button(background_normal="media_skip_forward.png", size_hint=(None,None), height=50, width=50)
        pause = Button(background_normal="media_playback_pause.png", size_hint=(None,None), height=50, width=50)
        play = Button(background_normal="media_playback_start.png", size_hint=(None,None), height=50, width=50)

        back.bind(on_press=self.back_btn_press)
        next.bind(on_press=self.next_btn_press)
        pause.bind(on_press=self.pause_btn_press)
        play.bind(on_press=self.play_btn_press)

        controls = GridLayout(cols=4,spacing=10, pos_hint={'top': 0.13, 'x': 0.7})
        controls.add_widget(back)
        controls.add_widget(next)
        controls.add_widget(pause)
        controls.add_widget(play)

        self._trackpos = Slider(size_hint=(None, None), width=400, height=50, pos_hint={'x': 0.15, 'top': 0.12})

        hdivider.add_widget(volume)
        hdivider.add_widget(root)

        hdivider.add_widget(controls)

        self._nowplaying = Label(text="Now Playing: Nothing", size_hint=(None, None), pos_hint={'x': 0.15, 'top': 0.15})
        self._nowplaying.bind(texture_size= self._nowplaying.setter('size'))

        self._track_elapsed = Label(text="0:00", size_hint=(None, None), pos_hint={'x': 0.64, 'top': 0.08})
        self._track_elapsed.bind(texture_size=self._track_elapsed.setter('size'))

        hdivider.add_widget(self._nowplaying)
        hdivider.add_widget(self._trackpos)
        hdivider.add_widget(self._track_elapsed)

        self._trackpos.bind(on_touch_down=self.trackpos_touch_down)
        self._trackpos.bind(on_touch_up=self.trackpos_touch_up)
        self._trackpos.bind(value=self.trackpos_changed)

        Clock.schedule_interval(self.update_status, 1)

        return hdivider



if __name__=='__main__':
    KivyMpd().run()