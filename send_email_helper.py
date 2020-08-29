#!/usr/bin/python3
import email_helper
import datetime
import MySQLdb
import config
import check_custom_carrier

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
	if check_custom_carrier.check_custom_carrier(tracking_code, carrier):	
		est_delivery_date_ampm = status
	else:
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