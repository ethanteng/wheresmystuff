# wheresmystuff
Track all your package deliveries in one place. Get real-time updates on where your packages are, plus a daily summary of what's arriving and when. Never miss a delivery again!

---------- 

## Tech stack
* python
* flask
* ngrok
* mysql


## 3rd party APIs used
* easypost
* mailgun
* scraperapi


---------- 


## Supported delivery carriers
100+ carriers supported by [EasyPost](https://www.easypost.com/carriers)

**plus:**
* ECom Express
* NZ Post
* HK Post
* AliExpress
* Royal Mail
* Amazon


---------- 


### To run this locally or in your production environment, you'll need to create your own API keys for:
* [EasyPost](https://www.easypost.com/)
* [Mailgun](https://www.mailgun.com/)
* [ngrok](https://ngrok.com/)
* [ScraperAPI](https://www.scraperapi.com/)


### Steps to run this locally or in your production environment:
1. `cp config_template.py config.py` and add your test and/or production API keys in `config.py`.
2. In `config.py` set `env` to `'prod'` or `'test'` as appropriate for your state of development.
3. `export FLASK_APP=main.py` and start flask e.g. `python3 -m flask run`.
4. `ngrok config add-authtoken TOKEN` to add your ngrok authtoken.
5. Open `ngrok.yml` and add your tunnel(s). See `ngrok.yml` or `ngrok_test.yml` for examples.
6. Start nrok `ngrok start --all --config="<path_to_your_ngrok.yml>"`