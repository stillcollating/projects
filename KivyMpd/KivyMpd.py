
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


class KivyMpd(App):

    def build(self):

        client = MPDClient(use_unicode=True)

        client.connect("192.168.56.101", 6600)


      #  for key, value in client.status().items():
      #  print("%s: %s" % (key, value))

    #    client.command_list_ok_begin()

        client.update()

        # for i in range(1,10):
        #     client.send_idle()
        #     changes = client.fetch_idle()
        #     print changes


        # for key, value in client.status().items():
        #     print("%s: %s" % (key, value))
        #
        # for artist in client.list("artist"):
        #     for album in client.list("album", "artist", artist):
        #         for song in client.find("artist", artist, "album", album):
        #             for k, v in song.iteritems():
        #                 print k + " " + v



        class Album:
            name = ''
            artist = ''

        albums = []

        for sAlbum in client.list("album"):
            album = Album()
            album.name = sAlbum
            artists = client.list("artist", "album", sAlbum)
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

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for a in albums:
            btn = Button(text=a.artist + " - " + a.name, size_hint_y=None, height=40)
            layout.add_widget(btn)
        root = ScrollView(size_hint=(None, None), size=(480, 480), pos_hint={'x': 0.3})
        root.add_widget(layout)

        divider = FloatLayout()
        volume = FloatLayout()
        vol_slider = Slider(orientation='vertical', size_hint=(None, None), width=100, height=400, pos_hint={'top': 0.95}, step=1)
        vol_label = Label(text="0", size_hint=(None, None), pos_hint={'top': 0.2})
        def OnSliderValueChange(instance,value):
             vol_label.text = str(int(value))

        vol_slider.bind(value=OnSliderValueChange)

        volume.add_widget(vol_slider)
        volume.add_widget(vol_label)

        divider.add_widget(volume)
        divider.add_widget(root)

        return divider


if __name__=='__main__':
    KivyMpd().run()