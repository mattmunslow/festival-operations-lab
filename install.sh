#!/bin/sh
# Sets up the lab on macOS or Linux. On Windows, follow INSTRUCTIONS.md.
set -e

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example. Fill in your values before running the scripts."
fi

echo ""
echo "Setup complete. Activate the environment in each new terminal with:"
echo "    source .venv/bin/activate"
