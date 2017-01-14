#!/usr/bin/env bash

. ././../../venv/bin/activate

PYTHONPATH=~/Projects/Argos gunicorn --bind 0.0.0.0:8080 alexa.app:app --workers 5
#PYTHONPATH=~/Projects/Argos python ././../app/__init__.py
