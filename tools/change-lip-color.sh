#!/bin/bash
colors="black\npink\nred\nblue\ntransparent\nrainbow"
newcolor="$(echo -en $colors | dmenu -b -i -l 15 -fn 'Source Code Pro:style=Regular')"

echo "Changing lip color to - $newcolor"
curl -H "Content-Type: application/json" -X POST --data "{\"lip_color\":\"$newcolor\"}" http://127.0.0.1:9987/
