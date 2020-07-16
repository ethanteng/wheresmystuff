#!/usr/bin/python3
import requests
import config

def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandbox6441ed402cbe4179802eb8bf0af5d96d.mailgun.org/messages",
		auth=("api", config.mailgun_api_key),
		data={"from": "Excited User <mailgun@sandbox6441ed402cbe4179802eb8bf0af5d96d.mailgun.org>",
			"to": ["ethanteng@gmail.com", "ethanteng@gmail.com"],
			"subject": "This is awesome",
			"text": "Mailgun for the win!"})
			
send_simple_message()
