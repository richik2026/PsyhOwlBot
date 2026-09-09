#!/bin/sh
set -e

alembic upgrade head
python bot_runner.py
