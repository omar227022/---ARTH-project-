#!/bin/bash
# عدل هذا المسار لمجلد خلفياتك الحقيقي
DIR="$HOME/Pictures"
if [ ! -d "$DIR" ]; then mkdir -p "$DIR"; fi
CHOICE=$(ls "$DIR" | rofi -dmenu -p "اختر خلفية" -theme-str "window {location: west; anchor: west; x-offset: 55px; width: 250px; height: 400px; border: 2px; border-radius: 15px; border-color: white;}")
if [ -n "$CHOICE" ]; then
    wal -i "$DIR/$CHOICE"
    pkill waybar; waybar -c ~/.config/theme-hack/config.jsonc -s ~/.config/theme-hack/style.css &
    swaync-client -rs
fi
