#!/usr/bin/python3
import MySQLdb
import config
import requests
import datetime


def get_packages_for_user(user_id):
	# Setup MySQL Connection
	db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
	cursor = db.cursor(MySQLdb.cursors.DictCursor)

	get_pkgs_query = """SELECT * FROM packages WHERE user_id = %s"""
	get_pkgs_parameters = [user_id]

	user_packages = []
	cursor.execute(get_pkgs_query, get_pkgs_parameters)
	packages = cursor.fetchall()
	for package in packages:

		package_id = package["id"]
		get_trackers_query = """SELECT * FROM trackers WHERE package_id = %s"""
		get_trackers_parameters = [package_id]

		cursor.execute(get_trackers_query, get_trackers_parameters)
		tracker = cursor.fetchone()
		if tracker["est_delivery_date"] >= datetime.datetime.now():
			
			index = get_index_of_date(user_packages, tracker["est_delivery_date"])
			if index == -1:
				user_packages.append([tracker["est_delivery_date"], package])
			else:
				user_packages[index].append(package)

	return(user_packages)


def get_index_of_date(array_to_search, date_to_find):
	dates_only = []
	for duple in array_to_search:

		dates_only.append(duple[0].strftime("%A %B %d, %Y"))

	try:
		index = dates_only.index(date_to_find.strftime("%A %B %d, %Y"))
	except:
		index = -1

	return(index)


def generate_delivery_schedule_for_user(user, user_packages):
	user_packages.sort()
	email_body = ""

	try:
		for user_package in user_packages:
			
			delivery_date = user_package[0].strftime("%A %B %d, %Y")
			email_body = email_body + "Arriving on " + delivery_date + ": " + "\n"

			for i in range(1, len(user_package)):

				description = str(user_package[i]["description"])
				carrier = str(user_package[i]["carrier"])
				tracking_code = str(user_package[i]["tracking_code"])

				if (carrier != 'None'):
					email_body = email_body + description + " (tracking code " + tracking_code + " to be delivered via " + carrier + ")\n"
				else:
					email_body = email_body + description + " (tracking code " + tracking_code + ")\n"
			else:
				email_body = email_body + "\n"
	except:
		print("No packages for user_id " + str(user["id"]))

	send_email(user, email_body)


def send_email(user, email_body):
	to_email = str(user["email"])
	subject = "Your scheduled deliveries"
	api_url = "https://api.mailgun.net/v3/sandbox6441ed402cbe4179802eb8bf0af5d96d.mailgun.org/messages"
	api_key = config.mailgun_api_key
	requests.post(api_url,
			auth=("api",api_key),
			data={"from": "Support at WheresMyStuff<support@sandbox6441ed402cbe4179802eb8bf0af5d96d.mailgun.org>",
				"to": str(to_email),
				"bcc": "ethanteng@gmail.com",
				"subject": subject,
				"text": email_body})


# Setup MySQL Connection
db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
cursor = db.cursor(MySQLdb.cursors.DictCursor)

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
	
	user_packages = get_packages_for_user(user["id"])
	if (len(user_packages) >= 1):
		generate_delivery_schedule_for_user(user, user_packages)