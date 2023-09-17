#!/bin/bash

python3 run_migrations.py &
wait $1
python3 main.py