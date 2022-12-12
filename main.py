from flask import Flask, request, Response
import json
import requests
import MySQLdb
import config
import datetime
from datetime import datetime
import send_email_helper
import email_helper
import delivery_schedule
import create_user
import create_package


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
			send_email_helper.send_email(tracking_code, status, status_detail, est_delivery_date_obj, carrier, origin, destination, current_city, current_state, current_country, public_url)
			
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


@app.get('/send_email')
def send_email():
	args = request.args
	email = args.get("email")
	delivery_schedule.send_delivery_schedule_email(email)

	return Response(status=200)


@app.post('/new_user')
def new_user():
	args = request.args
	first_name = args.get("first_name")
	last_name = args.get("last_name")
	email = args.get("email")
	user_id = create_user.create_user(first_name,last_name,email)

	return Response(status=201)


@app.post('/track_package')
def track_package():
	args = request.args

	# Both email and tracking_code are required params
	email = args.get("email")
	tracking_code = args.get("tracking_code")
	if (email is None or tracking_code is None):
		return Response(status=500)
	else:
		# Optional params
		carrier = args.get("carrier")
		description = args.get("description")
		custom_url = args.get("custom_url")

		user_id = create_user.create_user(None, None, email) # create new user if user isn't already in database
		created_new_package = create_package.create_package(user_id, tracking_code, carrier, description, custom_url)
		if (created_new_package):
			email_helper.send_ack_via_mailgun(email, tracking_code, description)
			return Response(status=201)
		else:
			return Response(status=200)