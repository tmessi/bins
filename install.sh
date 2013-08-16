#!/bin/env bash

name=${0##*/}

function print_help() {
    echo "usage: $name [options]

optional args:

    -p|--pretend  print what install will do without doing it.
    -h|--help     print this help."
}

pretend=0
OPTS=$(getopt -o ph --long pretend,help -n "$name" -- "$@")

if [ $? != 0 ]; then echo "option error" >&2; exit 1; fi

eval set -- "$OPTS"

while true; do
    case "$1" in
        -p|--pretend)
            pretend=1
            shift;;
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

pushd $(dirname $0) &> /dev/null

if [[ $pretend -eq 1 ]]; then
    echo "Would make dir '$HOME/bin/"
else
    mkdir -p "$HOME/bin/"
fi

for bin in $(ls); do
    if [ ! $bin == "README.rst" -a ! $bin == "install.sh" ]; then
        target="$HOME/bin/$dot"

        if [[ $pretend -eq 1 ]]; then
            echo "Would set $dot"
        else
            # Make a .bak of a file or dir
            if [ ! -h $target ]; then
                if [ -d $target -o -f $target ]; then
                    mv $target $target.bak
                fi
            fi

            echo "Setting $dot"
            ln -sf "$PWD/$dot" "$target"
        fi
    fi
done

popd &> /dev/null
