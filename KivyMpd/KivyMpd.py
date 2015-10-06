
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

class Album()
    name=""
    artist=""



class KivyMpd(App):

    def __init__(self):
        App.__init__(self)
        self.ip = "192.168.56.101"
        self.trackposistouched = False
        self.running = False
        self.client = MPDClient(use_unicode=True)

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

        while not connected:
            try:
                self.client.connect(self.config.get('main', 'ip'), 6600)
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

    def btncallback(self,instance):
        try:
            self.client.clear()
            for x in self.client.find('album', instance.id):
                self.client.add(x['file'])
            self.client.play(0)
        except:
            pass


    def build(self):

        self.connect_client()

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for a in albums:
            btn = Button(text=a.artist + " - " + a.name, id=a.name, size_hint_y=None, height=40)
            btn.bind(on_press=self.btncallback)
            layout.add_widget(btn)
        root = ScrollView(size_hint=(None, None), size=(400, 400), pos_hint={'x': 0.3, 'top':1})
        root.add_widget(layout)

        hdivider = FloatLayout()

        volume = FloatLayout()
        vol_slider = Slider(orientation='vertical', size_hint=(None, None), width=100, height=400, pos_hint={'top': 0.95}, step=1)
        vol_label = Label(text="0", size_hint=(None, None), pos_hint={'top': 0.2})

        def OnSliderValueChange(instance,value):
             vol_label.text = str(int(value))
             client.setvol(int(value))

        vol_slider.bind(value=OnSliderValueChange)
        vol_slider.value = int(client.status()['volume'])

        volume.add_widget(vol_slider)
        volume.add_widget(vol_label)

        back = Button(background_normal="media_skip_backward.png", size_hint=(None,None), height=50, width=50)
        next = Button(background_normal="media_skip_forward.png", size_hint=(None,None), height=50, width=50)
        stop = Button(background_normal="media_playback_stop.png", size_hint=(None,None), height=50, width=50)
        play = Button(background_normal="media_playback_start.png", size_hint=(None,None), height=50, width=50)

        controls = GridLayout(cols=4,spacing=10, pos_hint={'top': 0.13, 'x': 0.7})
        controls.add_widget(back)
        controls.add_widget(next)
        controls.add_widget(stop)
        controls.add_widget(play)

        trackpos = Slider(size_hint=(None, None), width=400, height=50, pos_hint={'x': 0.15, 'top': 0.12})

        hdivider.add_widget(volume)
        hdivider.add_widget(root)

        hdivider.add_widget(controls)

        nowplaying = Label(text="Now Playing: Nothing", size_hint=(None, None), pos_hint={'x': 0.15, 'top': 0.15})
        nowplaying.bind(texture_size=nowplaying.setter('size'))

        trackelapsed = Label(text="0:00", size_hint=(None, None), pos_hint={'x': 0.64, 'top': 0.08})
        trackelapsed.bind(texture_size=trackelapsed.setter('size'))

        hdivider.add_widget(nowplaying)
        hdivider.add_widget(trackpos)
        hdivider.add_widget(trackelapsed)

        def trackpostouchdown(instance,touch):
            if instance.collide_point(*touch.pos):
                self.trackposistouched = True

        def trackpostouchup(instance,touch):
            if self.trackposistouched:
                client.seekcur(int(math.floor(instance.value)))
                self.trackposistouched = False

        def trackposvaluechanged(instance,value):
            m, s = divmod(int(value), 60)
            trackelapsed.text = str(m) + ":" + str(s).zfill(2)


        trackpos.bind(on_touch_down=trackpostouchdown)
        trackpos.bind(on_touch_up=trackpostouchup)
        trackpos.bind(value=trackposvaluechanged)

        def test(dt):
            try:
                if not self.trackposistouched:

                    stat = client.status()

                    if "songid" in stat:
                        song = client.playlistid(stat['songid'])[0]
                        duration = int(song['time'])
                        m, s = divmod(duration, 60)

                        if "artist" in song and "title" in song:
                            nowplaying.text = song['artist'] + ' - ' + song["title"] + ' ' + str(m) + ":" + str(s).zfill(2)
                        elif "file" in song:
                            nowplaying.text = song['file']

                        trackpos.max = duration

                        if "elapsed" in stat:
                            elapsed = int(math.floor(float(stat['elapsed'])))
                            m, s = divmod(elapsed, 60)
                            trackpos.value = elapsed
                        else:
                            trackpos.value = 0

                    else:
                        nowplaying.text = ""
            except:
                print "Unexpected error:", sys.exc_info()[0]
                connected = False

                while not connected:
                    try:
                        client.connect(self.ip, 6600)
                        connected = True
                    except:
                        print "reconnect"
                        time.sleep(1)

        Clock.schedule_interval(test, 1)

        return hdivider



if __name__=='__main__':
    KivyMpd().run()