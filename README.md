# wheresmystuff
TripIt for package deliveries
https://wheresmystuff.co/


Local env
=========

### Set env variable in config.py
* env = "test"


### Upload email templates to Mailgun
* ./setup_templates.py


### Start Flask
* export FLASK_APP=main.py
* python3 -m flask run


### Start ngrok
* cp ngrok_test.yml /home/ubuntu/.ngrok2/ngrok.yml
* [add ngrok_auth_token to ngrok.yml]
* cd /home/ubuntu/Downloads
* nohup ./ngrok start --all --config="/home/ubuntu/.ngrok2/ngrok.yml" &


Production env
==============

### Set env variable in config.py
* env = "prod"


### Upload email templates to Mailgun
* ./setup_templates.py


### Start Flask if not already included in startup script
* export FLASK_APP=main.py
* python3 -m flask run


### Start ngrok
* cp ngrok.yml /home/ethanteng_gmail_com/.ngrok2
* [add ngrok_auth_token to ngrok.yml]
* cd /home/ethanteng_gmail_com
* nohup ./ngrok start --all --config="/home/ethanteng_gmail_com/.ngrok2/ngrok.yml" &


### Set up cron job for daily schedule emails
* crontab -e
* 01 00 * * * /home/ethanteng_gmail_com/wheresmystuff/delivery_schedule.py
