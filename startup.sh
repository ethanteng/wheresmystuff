#!/usr/bin/bash
python3 -m pip install Flask
python3 -m pip install requests
python3 -m pip install lxml
python3 -m pip install bs4
python3 -m pip install python-dateutil
python3 -m pip install fake-useragent
python3 -m pip install scraperapi-sdk
sudo cp /home/ethanteng_gmail_com/crawlera-ca.crt /usr/local/share/ca-certificates/crawlera-ca.crt
sudo update-ca-certificates
export FLASK_APP=/home/ethanteng_gmail_com/wheresmystuff/main.py
python3 -m flask run