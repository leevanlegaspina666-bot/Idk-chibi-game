[app]

# ============================================================
# APP INFORMATION
# ============================================================

title = Chibi Shark Pet

package.name = chibisharkpet

package.domain = org.chibisharkpet

version = 1.0.0

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,txt

source.exclude_exts = spec

source.exclude_dirs = .git,.github,bin,.buildozer,__pycache__


# ============================================================
# PYTHON / KIVY
# ============================================================

requirements = python3==3.12.9,hostpython3==3.12.9,kivy==2.3.1


# ============================================================
# PYTHON-FOR-ANDROID
# ============================================================

p4a.fork = kivy

p4a.branch = master

p4a.bootstrap = sdl2


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

android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True

android.allow_backup = True


# ============================================================
# PERMISSIONS
# ============================================================

android.permissions =


# ============================================================
# ANDROID ACTIVITY
# ============================================================

android.entrypoint = org.kivy.android.PythonActivity


# ============================================================
# ANDROID BUILD OUTPUT
# ============================================================

android.debug_artifact = apk

android.numeric_version = 1


# ============================================================
# ANDROID LOGGING
# ============================================================

android.logcat_filters = *:S python:D


# ============================================================
# SPLASH SCREEN
# ============================================================

android.presplash_color = #101010


# ============================================================
# BUILD CONFIGURATION
# ============================================================

[buildozer]

log_level = 2

warn_on_root = 1
