#!/bin/bash

# تنسيق القوائم
ROFI_CMD="rofi -dmenu -i -p 'القائمة' -theme-str 'window { width: 65%; height: 75%; border: 4px; border-radius: 20px; } listview { columns: 2; lines: 10; } element { padding: 25px; } element-text { size: 35px; font: \"Sans Bold 22\"; }'"

# تنسيق الصور
ROFI_IMG="rofi -dmenu -i -p 'الخلفيات' -show-icons -theme-str 'window { width: 98%; height: 95%; border-radius: 20px; } listview { columns: 6; lines: 5; spacing: 15px; } element { orientation: vertical; padding: 10px; } element-icon { size: 280px; horizontal-align: 0.5; } element-text { horizontal-align: 0.5; }'"

MAIN_CHOICE=$(echo -e "الاعدادات\nالثيمات\nالاختصارات\nخيارات الطاقة" | eval $ROFI_CMD)

case $MAIN_CHOICE in
"الاعدادات")
    SET_CHOICE=$(echo -e "الشبكة\nالبلوتوث\nالصوت\nخيارات النوافذ (ON/OFF)\nإعدادات هايبر لاند" | eval $ROFI_CMD)
    case $SET_CHOICE in
        "خيارات النوافذ (ON/OFF)")
            CONF_FILE="$HOME/.config/hypr/hyprland.conf"
            STATUS=$(sed -n '/hyprbars {/,/}/p' "$CONF_FILE" | grep "enabled =" | awk '{print $3}')
            if [ "$STATUS" == "yes" ]; then
                sed -i '/hyprbars {/,/}/s/enabled = yes/enabled = no/' "$CONF_FILE"
                hyprctl reload
                notify-send "النوافذ" "تم إيقاف خيارات النوافذ"
            else
                sed -i '/hyprbars {/,/}/s/enabled = no/enabled = yes/' "$CONF_FILE"
                hyprctl reload
                notify-send "النوافذ" "تم تفعيل خيارات النوافذ"
            fi ;;
        "الشبكة") kitty nmtui ;;
        "البلوتوث") blueman-manager ;;
        "الصوت") pavucontrol ;;
        "إعدادات هايبر لاند") kitty nano "$HOME/.config/hypr/hyprland.conf" ;;
    esac ;;

"الثيمات")
    SUB_THEME=$(echo -e "الخلفيات\nستايل وايبار" | eval $ROFI_CMD)
    case $SUB_THEME in
        "الخلفيات")
            # اختيار المجلد
            BG_CHOICE=$(echo -e "خلفيات Simple\nخلفيات 2000s" | eval $ROFI_CMD)
            
            if [[ "$BG_CHOICE" == "خلفيات Simple" ]]; then 
                DIR="$HOME/simple"
            elif [[ "$BG_CHOICE" == "خلفيات 2000s" ]]; then
                DIR="$HOME/2000s wallpapers"
            else
                exit 1
            fi

            # التأكد من وجود المجلد
            if [ ! -d "$DIR" ]; then notify-send "خطأ" "المجلد مهوب فيه!"; exit 1; fi

            # عرض الصور بالطريقة المباشرة (بدون متغيرات تخرب الكود)
            SELECTED=$( find "$DIR" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.jpeg" -o -iname "*.webp" \) | while read -r file; do
                filename=$(basename "$file")
                echo -en "$filename\0icon\x1f$file\n"
            done | eval $ROFI_IMG )

            # تطبيق الخلفية
            if [[ -n "$SELECTED" ]]; then
                swww img "$DIR/$SELECTED" --transition-type grow
                wal -q -i "$DIR/$SELECTED"
            fi ;;
            
        "ستايل وايبار")
            WB_TYPE=$(echo -e "البسيط\n2000s Style" | eval $ROFI_CMD)
            pkill waybar; sleep 0.5
            [[ "$WB_TYPE" == "البسيط" ]] && waybar & 
            [[ "$WB_TYPE" == "2000s Style" ]] && waybar -c ~/.config/waybar/themes/2000s-style/config -s ~/.config/waybar/themes/2000s-style/style.css & ;;
    esac ;;

"الاختصارات")
    echo -e "󰖭 Super + Q : قفل النافذة\n󰆍 Super + T : التيرمينال\n󰘔 Super + V : وضع العوم\n󰑐 Super + M : ريلود للسيستم\n󰒓 Super + Shift + A : الإعدادات\n󰈹 Super + Shift + Z : هاكر شو\n󰍛 Super + Mouse_L : أمسك الصفحة وحركها" | rofi -dmenu -i -p "الاختصارات" -theme-str 'window { width: 50%; }' ;;

"خيارات الطاقة")
    POWER_CHOICE=$(echo -e "أداء عالي\nمتوازن\nتوفير طاقة\nتسجيل خروج\nإعادة تشغيل\nإيقاف التشغيل" | eval $ROFI_CMD)
    case $POWER_CHOICE in
        "أداء عالي") powerprofilesctl set performance ;;
        "متوازن") powerprofilesctl set balanced ;;
        "توفير طاقة") powerprofilesctl set power-saver ;;
        *)  CONFIRM=$(echo -e "إيه والله\nلا يا خوي" | rofi -dmenu -i -p "متأكد؟")
            [[ "$CONFIRM" == "إيه والله" ]] && { [[ "$POWER_CHOICE" == "تسجيل خروج" ]] && hyprctl dispatch exit; [[ "$POWER_CHOICE" == "إعادة تشغيل" ]] && systemctl reboot; [[ "$POWER_CHOICE" == "إيقاف التشغيل" ]] && systemctl poweroff; } ;;
    esac ;;
esac

