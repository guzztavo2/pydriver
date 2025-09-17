#!/usr/bin/env bash
export DISPLAY=:99

# Mata restos antigos
killall -q Xvnc fluxbox || true
rm -f /tmp/.X99-lock
rm -rf /tmp/.X11-unix/X99

# Inicia Xvnc (X11 + VNC em um só processo)
Xvnc :99 -geometry 1280x800 -depth 24 -rfbport ${VNC_PORT:-5900} -SecurityTypes None &
sleep 1

# Inicia fluxbox
fluxbox &

# Mantém o container vivo
tail -f /dev/null
