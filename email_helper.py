#!/usr/bin/python3
import requests
import config

def send_via_mailgun(from_addr, to_addr, bcc_addr, email_subject, email_text):
	#store_template()

	api_url = "https://api.mailgun.net/v3/sandbox6441ed402cbe4179802eb8bf0af5d96d.mailgun.org/messages"
	api_key = config.mailgun_api_key
	requests.post(api_url,
			auth=("api",api_key),
			data={"from": from_addr,
				"to": to_addr,
				"bcc": bcc_addr,
				"subject": email_subject,
				#"template": "alert.template",
				"text": email_text})


def store_template():
	api_url = "https://api.mailgun.net/v3/sandbox6441ed402cbe4179802eb8bf0af5d96d.mailgun.org/templates"
	api_key = config.mailgun_api_key
	
	template_content = ""
	filepath = "./templates/alert.html"
	with open(filepath, mode='r') as template_file:
		template_content = template_file.read()

	requests.post(api_url,
			auth=("api",api_key),
			data={'template': template_content,
				'name': 'alert.template',
				'description': 'Alert template'})