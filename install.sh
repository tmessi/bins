#!/usr/bin/env bash

name=${0##*/}

function print_help() {
    echo "usage: $name [options]

optional args:

    -p|--pretend  print what install will do without doing it.
    -h|--help     print this help."
}

pretend=0
OPTS=$(getopt -o ph --long pretend,help -n "$name" -- "$@")

if [[ $? != 0 ]]; then echo "option error" >&2; exit 1; fi

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
    if [[ ! $bin == "README.rst" ]] && [[ ! $bin == "install.sh" ]] && [[ ! $bin == "LICENSE"  ]] && [[ ! $bin == "mplayer.md" ]]; then
        target="$HOME/bin/$bin"

        if [[ $pretend -eq 1 ]]; then
            echo "Would set $bin"
        else
            # Make a .bak of a file or dir
            if [[ ! -h $target ]]; then
                if [[ -d $target ]] || [[ -f $target ]]; then
                    mv $target $target.bak
                fi
            fi

            echo "Setting $bin"
            ln -sf "$PWD/$bin" "$target"
        fi
    fi
done

if [[ $pretend -eq 1 ]]; then
    echo "Would remove the following broken links"
    find $HOME/bin -xtype l
else
    find $HOME/bin -xtype l -delete
fi

popd &> /dev/null
