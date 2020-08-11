#!/usr/bin/python3
import sys
import os
import csv
import create_user
import create_package
import email_helper

filepath = sys.argv[1]
if not os.path.isfile(filepath):
	sys.exit()

with open(filepath, mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for row in csv_reader:

		first_name = row["first_name"]
		if first_name == "":
			first_name = None
		last_name = row["last_name"]
		if last_name == "":
			last_name = None
		email = row["email"]
		if email == "":
			email = None
		tracking_code = row["tracking_code"]
		if tracking_code == "":
			tracking_code = None
		carrier = row["carrier"]
		if carrier == "":
			carrier = None
		description = row["description"]
		if description == "":
			description = None
		custom_url = row["custom_url"]
		if custom_url == "":
			custom_url = None

		user_id = create_user.create_user(first_name, last_name, email)
		created_new_package = create_package.create_package(user_id, tracking_code, carrier, description, custom_url)
		
		if (created_new_package):
			email_helper.send_ack_via_mailgun(email, tracking_code, description)