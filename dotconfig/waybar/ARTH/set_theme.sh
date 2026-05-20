#!/bin/bash


IMG="$1"
CACHE_IMG="$HOME/.cache/current_wallpaper.jpg"

if [ -z "$IMG" ]; then echo "Usage: set_theme.sh <path_to_wallpaper>"; exit 1; fi

if ! pgrep -x swww-daemon > /dev/null; then
    swww init
fi

EXT="${IMG##*.}"
if [[ "$EXT" == "mp4" || "$EXT" == "gif" ]]; then
    ffmpeg -y -i "$IMG" -vframes 1 -f image2 "$CACHE_IMG" > /dev/null 2>&1
    USE_IMG="$CACHE_IMG"
else
    USE_IMG="$IMG"
fi

wal -i "$USE_IMG" -n -q

swww img "$IMG" --transition-type grow --transition-pos 0.9,0.9 --transition-step 90

pkill waybar
sleep 0.5
waybar -c ~/.config/waybar/ARTH/config.jsonc -s ~/.config/waybar/ARTH/style.css &

notify-send "ARTH Theme" "تم تغيير الخلفية وتحديث الألوان بنجاح!"
