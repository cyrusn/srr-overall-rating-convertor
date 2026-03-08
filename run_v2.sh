#!/bin/bash

# Navigate to the script's directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR/v2"

# Run the program using the virtual environment
if [ -f "./venv/bin/python" ]; then
    ./venv/bin/python main.py "$@"
else
    echo "Error: Virtual environment not found in v2/venv."
    echo "Please run the setup steps in v2/README.md first."
    exit 1
fi
