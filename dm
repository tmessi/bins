#!/usr/bin/env bash

name=${0##*/}

function print_help() {
    echo "usage: $name <theme>

mode:
    light good for being in the sun
    dark  normal mode

    -h|--help     print this help."
}

OPTS=$(getopt -o h --long help -n "$name" -- "$@")

want=

if [[ $? != 0 ]]; then echo "option error" >&2; exit 1; fi

eval set -- "$OPTS"

while true; do
    case "$1" in
        -h|--help)
            print_help
            exit 0
            ;;
        --)
            shift; break;;
        *)
            echo "Internal error!"; exit 1;;
    esac
done

if [[ $# -ne 1 ]]; then
    echo "Need a theme"
    print_help
    exit -1
fi

case "$1" in
    light|dark)
        want=$1
        ;;
    toggle)
        grep dark ~/.xsettingsd &> /dev/null
        is_dark=$?
        if [[ $is_dark -eq 0 ]]; then
            want=light
        else
            want=dark
        fi
        ;;
    *)
        echo "Invalid option"
        print_help
        exit -1
        ;;
esac

# now set some things

## xsettings for gtk
if [[ -f ~/.xsettingsd ]]; then
    grep dark ~/.xsettingsd &> /dev/null
    is_dark=$?
    if [[ $is_dark -eq 0 && $want == "light" ]]; then
        sed -i 's/Adwaita-dark/Adwaita/' ~/.xsettingsd
    elif [[ $is_dark -eq 1 && $want == "dark" ]]; then
        sed -i 's/Adwaita/Adwaita-dark/' ~/.xsettingsd
    fi
    killall -HUP xsettingsd
fi

# alacritty terminals
if [[ -f ~/.alacritty.toml ]]; then
    grep dark ~/.alacritty.toml &> /dev/null
    is_dark=$?
    if [[ $is_dark -eq 0 && $want == "light" ]]; then
        sed -i 's/gruvbox_dark/gruvbox_light/' ~/.alacritty.toml
    elif [[ $is_dark -eq 1 && $want == "dark" ]]; then
        sed -i 's/gruvbox_light/gruvbox_dark/' ~/.alacritty.toml
    fi
fi
