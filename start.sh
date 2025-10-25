#!/bin/bash

# Start virtual framebuffer
Xvfb :1 -screen 0 ${VNC_RESOLUTION}x24 &
sleep 2

# Start desktop environment
xfce4-session &

# Start VNC server
x11vnc -display :1 -nopw -forever -listen 0.0.0.0 -rfbport ${VNC_PORT} &

# Start noVNC (Websockify)
websockify --web=/usr/share/novnc/ ${NOVNC_PORT} localhost:${VNC_PORT} &

# Start ChargeGuru 
ChargeGuru
