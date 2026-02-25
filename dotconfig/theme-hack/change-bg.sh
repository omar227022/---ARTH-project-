#!/bin/bash
IMG=$(find ~/Pictures/Wallpapers ~/Downloads/Images ~/Desktop/Backgrounds -type f \( -name "*.jpg" -o -name "*.png" \) | shuf -n 1)
wal -i "$IMG"
pkill waybar; waybar -c ~/.config/theme-hack/config.jsonc -s ~/.config/theme-hack/style.css &
swaync-client -t -swb
