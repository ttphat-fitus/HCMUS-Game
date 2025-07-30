#!/bin/bash

echo "=== Dino Run Python Game Setup (macOS/Linux) ==="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

echo "Running setup script..."
python3 setup.py

if [ $? -ne 0 ]; then
    echo
    echo "Setup failed! Please check the errors above."
    exit 1
fi

echo
echo "Setup completed!"
echo
echo "To run the game:"
echo "1. Run: ./run_game.sh"
echo "   OR"
echo "2. Manually activate environment and run:"
echo "   source venv/bin/activate"
echo "   python3 main.py"
echo

# Make run script executable
chmod +x run_game.sh

echo "Made run_game.sh executable"
