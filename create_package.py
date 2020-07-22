#!/usr/bin/python3
import MySQLdb
import config

def create_package(user_id, tracking_code, description):
	# Setup MySQL Connection
	db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
	cursor = db.cursor()

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
