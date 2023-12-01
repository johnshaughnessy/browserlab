#!/bin/bash
echo ""
echo "Browserlab Launcher Initialization"
echo ""

echo "***Warning***"
echo "This installation makes changes on the host, NOT inside a docker container."
echo "Are you sure you want to continue? (y/n)"
read -r response
if ! echo "$response" | grep -Eq '^[yY]([eE][sS])?$'; then
    echo "Aborting."
    exit 1
fi

echo ""
echo "Installing python3, python3-pip, and python3-venv on the host."
echo "This will require sudo privileges."
sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv

# Set the directory where the virtual environment will be created
VENV_DIR=$HOME/browserlab/launcher/venv

# Create the virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "Creating virtual environment in $VENV_DIR"
    echo "Confirm? (y/n)"
    read -r response2
    if ! echo "$response2" | grep -Eq '^[yY]([eE][sS])?$'; then
        echo "Aborting."
        exit 1
    fi

    python3 -m venv $VENV_DIR
else
    echo ""
    echo "Virtual environment already exists in $VENV_DIR"
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

echo ""
echo "Activating virtual environment. ($VENV_DIR)"
echo "When we run 'which pip', it should point to $VENV_DIR/bin/pip :"
echo ""
which pip
echo ""
echo "If it does not, abort now. Continue? (y/n)"
read -r response3
if ! echo "$response3" | grep -Eq '^[yY]([eE][sS])?$'; then
    echo "Aborting."
    exit 1
fi

echo ""
echo "Now, in the virtual environment, we will install Flask."
pip install --upgrade pip

# Install Flask if it's not already installed
if ! pip freeze | grep -q Flask; then
    echo ""
    echo "Installing Flask"
    pip install Flask
else
    echo ""
    echo "Flask is already installed"
fi

# Deactivate the virtual environment
deactivate

echo ""
echo ""
echo "Initialization complete."
