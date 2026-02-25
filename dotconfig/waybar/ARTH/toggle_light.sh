#!/bin/bash
STATE_FILE="$HOME/.cache/arth_theme_state"

# اكتشاف الحالة الحالية
if [ ! -f "$STATE_FILE" ] || [ "$(cat $STATE_FILE)" == "dark" ]; then
    # تحويل للوضع الفاتح
    wal -i "$(swww query | grep -oP 'image: \K.*')" -l -n -q
    echo "light" > "$STATE_FILE"
else
    # تحويل للوضع الداكن
    wal -i "$(swww query | grep -oP 'image: \K.*')" -n -q
    echo "dark" > "$STATE_FILE"
fi

pkill -USR2 waybar # تحديث الوان وايبار بدون اعادة تشغيل كاملة
