#!/usr/bin/env python3
'''
A simple script for passing commands to various media players.

This script needs ``dbus-python`` for spotify communication.

To run simply::

    ./mediakeys.py <command>

Where command is one of the following::

    ``toggle``
    ``stop``
    ``next``
    ``previous``
'''

# pylint: disable=W0703

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import sys
import subprocess


def send_pandora(command):
    '''
    Send the command to pithos using dbus interface.
    '''
    try:
        bus = dbus.SessionBus()
        pithos_object = bus.get_object("net.kevinmehall.Pithos",
                                       "/net/kevinmehall/Pithos")
        pithos = dbus.Interface(pithos_object, "net.kevinmehall.Pithos")
        if command == 'toggle':
            pithos.PlayPause()
        elif command == 'stop':
            pithos.Stop()
        elif command == 'next':
            pithos.SkipSong()
        return True
    except dbus.exceptions.DBusException:
        return False


def send_spotify(command):
    '''
    Send the command to spotify using dbus iterface.
    '''
    try:
        bus_loop = DBusGMainLoop(set_as_default=True)
        session_bus = dbus.SessionBus(mainloop=bus_loop)
        spotify_bus = session_bus.get_object('org.mpris.MediaPlayer2.spotify',
                                             '/org/mpris/MediaPlayer2')
        spotify = dbus.Interface(spotify_bus, 'org.mpris.MediaPlayer2.Player')
        if command == 'toggle':
            spotify.PlayPause()
        elif command == 'stop':
            spotify.Stop()
        elif command == 'next':
            spotify.Next()
        elif command == 'prev':
            spotify.Previous()
        return True
    except Exception:
        return False


def send_ncmpcpp(command):
    '''
    Pass the command to ncmpcpp using a subprocess.
    '''
    if command == 'prev':
        cmd = 'mpc repeat off && mpc {} && mpc repeat on'
    else:
        cmd = 'mpc {}'

    cmd = cmd.format(command)
    kwargs = {'shell': True}
    proc = subprocess.Popen(cmd, **kwargs)
    proc.communicate()
    if proc.returncode == 0:
        return True
    return False


def main(arg):
    '''
    Pass the arg to media players.
    '''
    if arg in ('toggle', 'stop', 'next', 'prev'):
        # First try sending command to Spotify, then ncmpcpp
        return send_pandora(arg) or send_spotify(arg) or send_ncmpcpp(arg)
    return False


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if main(sys.argv[1]):
            exit(0)
        else:
            exit(100)
    else:
        exit(101)
