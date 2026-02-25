#!/bin/bash

# تنظيف الشاشة
pkill cava; pkill cmatrix; pkill peaclock

# 1. الماتريكس (عشان النقاط السوداء صغرت الخط)
kitty -o font_size=9 --class matrix_win cmatrix -s &
sleep 0.2

# 2. الكافا
kitty --class cava_win cava &
sleep 0.2

# 3. الساعة
kitty --class clock_win peaclock &
sleep 0.2

# 4. القطار الفخم (بيفتح تيرمنال يمر فيه القطار ويقفل)
kitty --class sl_win sh -c "sl; sleep 1" &

