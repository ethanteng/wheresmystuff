#!/usr/bin/python3
from flask import Response
import MySQLdb
import config
import requests
import datetime
from datetime import datetime
from dateutil import tz
import email_helper
from check_custom_carrier import check_custom_carrier


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

		tracking_code = package["tracking_code"]
		package_id = package["id"]
		carrier = package["carrier"]
		if not check_custom_carrier(tracking_code, carrier):
			get_trackers_query = """SELECT * FROM trackers WHERE package_id = %s"""
			get_trackers_parameters = [package_id]

			cursor.execute(get_trackers_query, get_trackers_parameters)
			tracker = cursor.fetchone()
			if (tracker["status"] != "delivered") and (tracker["status"] != "lost"): # Skip packages that have already been delivered or are currently lost
				
				if tracker["est_delivery_date"] is not None:
					if tracker["status"] in ("unknown","pre_transit","in_transit","out_for_delivery","available_for_pickup","delayed"):
						index = get_index_of_date(user_packages, tracker["est_delivery_date"])

						if index == -1:
							user_packages.append([tracker["est_delivery_date"], package])
						else:
							user_packages[index].append(package)
					else: # return_to_sender, failure, cancelled, error
						fake_date = datetime.strptime("January 31, 2100", "%B %d, %Y")
						index = get_index_of_date(user_packages, fake_date)

						if index == -1:
							user_packages.append([fake_date, package])
						else:
							user_packages[index].append(package)
				else:
					fake_date = datetime.strptime("January 31, 2100", "%B %d, %Y")
					index = get_index_of_date(user_packages, fake_date)

					if index == -1:
						user_packages.append([fake_date, package])
					else:
						user_packages[index].append(package)
		else:
			get_trackers_query = """SELECT * FROM custom_carrier_deliveries WHERE package_id = %s"""
			get_trackers_parameters = [package_id]

			cursor.execute(get_trackers_query, get_trackers_parameters)
			tracker = cursor.fetchone()
			if tracker is not None:
				if tracker["status"] is not None:
					if (tracker["status"].find("Delivered") == -1) and (tracker["status"].find("delivered") == -1) and (tracker["status"].find("lost") == -1): # Skip packages that have already been delivered or lost
						fake_date = datetime.strptime("January 31, 2200", "%B %d, %Y")
						index = get_index_of_date(user_packages, fake_date)

						if index == -1:
							user_packages.append([fake_date, package])
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
	email_json = {}

	for user_package in user_packages:
		json_key = ""
		PST_tz = tz.gettz("America/Los_Angeles")
		today = datetime.now(tz=PST_tz).strftime("%B %d, %Y")
		fake_date = datetime.strptime("January 31, 2100", "%B %d, %Y")
		fake_date_custom_carriers = datetime.strptime("January 31, 2200", "%B %d, %Y")

		if user_package[0].strftime("%B %d, %Y") == today:
			json_key = "ARRIVING TODAY:"
		elif user_package[0] < fake_date:
			delivery_date = user_package[0].strftime("%A %B %d, %Y")
			json_key = "Arriving on " + delivery_date + ":"
		elif user_package[0] < fake_date_custom_carriers:
			json_key = "Delivery date unknown for:"
		else:
			json_key = "Deliveries by other couriers:"


		json_value = ""
		for i in range(1, len(user_package)):
			description = None
			current_status = None
			current_location = None

			if user_package[i]["description"] is not None:
				description = str(user_package[i]["description"]) + ":"
			else:
				description = str(user_package[i]["tracking_code"]) + ":"

			current_status = get_current_status(user_package[i])
			if current_status is None:
				current_status = "unknown status"
			current_location = get_current_location(user_package[i])
			if current_location is None:
				current_location = "unknown location"

			json_value = json_value + "<li>" + description + " currently " + current_status + " at " + current_location + "</li>"

		#email_json.update({"packages" : [{"date" : json_key, "items" : json_value}]})
		email_json.setdefault('dates', []).append([{'date' : json_key}, {'items' : json_value}])

	send_email(user, email_json)


def send_email(user, email_json):
	from_addr = "Support at WheresMyStuff <support@wheresmystuff.co>"
	to_addr = str(user["email"])
	bcc_addr = "ethanteng@gmail.com"
	PST_tz = tz.gettz("America/Los_Angeles")
	today = datetime.now(tz=PST_tz).strftime("%b %-d")
	subject = str(today) + ": your packages are coming"
	email_helper.send_schedule_via_mailgun(from_addr, to_addr, bcc_addr, subject, email_json)


def get_current_status(package):
	# Setup MySQL Connection
	db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
	cursor = db.cursor(MySQLdb.cursors.DictCursor)

	if not check_custom_carrier(package["tracking_code"], package["carrier"]):
		query = """SELECT * FROM trackers WHERE package_id = %s"""
		parameters = [package["id"]]
		cursor.execute(query, parameters)
		tracker = cursor.fetchone()
	else:
		query = """SELECT * FROM custom_carrier_deliveries WHERE package_id = %s"""
		parameters = [package["id"]]
		cursor.execute(query, parameters)
		tracker = cursor.fetchone()

	return(str(tracker["status"]))


def get_current_location(package):
	# Setup MySQL Connection
	db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
	cursor = db.cursor(MySQLdb.cursors.DictCursor)

	if not check_custom_carrier(package["tracking_code"], package["carrier"]):
		query = """SELECT * FROM trackers WHERE package_id = %s"""
		parameters = [package["id"]]
		cursor.execute(query, parameters)
		tracker = cursor.fetchone()

		if ((tracker["current_city"] is None) and (tracker["current_city"] is None) and (tracker["current_country"] is None)):
			location = "unknown location"
		else:
			city = ""
			state = ""
			country = ""
			if tracker["current_city"] is not None:
				city = tracker["current_city"]
			if tracker["current_state"] is not None:
				state = tracker["current_state"]
			if tracker["current_country"] is not None:
				country = tracker["current_country"]
			location = city + " " + state + " " + country
	else:
		location = "unknown location"
	
	return(location)


def send_delivery_schedule_email(email):
	# Setup MySQL Connection
	db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
	cursor = db.cursor(MySQLdb.cursors.DictCursor)

	if email is None:	# Send email to all users
		cursor.execute("SELECT * FROM users")
	else:
		cursor.execute("SELECT * FROM users WHERE email IN " + "('" + email + "')")

	users = cursor.fetchall()
	for user in users:
		user_packages = get_packages_for_user(user["id"])
		if (len(user_packages) >= 1):
			generate_delivery_schedule_for_user(user, user_packages)