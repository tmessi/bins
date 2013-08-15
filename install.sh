#!/bin/env bash

pushd $(dirname $0) &> /dev/null

mkdir -p "$HOME/bin/"

for bin in $(ls); do
    if [ ! $bin == "README.rst" -a ! $bin == "install.sh" ]; then
        target="$HOME/bin/$dot"

        # Make a .bak of a file or dir
        if [ ! -h $target ]; then
            if [ -d $target -o -f $target ]; then
                mv $target $target.bak
            fi
        fi

        echo "Setting $dot"
        ln -sf "$PWD/$dot" "$target"
    fi
done

popd &> /dev/null
