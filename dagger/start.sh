#!/bin/bash

# Start virtual framebuffer
Xvfb :1 -screen 0 ${VNC_RESOLUTION}x24 &
sleep 2

# Start minimal window manager (optional)
matchbox-window-manager -use_titlebar no &

# Start ChargeGuru in full-screen mode (if supported)
DISPLAY=:1 ChargeGuru &

# Wait a bit to ensure app is running before starting VNC
sleep 3

# Start VNC server
x11vnc -display :1 -nopw -forever -listen 0.0.0.0 -rfbport ${VNC_PORT} \
        -noxrecord -noxfixes -noxdamage -clip ${VNC_RESOLUTION}x${VNC_RESOLUTION} &

# Start noVNC
websockify --web=/usr/share/novnc/ ${NOVNC_PORT} localhost:${VNC_PORT}
