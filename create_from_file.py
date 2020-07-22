#!/usr/bin/python3
import sys
import os
import csv
import create_user
import create_package

filepath = sys.argv[1]
if not os.path.isfile(filepath):
	sys.exit()

with open(filepath, mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for row in csv_reader:

		user_id = create_user.create_user(row["first_name"], row["last_name"], row["email"])
		create_package.create_package(user_id, row["tracking_code"], row["description"])