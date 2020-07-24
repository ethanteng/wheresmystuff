#!/usr/bin/python3
import requests
import config


def store_update_template():
	api_url = "https://api.mailgun.net/v3/" + config.mailgun_url + "/templates"
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
	api_url = "https://api.mailgun.net/v3/" + config.mailgun_url + "/templates"
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


def delete_update_template():
	api_url = "https://api.mailgun.net/v3/" + config.mailgun_url + "/templates"
	api_key = config.mailgun_api_key
	
	requests.delete(api_url,
			auth=("api",api_key),
			data={'name': 'update.template'})


def delete_schedule_template():
	api_url = "https://api.mailgun.net/v3/" + config.mailgun_url + "/templates"
	api_key = config.mailgun_api_key
	
	requests.delete(api_url,
			auth=("api",api_key),
			data={'name': 'schedule.template'})