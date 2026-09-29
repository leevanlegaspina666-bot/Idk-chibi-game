[app]

# ============================================================
# BASIC APP INFORMATION
# ============================================================

title = Chibi Shark Pet

package.name = chibisharkpet

package.domain = org.chibisharkpet

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,txt

source.exclude_exts = spec

source.exclude_dirs = .git,.github,bin,.buildozer,__pycache__

version = 1.0.0


# ============================================================
# REQUIREMENTS
# ============================================================

requirements = python3,kivy


# ============================================================
# SCREEN
# ============================================================

orientation = landscape

fullscreen = 1


# ============================================================
# ANDROID
# ============================================================

android.api = 35

android.minapi = 24

android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_license = True

android.allow_backup = True


# ============================================================
# ANDROID PERMISSIONS
# ============================================================

# The current game does not need internet or storage
# permissions because all assets are packaged inside the APK.

android.permissions =


# ============================================================
# ANDROID APP SETTINGS
# ============================================================

android.entrypoint = org.kivy.android.PythonActivity

android.presplash_color = #101010

android.adaptive_icon_foreground.filename = %(source.dir)s/assets/town_map.png

android.adaptive_icon_background.color = #101010


# ============================================================
# PYTHON-FOR-ANDROID
# ============================================================

p4a.bootstrap = sdl2


# ============================================================
# LOGGING
# ============================================================

android.logcat_filters = *:S python:D


# ============================================================
# VERSION CODE
# ============================================================

android.numeric_version = 1


# ============================================================
# BUILD SETTINGS
# ============================================================

# These make the build reproducible without unnecessarily
# changing the normal Buildozer defaults.

p4a.fork = kivy


# ============================================================
# WINDOWS / IOS
# ============================================================

# Not used for this project.


[buildozer]

log_level = 2

warn_on_root = 1
