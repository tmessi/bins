#!/usr/bin/env bash

name=${0##*/}

function print_help() {
    echo "usage: $name <mode>

mode:
    full          capture the full screen
    window        capture the window that is clicked on

optional args:
    -h|--help     print this help."
}

OPTS=$(getopt -o h --long help -n "$name" -- "$@")

if [ $? != 0 ]; then echo "option error" >&2; exit 1; fi

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

if [ $# -eq 1 ]; then
	case $1 in
	full)
		scrot -m
		;;
	window)
		sleep 1
		scrot -s
		;;
	*)
        echo "Invalid option"
        print_help
        exit -1
		;;
	esac;
else
    echo "Need a mode"
    print_help
    exit -1
fi
