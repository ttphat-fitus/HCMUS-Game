#!/bin/bash

echo "Starting Dino Run Game..."

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment not found!"
    echo "Please run ./setup.sh first to set up the game."
    exit 1
fi

# Activate virtual environment and run game
source venv/bin/activate
python3 main.py

if [ $? -ne 0 ]; then
    echo
    echo "Game exited with an error."
fi
