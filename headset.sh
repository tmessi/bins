#!/bin/bash
grep -A4 -ri 'Headphone Playback Switch' /proc/asound/card0/codec#0 | grep "Amp-Out vals.*0x00 0x00" -q && echo 'headphones'
