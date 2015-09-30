
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from mpd import MPDClient


class KivyMpd(App):

    def build(self):

        client = MPDClient(use_unicode=True)

        client.connect("192.168.56.101", 6600)


      #  for key, value in client.status().items():
      #  print("%s: %s" % (key, value))

    #    client.command_list_ok_begin()

        for artist in client.list("artist"):
            for album in client.list("album", "artist", artist):
                for song in client.find("artist", artist, "album", album):
                    for k, v in song.iteritems():
                        print k + " " + v







    #    results = client.command_list_end()




        return Label(text='Hello world')


if __name__=='__main__':
    KivyMpd().run()