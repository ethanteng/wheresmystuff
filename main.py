from flask import Flask, request, Response
import json
import requests
import MySQLdb
import config
import datetime
from datetime import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def respond():
	update = request.json
	tracking_code = update["result"]["tracking_code"]
	status = update["result"]["status"]

	# Formatting the delivery date to be more human-readable
	est_delivery_date_str = str(update["result"]["est_delivery_date"])
	est_delivery_date_obj = datetime.strptime(est_delivery_date_str, "%Y-%m-%dT%H:%M:%SZ")
	est_delivery_date = est_delivery_date_obj.strftime("%b %d %Y %-I:%M%p")
	
	carrier = update["result"]["carrier"]

	send_email(tracking_code, status, est_delivery_date, carrier)
	
	return Response(status=200)
	
	
def send_email(tracking_code, status, est_delivery_date, carrier):
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
	
	# Send email
	api_url = "https://api.mailgun.net/v3/sandbox6441ed402cbe4179802eb8bf0af5d96d.mailgun.org/messages"
	api_key = config.mailgun_api_key
	requests.post(api_url,
			auth=("api",api_key),
			data={"from": "Support at WheresMyStuff<support@sandbox6441ed402cbe4179802eb8bf0af5d96d.mailgun.org>",
				"to": str(email),
				"bcc": "ethanteng@gmail.com",
				"subject": "Update about your " + str(description),
				"text": "Tracking code: " + str(tracking_code) + "\n" + "Delivery status: " + str(status) + "\n" + "Estimated delivery date: " + str(est_delivery_date) + "\n" + "Carrier: " + str(carrier)})
