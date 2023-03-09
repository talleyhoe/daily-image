#!/bin/bash

script_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
cd $script_path

echo "Make sure your config is setup"
echo "Running..."
source ./pyenv/bin/activate
cd ./src
python main.py
