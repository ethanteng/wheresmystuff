#!/usr/bin/python3
import MySQLdb
import config
import create_tracker
import check_amazon

def create_package(user_id, tracking_code, carrier, description, amazon_url):
	# Setup MySQL Connection
	db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
	cursor = db.cursor()

	# Check if the tracking code already exists for the user
	check_stmt = """SELECT COUNT(*) FROM packages WHERE user_id = %s AND tracking_code = %s"""
	check_value = (user_id, tracking_code)
	cursor.execute(check_stmt, check_value)
	results = cursor.fetchone()
	num_results = results[0]

	# If the tracking code doesn't already exist for the user
	if (num_results == 0):
		
		# Create a new package
		if (carrier is None):
			new_pkg_stmt = """INSERT INTO packages (user_id, tracking_code, description) VALUES (%s, %s, %s)"""
			new_pkg_values = (user_id, tracking_code, description)
		else:
			new_pkg_stmt = """INSERT INTO packages (user_id, tracking_code, carrier, description) VALUES (%s, %s, %s, %s)"""
			new_pkg_values = (user_id, tracking_code, carrier, description)

		cursor.execute(new_pkg_stmt, new_pkg_values)
		pkg_id = cursor.lastrowid

		if not check_amazon.check_amazon(tracking_code):

			# Create the associated tracker db entry
			query = "INSERT INTO trackers (package_id) VALUES (%s)"
			value = [pkg_id]
			cursor.execute(query, value)

			# Save changes to database
			db.commit()

			# Create the EasyPost tracker object
			create_tracker.create_tracker(tracking_code, carrier)
		else:

			query = "INSERT INTO amazon_delivery (package_id, tracking_url) VALUES (%s, %s)"
			values = (pkg_id, amazon_url)
			cursor.execute(query, values)

			db.commit()