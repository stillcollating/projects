
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


        albums = []

        for sAlbum in client.list("album"):
            album = dict()
            album['name'] = sAlbum
            artists = client.list("artist", "album", sAlbum)
            if len(artists) == 1:
                album['artist'] = artists[0]
            elif len(artists) > 1:
                album['artist'] = "VA"
            elif len(artists) == 0:
                album['artist'] = "Unknown"
            albums.append(album)

        for x in albums:
            print x['artist'] + " - " + x['name']


    #    results = client.command_list_end()




        return Label(text='Hello world')


if __name__=='__main__':
    KivyMpd().run()