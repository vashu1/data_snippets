#!/usr/bin/env bash

python3 -m venv env

./env/bin/pip install -r requirements.txt

# no proper installation for mpl_toolkits
git clone --depth 1 https://github.com/matplotlib/basemap.git
cd basemap
../env/bin/python setup.py install
cd -
