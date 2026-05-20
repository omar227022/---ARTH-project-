import sys
import os
import subprocess
import shutil
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QSlider, QStackedWidget, 
                             QFrame, QGridLayout, QColorDialog, QScrollArea, QTabWidget, QToolButton, QCheckBox, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QColor, QCursor

HOME = os.path.expanduser("~")

REPO_DIR = os.path.join(HOME, ".arth_repo_cache")
WALL_BASE = os.path.join(REPO_DIR, "wallpapers")

USER_FALLUP = os.path.join(WALL_BASE, "fallup")
VIDEO_DIR = os.path.join(WALL_BASE, "wallpapers mp4")
SIMPLE_DIR = os.path.join(WALL_BASE, "simple")
WALL2000_DIR = os.path.join(WALL_BASE, "2000s wallpapers")
ARTH_WALL_DIR = os.path.join(WALL_BASE, "ARTH Wallpaper")
CYBER_DIR = os.path.join(WALL_BASE, "cyber")

FALLUP_CONF = os.path.join(HOME, ".config/waybar/themes/fallup")
ARTH_CONF = os.path.join(HOME, ".config/waybar/ARTH")
SIMPLE_BAR_CONF = os.path.join(HOME, ".config/waybar/simple") 

FF_THEMES = os.path.join(HOME, ".config/fastfetch/themes")
CACHE_DIR = os.path.join(HOME, ".cache/arth_settings")

ANIM_CONF_FILE = os.path.join(HOME, ".config/hypr/animations.conf")

LAST_BAR_FILE = os.path.join(CACHE_DIR, "last_waybar_type")
ADAPT_FILE = os.path.join(CACHE_DIR, "border_adapt_mode")
WAYBAR_ADAPT_FILE = os.path.join(CACHE_DIR, "waybar_adapt_mode")

def check_and_install_dependencies():
    packages = {
        "waybar": "waybar",
        "hyprctl": "hyprland",
        "wal": "python-pywal",
        "swww": "swww",
        "mpvpaper": "mpvpaper",
        "fastfetch": "fastfetch",
        "kitty": "kitty",
        "playerctl": "playerctl"
    }
    
    missing_cmds = [cmd for cmd in packages.keys() if shutil.which(cmd) is None]
    
    if missing_cmds:
        missing_pkgs = [packages[cmd] for cmd in missing_cmds]
        print("\n" + "="*50)
        print("فيه حزم ناقصة لتشغيل ARTH OS، جاري التثبيت...")
        print("="*50 + "\n")
        
        try:
            if shutil.which("paru"):
                subprocess.run(["paru", "-S", "--noconfirm"] + missing_pkgs)
            elif shutil.which("yay"):
                subprocess.run(["yay", "-S", "--noconfirm"] + missing_pkgs)
            else:
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm"] + missing_pkgs)
        except Exception as e:
            print(f"فشل التثبيت التلقائي: {e}")

def setup_repo():
    if not os.path.exists(REPO_DIR):
        print("\n" + "="*50)
        print("اصبر شوي قاعد يحمل الخلفيات من القيت هوب | مع تحيات ارث - ARTH")
        print("="*50 + "\n")
        subprocess.run(["git", "clone", "https://github.com/omar227022/---ARTH-project-.git", REPO_DIR])

