from flask import Flask, request, Response
import json
import requests
import MySQLdb
import config
import datetime
from datetime import datetime
import email_helper

app = Flask(__name__)
@app.route('/webhook', methods=['POST'])


def respond():
	update = request.json

	if update["description"] != "tracker.created":
		tracking_code = None
		tracker_id = None
		status = None
		origin = None
		destination = None
		carrier = None
		est_delivery_date_obj = None
		updated_at_date_obj = None
		status_detail = None
		current_city = None
		current_state = None
		current_country = None
		public_url = None

		if update["result"] is not None:
			if update["result"]["tracking_code"] is not None:
				tracking_code = update["result"]["tracking_code"]
			if update["result"]["id"] is not None:
				tracker_id = update["result"]["id"]
			if update["result"]["status"] is not None:
				status = update["result"]["status"]
			if update["result"]["carrier_detail"] is not None:
				if update["result"]["carrier_detail"]["origin_location"] is not None:
					origin = update["result"]["carrier_detail"]["origin_location"]
				if update["result"]["carrier_detail"]["destination_location"] is not None:
					destination = update["result"]["carrier_detail"]["destination_location"]
			if update["result"]["carrier"] is not None:
				carrier = update["result"]["carrier"]
			if update["result"]["public_url"] is not None:
				public_url = update["result"]["public_url"]

			# Formatting the delivery date to be more human-readable
			if update["result"]["est_delivery_date"] is not None:
				est_delivery_date_str = str(update["result"]["est_delivery_date"])
				est_delivery_date_obj = datetime.strptime(est_delivery_date_str, "%Y-%m-%dT%H:%M:%SZ")
				#est_delivery_date = est_delivery_date_obj.strftime("%b %d %Y %-I:%M%p")

			# Formatting the updated at date to be more human readable
			if update["result"]["updated_at"] is not None:
				updated_at_date_str = str(update["result"]["updated_at"])
				updated_at_date_obj = datetime.strptime(updated_at_date_str, "%Y-%m-%dT%H:%M:%SZ")

			# Get the most recent tracking details
			if update["result"]["tracking_details"] is not None:
				tracking_details = update["result"]["tracking_details"]
				num_tracking_details = len(tracking_details)
				most_recent_detail = update["result"]["tracking_details"][num_tracking_details-1]
				status_detail = most_recent_detail["message"]
				current_city = most_recent_detail["tracking_location"]["city"]
				current_state = most_recent_detail["tracking_location"]["state"]
				current_country = most_recent_detail["tracking_location"]["country"]
			else:
				status_detail = None
				current_city = None
				current_state = None
				current_country = None

			update_tracker(tracking_code, tracker_id, status, est_delivery_date_obj, current_city, current_state, current_country, updated_at_date_obj)
			#send_email(tracking_code, status, status_detail, est_delivery_date, carrier, origin, destination, current_city, current_state, current_country)
			send_email(tracking_code, status, status_detail, est_delivery_date_obj, carrier, origin, destination, current_city, current_state, current_country, public_url)
			
			return Response(status=200)
		else:
			return Response(status=500)
	else:
		return Response(status=200)


def update_tracker(tracking_code, tracker_id, status, est_delivery_date, current_city, current_state, current_country, updated_at_date):
	# Setup MySQL Connection
	db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
	cursor = db.cursor()

	# Find package associated with this tracker
	query_packages = """SELECT id FROM packages WHERE tracking_code = %s"""
	cursor.execute(query_packages, [tracking_code])
	pkg_id = cursor.fetchone()

	# Update tracker db table
	query_trackers = """UPDATE trackers SET tracker_id = %s, status = %s, est_delivery_date = %s, current_city = %s, current_state = %s, current_country = %s, updated_at = %s WHERE package_id = %s"""
	query_parameters = (tracker_id, status, est_delivery_date, current_city, current_state, current_country, updated_at_date, pkg_id)
	cursor.execute(query_trackers, query_parameters)

	# Save changes to database
	db.commit()


def send_email(tracking_code, status, status_detail, est_delivery_date, carrier, origin, destination, current_city, current_state, current_country, public_url):
	# Setup MySQL Connection
	db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
	cursor = db.cursor()
	
	# Find user associated with this package
	query_packages = """SELECT user_id, description FROM packages WHERE tracking_code = %s"""
	cursor.execute(query_packages, [tracking_code])
	result = cursor.fetchone()
	user_id = result[0]
	description = result[1]
	
	# Get user name and email
	query_users = """SELECT firstname, lastname, email FROM users WHERE id = %s"""
	cursor.execute(query_users, [user_id])
	user = cursor.fetchone()
	firstname = user[0]
	lastname = user[1]
	email = user[2]

	# Formatting the delivery date to be more human-readable (with AM / PM)
	est_delivery_date_ampm = None
	if est_delivery_date is not None:
		est_delivery_date_ampm = est_delivery_date.strftime("%b %d %Y %-I:%M%p")
	
	# Send email
	from_addr = "Support at WheresMyStuff <support@wheresmystuff.co>"
	to_addr = str(email)
	bcc_addr = "ethanteng@gmail.com"
	if description is not None:
		subject = "Update about your " + str(description)
	else:
		subject = "Update about your package " + str(tracking_code)
	if status is None:
		status = "unknown"
	if status_detail is None:
		status_detail = "no further details available"
	if ((current_city is None) and (current_state is None) and (current_country is None)):
		current_location = "unknown"
	else:
		if current_city is None:
			current_city = ""
		if current_state is None:
			current_state = ""
		if current_country is None:
			current_country = ""
		current_location = current_city + " " + current_state + " " + current_country
	if destination is None:
		destination = ""
	if est_delivery_date_ampm is None:
		est_delivery_date_ampm = "none available"
	if carrier is None:
		carrier = ""
	if public_url is None:
		public_url = ""
	email_json = {
		"status": str(status),
		"status_detail": str(status_detail),
		"current_location": current_location,
		"destination": str(destination),
		"est_delivery_date": str(est_delivery_date_ampm),
		"carrier": str(carrier),
		"tracking_code": str(tracking_code),
		"public_url" : str(public_url)
	}
	email_helper.send_update_via_mailgun(from_addr, to_addr, bcc_addr, subject, email_json)