#!/usr/bin/python3
import MySQLdb
import config

# Setup MySQL Connection
db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
cursor = db.cursor()

# Create a new package
cursor.execute("INSERT INTO packages (user_id, tracking_code, description) VALUES (1, 'EZ3000000003', 'Test package 3')")
pkg_id = cursor.lastrowid

# Create the associated tracker
query = "INSERT INTO trackers (package_id) VALUES (%s)"
value = [pkg_id]
cursor.execute(query, value)

# Save changes to database
db.commit()
