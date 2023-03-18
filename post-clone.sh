#!/bin/bash

python3 -m pip install -r requirements.txt

mkdir -p $HOME/.local/bin
cp plot.py $HOME/.local/bin/plot
