#/bin/bash

SOUND_UID=$(id -u daniel)
sudo XDG_RUNTIME_DIR=/run/user/$SOUND_UID \
    PULSE_SERVER=unix:/run/user/$SOUND_UID/pulse/native \
    ./venv/bin/python3 game.py 
