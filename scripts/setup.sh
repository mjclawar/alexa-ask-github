#!/usr/bin/env bash


if [ ! -f ../ngrok ]; then
    wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip \
        -O ../ngrok.zip
    unzip ../ngrok.zip  -d ../
fi

. ././../venv/bin/activate
pip install -r ././../requirements.txt
