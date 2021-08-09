#!/usr/bin/env python3
'''
Simple script to adjust volume with pulseaudio via ``pacmd``

This script needs ``pacmd`` installed (normally part of pulseaudio).

To run simply::

    ./soundkeys.py <command>

Where command is one of the following::

    ``raise``
    ``lower``
    ``toggle``
    ``volume``
'''
import subprocess
import sys

# The amount to increase/decrease the volume
VOL_STEP = int('0x01000', 0)
# The max volume
MAX_VOL = int('0x10000', 0)
# The min volume
MIN_VOL = int('0x00000', 0)


def _get_def(t='sink'):
    '''
    Get the default/fallback sink/source name
    '''
    cmd = 'pacmd dump | grep "^set-default-{}"'.format(t)
    out = cmdrun(cmd)['stdout']
    default = out.split()[1]
    return default


def cmdrun(cmd):
    '''
    Wrapper to run a subprocess command and return the result.

    cmd
        The command to run.

    Returns a dict with the following::

        {'stdout': stdout,
         'stderr': stderr,
         'pid': pid,
         'retcode': return_code}
    '''
    ret = dict()
    kwargs = {'shell': True,
              'stdout': subprocess.PIPE,
              'stderr': subprocess.PIPE}
    proc = subprocess.Popen(cmd, **kwargs)
    out, err = proc.communicate()

    ret['stdout'] = out.decode()
    ret['stderr'] = err.decode()
    ret['pid'] = proc.pid
    ret['retcode'] = proc.returncode
    return ret


def muted(t='sink'):
    '''
    Check if the audio is muted.

    Return ``true`` if muted, ``false`` if not.
    '''
    default = _get_def(t)
    cmd = 'pacmd dump | grep "^set-{}-mute {}"'.format(t, default)
    out = cmdrun(cmd)['stdout']
    state = out.split()[2]
    if state == 'yes':
        return True
    # else
    return False


def get_vol(t='sink'):
    '''
    Get the current volume.

    Return the current volume value.
    '''
    default = _get_def(t)
    cmd = 'pacmd dump | grep "^set-{}-volume {}"'.format(t, default)
    out = cmdrun(cmd)['stdout']
    vol = out.split()[2]
    return int(vol, 0)


def inc_vol():
    '''
    Get the increased volume level.

    Return the new volume in hex.
    '''
    new_vol = get_vol() + VOL_STEP
    if new_vol > MAX_VOL:
        new_vol = MAX_VOL
    return hex(new_vol)


def dec_vol():
    '''
    Get the decreased volumn level

    Return the new volume in hex
    '''
    new_vol = get_vol() - VOL_STEP
    if new_vol < MIN_VOL:
        new_vol = MIN_VOL
    return hex(new_vol)


def vol_percent(t="sink"):
    '''
    Get current volume as a percentage
    '''
    if muted(t):
        print('0')
    else:
        percent = int(get_vol(t) / float(MAX_VOL) * 100)
        print(percent)

def main(arg):
    '''
    Run the command
    '''
    if arg in ('raise', 'lower', 'toggle'):
        sink_name = _get_def('sink')
        cmd = 'pactl {} {} {}'
        if arg == 'toggle':
            if muted('sink'):
                cmd = cmd.format('set-sink-mute', sink_name, 0)
            else:
                cmd = cmd.format('set-sink-mute', sink_name, 1)
        elif arg == 'raise':
            new_vol = inc_vol()
            cmd = cmd.format('set-sink-volume', sink_name, new_vol)
        elif arg == 'lower':
            new_vol = dec_vol()
            cmd = cmd.format('set-sink-volume', sink_name, new_vol)
        if cmdrun(cmd)['retcode'] == 0:
            return True
    elif arg in ('mic-raise', 'mic-lower', 'mic-toggle'):
        source_name = _get_def('source')
        cmd = 'pactl {} {} {}'
        if arg == 'mic-toggle':
            if muted('source'):
                cmd = cmd.format('set-source-mute', source_name, 0)
            else:
                cmd = cmd.format('set-source-mute', source_name, 1)
        elif arg == 'mic-raise':
            new_vol = inc_vol()
            cmd = cmd.format('set-source-volume', source_name, new_vol)
        elif arg == 'mic-lower':
            new_vol = dec_vol()
            cmd = cmd.format('set-source-volume', source_name, new_vol)
        print(cmd)
        if cmdrun(cmd)['retcode'] == 0:
            return True
    elif arg == 'volume':
        vol_percent()
        return True
    elif arg == 'mic-volume':
        vol_percent("source")
    return False


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if main(sys.argv[1]):
            exit(0)
        else:
            exit(100)
    else:
        exit(101)
