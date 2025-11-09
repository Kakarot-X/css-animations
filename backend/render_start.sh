#!/bin/bash
cd /opt/render/project/src/backend
python seed_animations.py
uvicorn server:app --host 0.0.0.0 --port $PORT
