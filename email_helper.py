#!/usr/bin/python3
import requests
import config
import json

def send_update_via_mailgun(from_addr, to_addr, bcc_addr, email_subject, email_json):
	store_update_template()

	api_url = "https://api.mailgun.net/v3/sandbox6441ed402cbe4179802eb8bf0af5d96d.mailgun.org/messages"
	api_key = config.mailgun_api_key
	requests.post(api_url,
			auth=("api",api_key),
			data={"from": from_addr,
				"to": to_addr,
				"bcc": bcc_addr,
				"subject": email_subject,
				"template": "update.template",
				"h:X-Mailgun-Variables": json.dumps(email_json)})


def send_schedule_via_mailgun(from_addr, to_addr, bcc_addr, email_subject, email_json):
	#store_schedule_template()

	api_url = "https://api.mailgun.net/v3/sandbox6441ed402cbe4179802eb8bf0af5d96d.mailgun.org/messages"
	api_key = config.mailgun_api_key
	requests.post(api_url,
			auth=("api",api_key),
			data={"from": from_addr,
				"to": to_addr,
				"bcc": bcc_addr,
				"subject": email_subject,
				"template": "schedule.template",
				"h:X-Mailgun-Variables": json.dumps(email_json)})


def store_update_template():
	api_url = "https://api.mailgun.net/v3/sandbox6441ed402cbe4179802eb8bf0af5d96d.mailgun.org/templates"
	api_key = config.mailgun_api_key
	
	template_content = ""
	filepath = "./templates/update.html"
	with open(filepath, mode='r') as template_file:
		template_content = template_file.read()

	requests.post(api_url,
			auth=("api",api_key),
			data={'template': template_content,
				'name': 'update.template',
				'description': 'Update template'})


def store_schedule_template():
	api_url = "https://api.mailgun.net/v3/sandbox6441ed402cbe4179802eb8bf0af5d96d.mailgun.org/templates"
	api_key = config.mailgun_api_key
	
	template_content = ""
	filepath = "./templates/schedule.html"
	with open(filepath, mode='r') as template_file:
		template_content = template_file.read()

	requests.post(api_url,
			auth=("api",api_key),
			data={'template': template_content,
				'name': 'schedule.template',
				'description': 'Schedule template'})