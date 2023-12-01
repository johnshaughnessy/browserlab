#!/bin/bash
VENV_DIR=$HOME/browserlab/launcher/venv

echo "Activating virtual environment. ($VENV_DIR))"
source $VENV_DIR/bin/activate
echo "When you want to deactivate, run $VENV_DIR/bin/deactivate ."

echo "Starting server."
pushd $HOME/browserlab

echo "Starting server from pwd: $(pwd)"
python3 $HOME/browserlab/launcher/server/server.py
