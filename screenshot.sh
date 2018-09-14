#!/usr/bin/env bash

name=${0##*/}

function print_help() {
    echo "usage: $name <mode>

mode:
    full          capture the full screen
    window        capture the window that is clicked or an area if you click and drag

optional args:
    -c|--clipboard place the image on the clipboard instead of a file
    -h|--help     print this help."
}

OPTS=$(getopt -o h,c --long help,clipboard -n "$name" -- "$@")

# create dir for screenshots
mkdir -p ~/screenshots
scrot_opt="-m"
clipboard=0

if [[ $? != 0 ]]; then echo "option error" >&2; exit 1; fi

eval set -- "$OPTS"

while true; do
    case "$1" in
        -h|--help)
            print_help
            exit 0
            ;;
        -c|--clipboard)
            clipboard=1
            shift
            ;;
        --)
            shift; break;;
        *)
            echo "Internal error!"; exit 1;;
    esac
done

if [[ $# -eq 1 ]]; then
    case $1 in
    full)
        scrot_opt="-m"
        ;;
    window)
        sleep 1
        scrot_opt="-s"
        ;;
    *)
        echo "Invalid option"
        print_help
        exit -1
        ;;
    esac;

    if [[ $clipboard -eq 1 ]]; then
        scrot $scrot_opt /tmp/screenshot.png && xclip -selection clipboard -t image/png -i /tmp/screenshot.png
        rm -f /tmp/screenshot.png
    else
        scrot $scrot_opt '%Y-%m-%d-%H%M%S_$wx$h.png' -e 'mv $f ~/screenshots'
    fi
else
    echo "Need a mode"
    print_help
    exit -1
fi