def setup_waybar_colors():
    wal_file = os.path.join(HOME, ".cache/wal/colors-waybar.css")
    if not os.path.exists(wal_file):
        return

    theme_dirs = [
        os.path.join(HOME, ".config/waybar"),
        os.path.join(HOME, ".config/waybar/themes"),
        os.path.join(HOME, ".config/waybar/ARTH"),
        os.path.join(HOME, ".config/theme-hack"),
    ]

    for base in theme_dirs:
        if not os.path.exists(base):
            continue

        for root, dirs, files in os.walk(base):
            if "style.css" in files:
                colors_path = os.path.join(root, "colors.css")
                style_file = os.path.join(root, "style.css")
                try:
                    if os.path.exists(colors_path) or os.path.islink(colors_path):
                        os.remove(colors_path)
                    os.symlink(wal_file, colors_path)

                    with open(style_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    if '@import "colors.css";' not in content:
                        lines = [line for line in content.splitlines() if "colors-waybar.css" not in line and "colors.css" not in line]
                        lines.insert(0, '@import "colors.css";')
                        with open(style_file, "w", encoding="utf-8") as f:
                            f.write("\n".join(lines))
                except Exception:
                    pass

class ArthDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arth OS Control Center")
        self.setFixedSize(1100, 750) 
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.current_anim_template = "bezier = bouncy, 0.4, 0.0, 0.2, 1.4\nanimation = windows, 1, {spd}, bouncy, popin 80%\nanimation = workspaces, 1, {spd}, bouncy, slide"
        self.is_anim_enabled = True

        self.central_widget = QWidget()
        self.central_widget.setObjectName("MainFrame")
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(250)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        title = QLabel("ARTH OS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("AppTitle")
        self.sidebar_layout.addWidget(title)

        self.add_nav_btn("معرض الخلفيات", 0)
        self.add_nav_btn("ستايل البار", 1)
        self.add_nav_btn("الحدود والشفافية", 2)
        self.add_nav_btn("أنميشن النظام", 3)
        self.add_nav_btn("إعدادات الفاست فاتش", 4)
        self.add_nav_btn("النظام والطاقة", 5)
        self.sidebar_layout.addStretch()
        exit_btn = QPushButton("إغلاق")
        exit_btn.setObjectName("ExitBtn")
        exit_btn.clicked.connect(self.close)
        self.sidebar_layout.addWidget(exit_btn)

        self.pages = QStackedWidget()
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.pages)

        self.init_wallpaper_page() 
        self.init_waybar_page() 
        self.init_border_blur_page()
        self.init_animation_page()
        self.init_fastfetch_page() 
        self.init_system_page() 

        self.setStyleSheet("""
            #MainFrame { background-color: rgba(10, 10, 20, 0.95); border-radius: 12px; border: 1px solid #3b82f6; }
            #Sidebar { background-color: rgba(5, 10, 25, 0.6); border-top-left-radius: 12px; border-bottom-left-radius: 12px; }
            #AppTitle { font-size: 26px; font-weight: 900; color: #3b82f6; margin: 20px 0; }
            QPushButton { background: transparent; color: #60a5fa; padding: 10px; text-align: left; font-size: 14px; border-radius: 6px; margin: 2px 10px; }
            QPushButton:hover { background-color: rgba(59, 130, 246, 0.15); color: #93c5fd; }
            QLabel { color: #60a5fa; }
            QTabWidget::pane { border: 0; }
            QTabBar::tab { background: #1e293b; color: #60a5fa; padding: 8px 15px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background: #1e3a8a; color: #93c5fd; border-bottom: 2px solid #3b82f6; }
            QScrollArea { border: none; background: transparent; }
            QCheckBox { color: #60a5fa; spacing: 5px; }
            QCheckBox::indicator { width: 18px; height: 18px; border: 1px solid #3b82f6; border-radius: 4px; }
            QCheckBox::indicator:checked { background-color: #3b82f6; }
            #ExitBtn { color: #ef4444; text-align: center; }
        """)

    def add_nav_btn(self, text, index):
        btn = QPushButton(text)
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.clicked.connect(lambda: self.pages.setCurrentIndex(index))
        self.sidebar_layout.addWidget(btn)

    def import_wallpaper_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "اختر مجلد الخلفيات", HOME)
        if folder_path:
            imported = 0
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    ext = file_name.lower().split('.')[-1]
                    if ext in ['mp4', 'gif', 'mkv']:
                        os.makedirs(VIDEO_DIR, exist_ok=True)
                        shutil.copy(file_path, VIDEO_DIR)
                        imported += 1
                    elif ext in ['png', 'jpg', 'jpeg']:
                        os.makedirs(ARTH_WALL_DIR, exist_ok=True)
                        shutil.copy(file_path, ARTH_WALL_DIR)
                        imported += 1
            
            if imported > 0:
                QMessageBox.information(self, "نجاح", f"تم استيراد {imported} خلفية من المجلد بنجاح. أعد تشغيل الأداة لتحديث المعرض.")
            else:
                QMessageBox.warning(self, "تنبيه", "المجلد اللي اخترته ما فيه خلفيات أو فيديوهات مدعومة!")

    def init_wallpaper_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        btn_import = QPushButton("إضافة مجلد خلفيات (MP4, GIF, PNG, JPG)")
        btn_import.setStyleSheet("background-color: #3b82f6; color: #0f172a; font-weight: bold; padding: 10px; margin-bottom: 10px; text-align: center;")
        btn_import.clicked.connect(self.import_wallpaper_folder)
        layout.addWidget(btn_import)

        tabs = QTabWidget()
        tabs.addTab(self.create_gallery(ARTH_WALL_DIR, "image"), "Arth")
        tabs.addTab(self.create_gallery(SIMPLE_DIR, "image"), "Simple")
        tabs.addTab(self.create_gallery(WALL2000_DIR, "image"), "2000s")
        tabs.addTab(self.create_gallery(USER_FALLUP, "image"), "Fallup")
        tabs.addTab(self.create_gallery(CYBER_DIR, "image"), "Cyber")
        tabs.addTab(self.create_gallery(VIDEO_DIR, "video"), "Live")
        layout.addWidget(tabs)
        self.pages.addWidget(page)

    def create_gallery(self, directory, mode):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(8)
        row, col = 0, 0
        if os.path.exists(directory):
            files = sorted(os.listdir(directory))
            for f in files:
                full_path = os.path.join(directory, f)
                if mode == "image" and not f.lower().endswith(('.png', '.jpg', '.jpeg')): continue
                if mode == "video" and not f.lower().endswith(('.mp4', '.gif', '.mkv')): continue
                btn = QToolButton()
                btn.setText(f[:10]) 
                btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
                btn.setFixedSize(130, 110)
                btn.setStyleSheet("QToolButton { background: #1e293b; border: 1px solid #334155; border-radius: 6px; color: #60a5fa; } QToolButton:hover { border-color: #3b82f6; color: #93c5fd; }")
                if mode == "image":
                    btn.setIcon(QIcon(full_path))
                    btn.setIconSize(QSize(100, 75))
                    btn.clicked.connect(lambda ch, p=full_path: self.apply_wallpaper(p, "image"))
                else: 
                    thumb = full_path.rsplit('.', 1)[0] + ".jpg"
                    if os.path.exists(thumb): btn.setIcon(QIcon(thumb))
                    else: btn.setIcon(QIcon.fromTheme("video-x-generic"))
                    btn.setIconSize(QSize(100, 75))
                    btn.clicked.connect(lambda ch, p=full_path: self.apply_wallpaper(p, "video"))
                grid.addWidget(btn, row, col)
                col += 1
                if col > 4: col = 0; row += 1
        container.setLayout(grid)
        scroll.setWidget(container)
        return scroll

    def apply_wallpaper(self, path, mode):
        if mode == "image":
            subprocess.run("pkill mpvpaper", shell=True)
            subprocess.run(f"swww img '{path}' --transition-type grow --transition-fps 120", shell=True)
            subprocess.run(f"wal -q -n -i '{path}'", shell=True)
        else:
            subprocess.run("pkill mpvpaper", shell=True)
            mpv_opts = "--no-audio --loop-playlist --ovfm=fps=30 --hwdec=auto"
            subprocess.Popen(f"mpvpaper -o '{mpv_opts}' '*' '{path}'", shell=True)
            thumb = path.rsplit('.', 1)[0] + ".jpg"
            if os.path.exists(thumb): subprocess.run(f"wal -q -n -i '{thumb}'", shell=True)
        self.check_adapt_border()
        if os.path.exists(WAYBAR_ADAPT_FILE) and open(WAYBAR_ADAPT_FILE).read().strip() == "true":
            self.reload_waybar_smart()

    def reload_waybar_smart(self):
        style = open(LAST_BAR_FILE, "r").read().strip() if os.path.exists(LAST_BAR_FILE) else "default"
        self.apply_waybar(style)

    def init_waybar_page(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(30,30,30,30)
        layout.addWidget(QLabel("ستايل البار:", styleSheet="font-size: 20px; color: #3b82f6;"))
        styles = [("Default", "default"), ("Fallup", "fallup"), ("2000s", "2000s"), ("Hack", "hack"), ("ARTH", "arth"), ("Cyber Bar", "cyber")]
        grid = QGridLayout()
        for i, (name, code) in enumerate(styles):
            btn = QPushButton(name)
            btn.setStyleSheet("background-color: #1e293b; border: 1px solid #334155; text-align: center; height: 50px;")
            btn.clicked.connect(lambda ch, c=code: self.apply_waybar(c))
            grid.addWidget(btn, i // 2, i % 2)
        layout.addLayout(grid)
        chk_adapt_bar = QCheckBox("تكييف ألوان الواي بار مع الخلفية تلقائياً")
        chk_adapt_bar.clicked.connect(lambda: self.toggle_waybar_adapt(chk_adapt_bar.isChecked()))
        if os.path.exists(WAYBAR_ADAPT_FILE) and open(WAYBAR_ADAPT_FILE).read().strip() == "true":
            chk_adapt_bar.setChecked(True)
        layout.addWidget(chk_adapt_bar)
        layout.addStretch(); self.pages.addWidget(page)

    def toggle_waybar_adapt(self, checked):
        with open(WAYBAR_ADAPT_FILE, "w") as f: f.write("true" if checked else "false")

    def apply_waybar(self, style_code):
        with open(LAST_BAR_FILE, "w") as f: f.write(style_code)
        subprocess.run(["pkill", "waybar"])
        cmd = "waybar &"
        if style_code == "fallup": cmd = f"waybar -c {FALLUP_CONF}/top.jsonc -s {FALLUP_CONF}/style.css & waybar -c {FALLUP_CONF}/bottom.jsonc -s {FALLUP_CONF}/style.css &"
        elif style_code == "2000s": cmd = f"waybar -c {HOME}/.config/waybar/themes/2000s-style/config -s {HOME}/.config/waybar/themes/2000s-style/style.css &"
        elif style_code == "hack": cmd = f"waybar -c {HOME}/.config/theme-hack/config.jsonc -s {HOME}/.config/theme-hack/style.css &"
        elif style_code == "arth": cmd = f"waybar -c {ARTH_CONF}/config.jsonc -s {ARTH_CONF}/style.css &"
        elif style_code == "cyber": cmd = f"waybar -c {HOME}/.config/waybar/themes/cyber-bar/config.jsonc -s {HOME}/.config/waybar/themes/cyber-bar/style.css &"
        subprocess.Popen(cmd, shell=True)
        self.check_adapt_border()

    def update_blur_and_passes(self, val):
        passes = max(1, val // 2)
        subprocess.run(f"hyprctl keyword decoration:blur:size {val}", shell=True)
        subprocess.run(f"hyprctl keyword decoration:blur:passes {passes}", shell=True)

    def init_border_blur_page(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(30,30,30,30)
        layout.addWidget(QLabel("الحدود والشفافية والبلور:", styleSheet="font-size: 18px; color: #3b82f6;"))
        
        layout.addWidget(QLabel("البلور"))
        s_blur = QSlider(Qt.Orientation.Horizontal); s_blur.setRange(0, 30); s_blur.setValue(5)
        s_blur.valueChanged.connect(self.update_blur_and_passes)
        layout.addWidget(s_blur)

        layout.addWidget(QLabel("تكبير حجم الحدود"))
        s_border_size = QSlider(Qt.Orientation.Horizontal)
        s_border_size.setRange(0, 30)
        s_border_size.setValue(2)
        s_border_size.valueChanged.connect(lambda v: subprocess.run(f"hyprctl keyword general:border_size {v}", shell=True))
        layout.addWidget(s_border_size)

        layout.addWidget(QLabel("تدوير الحواف"))
        s_round = QSlider(Qt.Orientation.Horizontal)
        s_round.setRange(0, 30)
        s_round.setValue(5)
        s_round.valueChanged.connect(lambda v: subprocess.run(f"hyprctl keyword decoration:rounding {v}", shell=True))
        layout.addWidget(s_round)

        layout.addWidget(QLabel("شفافية النظام"))
        s_trans = QSlider(Qt.Orientation.Horizontal); s_trans.setRange(1, 10); s_trans.setValue(10)
        s_trans.valueChanged.connect(self.set_transparency)
        layout.addWidget(s_trans)
        
        layout.addWidget(QLabel("تغميق كيتي"))
        s_kitty = QSlider(Qt.Orientation.Horizontal); s_kitty.setRange(0, 100); s_kitty.setValue(0)
        s_kitty.valueChanged.connect(self.set_kitty_darkness)
        layout.addWidget(s_kitty)

        layout.addWidget(QLabel("شفافية الحدود"))
        s_border = QSlider(Qt.Orientation.Horizontal); s_border.setRange(0, 100); s_border.setValue(100)
        s_border.valueChanged.connect(self.set_border_alpha)
        layout.addWidget(s_border)
        btn_border_col = QPushButton("تغيير لون الحدود")
        btn_border_col.setStyleSheet("background: #3b82f6; color: #0f172a; font-weight: bold; margin-top: 10px;")
        btn_border_col.clicked.connect(self.pick_border_color)
        layout.addWidget(btn_border_col)
        btn_adapt = QPushButton("تفعيل لون الحدود المتكيف")
        btn_adapt.setStyleSheet("background: #60a5fa; color: #0f172a; font-weight: bold;")
        btn_adapt.clicked.connect(self.enable_adapt)
        layout.addWidget(btn_adapt); layout.addStretch(); self.pages.addWidget(page)

    def set_kitty_darkness(self, val):
        dark_val = int(255 * (1 - val/100.0))
        color = f"#{dark_val:02x}{dark_val:02x}{dark_val:02x}"
        subprocess.run(f"kitty @ set-colors background='{color}'", shell=True)

    def init_animation_page(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(30,30,30,30)
        layout.addWidget(QLabel("إعدادات الأنميشن الحية (ARTH-8):", styleSheet="font-size: 20px; color: #3b82f6;"))
        
        self.anim_styles = {
            "ارتدادي": "bezier = bouncy, 0.4, 0.0, 0.2, 1.4\nanimation = windows, 1, {spd}, bouncy, popin 80%\nanimation = workspaces, 1, {spd}, bouncy, slide",
            "ناعم": "bezier = smooth, 0.25, 0.1, 0.25, 1.0\nanimation = windows, 1, {spd}, smooth\nanimation = workspaces, 1, {spd}, smooth, slide",
            "طلقة": "bezier = fast, 0.1, 0.9, 0.1, 1.05\nanimation = windows, 1, {spd}, fast, popin 80%\nanimation = workspaces, 1, {spd}, fast, slide",
            "خاطف": "bezier = snappy, 0.0, 0.85, 0.15, 1.0\nanimation = windows, 1, {spd}, snappy, slide\nanimation = workspaces, 1, {spd}, snappy, slide",
            "مطاطي": "bezier = elastic, 0.68, -0.55, 0.265, 1.55\nanimation = windows, 1, {spd}, elastic, popin\nanimation = workspaces, 1, {spd}, elastic, slide",
            "رايق": "bezier = lazy, 0.5, 0.0, 0.5, 1.0\nanimation = windows, 1, {spd}, lazy\nanimation = workspaces, 1, {spd}, lazy, slidevert",
            "انزلاقي": "bezier = gliding, 0.1, 1.0, 0.0, 1.0\nanimation = windows, 1, {spd}, gliding, slide\nanimation = workspaces, 1, {spd}, gliding, slide",
            "حماسي": "bezier = energetic, 0.175, 0.885, 0.32, 1.275\nanimation = windows, 1, {spd}, energetic, popin 70%\nanimation = workspaces, 1, {spd}, energetic, slide"
        }
        
        grid = QGridLayout()
        names = list(self.anim_styles.keys())
        for i, name in enumerate(names):
            btn = QPushButton(name)
            btn.setStyleSheet("background-color: #1e293b; border: 1px solid #334155; text-align: center; height: 50px;")
            btn.clicked.connect(lambda ch, n=name: self.set_anim_style(n))
            grid.addWidget(btn, i // 2, i % 2)
        layout.addLayout(grid)

        layout.addSpacing(20)
        layout.addWidget(QLabel("سرعة الأنميشن (كل ما قل الرقم زادت السرعة):"))
        self.spd_slider = QSlider(Qt.Orientation.Horizontal)
        self.spd_slider.setRange(1, 15)
        self.spd_slider.setValue(7)
        self.spd_slider.valueChanged.connect(self.apply_anim_changes)
        layout.addWidget(self.spd_slider)

        layout.addSpacing(20)
        self.toggle_anim_btn = QPushButton("إلغاء تفعيل الأنميشن")
        self.toggle_anim_btn.setStyleSheet("background-color: #ef4444; color: white; font-weight: bold; height: 45px;")
        self.toggle_anim_btn.clicked.connect(self.toggle_animation)
        layout.addWidget(self.toggle_anim_btn)

        layout.addStretch()
        self.pages.addWidget(page)

    def set_anim_style(self, name):
        self.current_anim_template = self.anim_styles[name]
        self.apply_anim_changes()

    def toggle_animation(self):
        self.is_anim_enabled = not self.is_anim_enabled
        if self.is_anim_enabled:
            self.toggle_anim_btn.setText("إلغاء تفعيل الأنميشن")
            self.toggle_anim_btn.setStyleSheet("background-color: #ef4444; color: white; font-weight: bold; height: 45px;")
        else:
            self.toggle_anim_btn.setText("تفعيل الأنميشن")
            self.toggle_anim_btn.setStyleSheet("background-color: #22c55e; color: white; font-weight: bold; height: 45px;")
        self.apply_anim_changes()

    def apply_anim_changes(self):
        spd = self.spd_slider.value()
        enabled_str = "yes" if self.is_anim_enabled else "no"
        final_content = f"animations {{\n    enabled = {enabled_str}\n"
        final_content += self.current_anim_template.format(spd=spd)
        final_content += "\n}"

        try:
            with open(ANIM_CONF_FILE, "w") as f:
                f.write(final_content)
        except: pass

        subprocess.run(f"hyprctl keyword animations:enabled {'1' if self.is_anim_enabled else '0'}", shell=True)
        if self.is_anim_enabled:
            lines = self.current_anim_template.format(spd=spd).split('\n')
            for line in lines:
                if line.strip() and "=" in line:
                    parts = line.split("=", 1)
                    key = parts[0].strip()
                    val = parts[1].strip()
                    subprocess.run(f"hyprctl keyword {key} '{val}'", shell=True)

    def set_border_alpha(self, val):
        alpha = hex(int(val * 2.55))[2:].zfill(2)
        subprocess.run(f"hyprctl keyword general:col.active_border 'rgba(3b82f6{alpha})'", shell=True)
        subprocess.run(f"hyprctl keyword general:col.inactive_border 'rgba(334155{alpha})'", shell=True)

    def set_transparency(self, value):
        opacity = value / 10.0
        subprocess.run(f"hyprctl keyword decoration:active_opacity {opacity}", shell=True)
        subprocess.run(f"hyprctl keyword decoration:inactive_opacity {opacity}", shell=True)

    def pick_border_color(self):
        col = QColorDialog.getColor()
        if col.isValid(): self.set_border_color(col.name())

    def set_border_color(self, hex_code):
        clean_hex = hex_code.replace("#", "")
        subprocess.run(f"hyprctl keyword general:col.active_border 'rgba({clean_hex}ff)'", shell=True)
        subprocess.run(f"hyprctl keyword general:col.inactive_border 'rgba({clean_hex}ff)'", shell=True)

    def enable_adapt(self):
        with open(ADAPT_FILE, "w") as f: f.write("true")
        self.check_adapt_border()

    def check_adapt_border(self):
        if os.path.exists(ADAPT_FILE) and open(ADAPT_FILE).read().strip() == "true":
            try:
                wal_color = subprocess.check_output("sed -n '2p' ~/.cache/wal/colors", shell=True).decode().strip()
                self.set_border_color(wal_color)
            except: pass

    def init_fastfetch_page(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(30,30,30,30)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); content = QWidget(); grid = QGridLayout(content)
        if os.path.exists(FF_THEMES):
            for i, t in enumerate([f for f in os.listdir(FF_THEMES) if f.endswith(".jsonc")]):
                btn = QPushButton(t.replace(".jsonc", "")); btn.clicked.connect(lambda ch, th=t: self.apply_ff(th))
                grid.addWidget(btn, i // 3, i % 3)
        scroll.setWidget(content); layout.addWidget(scroll); self.pages.addWidget(page)

    def apply_ff(self, theme):
        src = os.path.join(FF_THEMES, theme)
        dst = os.path.expanduser("~/.config/fastfetch/config.jsonc")
        subprocess.run(f"cp '{src}' '{dst}'", shell=True)
        subprocess.Popen("kitty --hold -e fastfetch", shell=True)

    def init_system_page(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(30,30,30,30)
        layout.addWidget(QLabel("وضع الأداء:"))
        perf_layout = QHBoxLayout()
        modes = [("اقتصادي", "power-saver"), ("متوازن", "balanced"), ("عالي", "performance")]
        for m_name, m_cmd in modes:
            btn_p = QPushButton(m_name)
            btn_p.clicked.connect(lambda ch, c=m_cmd: subprocess.run(f"powerprofilesctl set {c}", shell=True))
            perf_layout.addWidget(btn_p)
        layout.addLayout(perf_layout)
        layout.addSpacing(10)
        tools = [("الشبكة", "kitty nmtui"), ("الصوت", "pavucontrol"), ("Config", "kitty nano ~/.config/hypr/hyprland.conf")]
        for name, cmd in tools:
            b = QPushButton(name); b.clicked.connect(lambda ch, c=cmd: subprocess.Popen(c, shell=True))
            layout.addWidget(b)
        layout.addStretch()
        layout.addWidget(QLabel("خيارات الطاقة:"))
        power_layout = QHBoxLayout()
        opts = [("إيقاف التشغيل", "systemctl poweroff"), ("إعادة التشغيل", "systemctl reboot"), ("خروج الجلسة", "hyprctl dispatch exit")]
        for name, cmd in opts:
            btn_pw = QPushButton(name)
            btn_pw.setStyleSheet("background: #ef4444; color: white;")
            btn_pw.clicked.connect(lambda ch, n=name, c=cmd: self.confirm_action(n, c))
            power_layout.addWidget(btn_pw)
        layout.addLayout(power_layout)
        self.pages.addWidget(page)

    def confirm_action(self, name, cmd):
        reply = QMessageBox.question(self, 'تأكيد', f'متأكد تبي تسوي {name}؟', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes: subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(FF_THEMES, exist_ok=True)
    
    check_and_install_dependencies()
    setup_repo()
    setup_waybar_colors()
    
    app = QApplication(sys.argv)
    win = ArthDashboard()
    win.show()
    sys.exit(app.exec())
