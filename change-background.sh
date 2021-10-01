#!/bin/bash
dirpath="/home/jm/git/CoolGuy.exe/fakecam"
newfile="$(ls -l $dirpath/backgrounds | awk '/[.jpg|.gif]/{print $9}' | dmenu -b -i -l 4 -fn 'Source Code Pro:style=Regular')"

[[ -e "$dirpath/backgrounds/$newfile" ]] || exit 1
echo "Changing backgrounds to - $newfile"
curl -H "Content-Type: application/json" -X POST --data "{\"filename\":\"$newfile\"}" http://127.0.0.1:5000/
