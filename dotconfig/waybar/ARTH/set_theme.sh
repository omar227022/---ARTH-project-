#!/bin/bash
# طريقة الاستخدام: ./set_theme.sh path/to/image.png (أو mp4/gif)

IMG="$1"
CACHE_IMG="$HOME/.cache/current_wallpaper.jpg"

if [ -z "$IMG" ]; then echo "Usage: set_theme.sh <path_to_wallpaper>"; exit 1; fi

# تشغيل swww إذا كان طافي
if ! pgrep -x swww-daemon > /dev/null; then
    swww init
fi

# 1. التعامل مع الفيديو والـ GIF لاستخراج لون ثابت
EXT="${IMG##*.}"
if [[ "$EXT" == "mp4" || "$EXT" == "gif" ]]; then
    # خذ لقطة للشاشة الأولى عشان نستخرج منها الألوان
    ffmpeg -y -i "$IMG" -vframes 1 -f image2 "$CACHE_IMG" > /dev/null 2>&1
    USE_IMG="$CACHE_IMG"
else
    USE_IMG="$IMG"
fi

# 2. توليد الألوان باستخدام Pywal
wal -i "$USE_IMG" -n -q

# 3. تغيير الخلفية (يدعم المتحرك)
swww img "$IMG" --transition-type grow --transition-pos 0.9,0.9 --transition-step 90

# 4. إعادة تشغيل Waybar ليأخذ الألوان الجديدة
pkill waybar
sleep 0.5
waybar -c ~/.config/waybar/ARTH/config.jsonc -s ~/.config/waybar/ARTH/style.css &

# إشعار
notify-send "ARTH Theme" "تم تغيير الخلفية وتحديث الألوان بنجاح!"
