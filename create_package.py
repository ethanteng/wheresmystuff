#!/usr/bin/python3
import MySQLdb
import config
import create_tracker

def create_package(user_id, tracking_code, description):
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
		new_pkg_stmt = """INSERT INTO packages (user_id, tracking_code, description) VALUES (%s, %s, %s)"""
		new_pkg_values = (user_id, tracking_code, description)
		cursor.execute(new_pkg_stmt, new_pkg_values)
		pkg_id = cursor.lastrowid

		# Create the associated tracker db entry
		query = "INSERT INTO trackers (package_id) VALUES (%s)"
		value = [pkg_id]
		cursor.execute(query, value)

		# Save changes to database
		db.commit()

		# Create the EasyPost tracker object
		create_tracker.create_tracker(tracking_code)