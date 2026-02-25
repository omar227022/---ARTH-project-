#!/bin/bash

# 1. طف الـ Waybar عشان نجدد الألوان
pkill waybar

# 2. انتظر ثانية بسيطة عشان نضمن إن الخلفية الجديدة "ثبتت"
sleep 1

# 3. صيد المسار الحقيقي للخلفية (سواء كانت صورة أو فيديو)
CURRENT_WALL=$(swww query | grep -oP 'image: \K.*' | head -n 1)

# إذا ما لقى شي، يطلع عشان ما يحوس الدنيا
if [ -z "$CURRENT_WALL" ]; then
    notify-send "ARTH Bar" "ما لقيت خلفية شغالة يا عمر! 🧐"
    exit 1
fi

echo "🖼️ قاعد أحلل ألوان: $CURRENT_WALL"

# 4. معالجة الخلفية (متحركة أو ثابتة)
EXT="${CURRENT_WALL##*.}"
CACHE_DIR="$HOME/.cache/wal"
mkdir -p "$CACHE_DIR"
SNAP_IMG="$CACHE_DIR/current_snap.jpg"

if [[ "$EXT" == "mp4" || "$EXT" == "gif" || "$EXT" == "webm" ]]; then
    # إذا كانت متحركة، ناخذ لقطة من أول ثانية
    ffmpeg -y -i "$CURRENT_WALL" -vframes 1 "$SNAP_IMG" > /dev/null 2>&1
    wal -i "$SNAP_IMG" -n -q
else
    # إذا صورة عادية، نستخدمها مباشرة
    wal -i "$CURRENT_WALL" -n -q
fi

# 5. شغل الـ Waybar بالإعدادات حقتك
waybar -c ~/.config/waybar/ARTH/config.jsonc -s ~/.config/waybar/ARTH/style.css &

notify-send "ARTH System" "تم تحديث الألوان بناءً على الخلفية المتحركة! 🎥✨"
