#!/bin/bash

python3 -m venv venv
source ./venv/bin/activate
pip install setuptools wheel
python3 setup.py sdist bdist_wheel
