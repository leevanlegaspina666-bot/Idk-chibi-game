[app]

title = Chibi Shark Pet
package.name = chibisharkpet
package.domain = org.chibisharkpet
version = 1.0.0

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,txt
source.exclude_exts = spec
source.exclude_dirs = .git,.github,bin,.buildozer,__pycache__,p4a-local

requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.1

orientation = landscape
fullscreen = 1

android.api = 35
android.minapi = 24
android.ndk = 28c
android.ndk_api = 24

android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True

android.entrypoint = org.kivy.android.PythonActivity
android.debug_artifact = apk
android.numeric_version = 1
android.allow_backup = True
android.permissions =

p4a.fork = kivy
p4a.branch = master
p4a.source_dir = ./p4a-local
p4a.bootstrap = sdl2

android.presplash_color = #101010


[buildozer]

log_level = 2
warn_on_root = 1
