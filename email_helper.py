#!/usr/bin/python3
import requests
import config
import json

def send_update_via_mailgun(from_addr, to_addr, bcc_addr, email_subject, email_json):

	api_url = None
	if config.env == "test":
		api_url = "https://api.mailgun.net/v3/" + config.mailgun_test_url + "/messages"
	else:
		api_url = "https://api.mailgun.net/v3/" + config.mailgun_prod_url + "/messages"

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
	
	api_url = None
	if config.env == "test":
		api_url = "https://api.mailgun.net/v3/" + config.mailgun_test_url + "/messages"
	else:
		api_url = "https://api.mailgun.net/v3/" + config.mailgun_prod_url + "/messages"

	api_key = config.mailgun_api_key
	requests.post(api_url,
			auth=("api",api_key),
			data={"from": from_addr,
				"to": to_addr,
				"bcc": bcc_addr,
				"subject": email_subject,
				"template": "schedule.template",
				"h:X-Mailgun-Variables": json.dumps(email_json)})


def send_ack_via_mailgun(email, tracking_code, description):

	from_addr = "Support at WheresMyStuff <support@wheresmystuff.co>"
	to_addr = str(email)
	bcc_addr = "ethanteng@gmail.com"
	if description is not None:
		email_subject = "WheresMyStuff is now tracking your " + str(description) + " (" + str(tracking_code) + ")"
	else:
		email_subject = "WheresMyStuff is now tracking your package " + str(tracking_code)
	email_body = "Thanks for using WheresMyStuff! You'll start getting updates about this package (" + str(tracking_code) + ") from support@wheresmystuff.co."

	api_url = None
	if config.env == "test":
		api_url = "https://api.mailgun.net/v3/" + config.mailgun_test_url + "/messages"
	else:
		api_url = "https://api.mailgun.net/v3/" + config.mailgun_prod_url + "/messages"

	api_key = config.mailgun_api_key
	requests.post(api_url,
			auth=("api",api_key),
			data={"from": from_addr,
				"to": to_addr,
				"bcc": bcc_addr,
				"subject": email_subject,
				"text": email_body})