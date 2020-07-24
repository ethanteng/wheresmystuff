#!/usr/bin/python3
import requests
import config
import json

def send_update_via_mailgun(from_addr, to_addr, bcc_addr, email_subject, email_json):

	api_url = "https://api.mailgun.net/v3/" + config.mailgun_url + "/messages"
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
	
	api_url = "https://api.mailgun.net/v3/" + config.mailgun_url + "/messages"
	api_key = config.mailgun_api_key
	requests.post(api_url,
			auth=("api",api_key),
			data={"from": from_addr,
				"to": to_addr,
				"bcc": bcc_addr,
				"subject": email_subject,
				"template": "schedule.template",
				"h:X-Mailgun-Variables": json.dumps(email_json)})