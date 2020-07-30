#!/usr/bin/bash
python3 -m pip install Flask
python3 -m pip install requests
python3 -m pip install lxml
python3 -m pip install bs4
export FLASK_APP=/home/ethanteng_gmail_com/wheresmystuff/main.py
python3 -m flask run