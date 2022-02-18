#!/bin/bash
FILENAME="requirements.txt"
for pkg in "$@"; do
    pip3 install "$pkg"
    NAME="$(pip3 show "$pkg" | grep -w Name: | awk '{print $2}' | tail -n 1)";
    VERSION="$(pip3 show "$pkg" | grep -w Version: | awk '{print $2}' | tail -n 1)";

    if [ ! -z "$(grep "^$NAME=" $FILENAME)" ]; then echo "PACKAGE ALREADY EXISTS in "; exit 1; fi
    if [ ! -d $NAME ]; then
        echo $NAME==$VERSION >> $FILENAME;
    fi
done
sort -t= $FILENAME -o $FILENAME
