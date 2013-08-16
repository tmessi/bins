#!/usr/bin/env python2
'''
A simple script to get the playback status of spotify.

This script needs ``dbus-python`` for spotify communication

To run simply::

    ./spotify-monitor.py <command>

Where command is one of the following::

    ``playback``
    ``playing``
'''

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import sys

def get_status(command):
    '''
    Get the status.

    command
        The command to query spofity with.

    Returns the status from spotify.
    '''
    try:
        bus_loop = DBusGMainLoop(set_as_default=True)
        session_bus = dbus.SessionBus(mainloop=bus_loop)
        spotify_bus = session_bus.get_object('org.mpris.MediaPlayer2.spotify',
                                             '/org/mpris/MediaPlayer2')
        spotify = dbus.Interface(spotify_bus,
                                 'org.freedesktop.DBus.Properties')
        if command == 'playback':
            res = spotify.Get('org.mpris.MediaPlayer2.Player',
                              'PlaybackStatus')
        elif command == 'playing':
            meta = spotify.Get('org.mpris.MediaPlayer2.Player',
                               'Metadata')
            artist = meta['xesam:artist'][0].encode('utf-8')
            title = meta['xesam:title'].encode('utf-8')
            res = '{0} - {1}'.format(title, artist)
    except Exception as e:
        res = 'Not Playing'
    return res

def main(arg):
    '''
    Pass the arg to spotify.
    '''
    if arg in ('playback', 'playing'):
        # First try sending command to Spotify
        res = get_status(arg)
        print res

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        exit(101)
