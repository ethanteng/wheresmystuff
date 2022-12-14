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