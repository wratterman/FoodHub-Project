#!/bin/bash

exec python3 run_migrations.py &
exec sleep 60 &
exec python3 munchies.py