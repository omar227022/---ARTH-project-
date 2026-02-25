#!/bin/bash
options="󰒮 السابق\n󰐊 تشغيل/إيقاف\n󰒭 التالي"
chosen=$(echo -e "$options" | rofi -dmenu -i -p "التحكم بالموسيقى" -theme-str "window {width: 200px; border: 2px; border-color: @color1;} listview {lines: 3;}")

case "$chosen" in
    *السابق) playerctl previous ;;
    *تشغيل/إيقاف) playerctl play-pause ;;
    *التالي) playerctl next ;;
esac
