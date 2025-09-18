#!/usr/bin/env bash
export DISPLAY=:99

killall -q Xvnc fluxbox || true
rm -f /tmp/.X99-lock
rm -rf /tmp/.X11-unix/X99

Xvnc :99 -geometry 1280x800 -depth 24 -rfbport ${VNC_PORT:-5900} -SecurityTypes None &
sleep 2
fluxbox &
sleep 2
chromium --no-sandbox --disable-dev-shm-usage --user-data-dir=/tmp/chromium-vnc &
tail -f /dev/null