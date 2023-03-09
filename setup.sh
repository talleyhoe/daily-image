#!/bin/bash

script_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
cd $script_path

echo "Creating a virtual environment"
python -m venv pyenv

echo "Installing requirements"
source ./pyenv/bin/activate
pip install -r ./requirements.txt --quiet 

echo "Done!"
