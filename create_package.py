#!/usr/bin/python3
import MySQLdb
import config

# Setup MySQL Connection
db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
cursor = db.cursor()

# Create a new user
cursor.execute("INSERT INTO packages (user_id, tracking_code, description) VALUES (1, 'EZ2000000002', 'Fake package 5')")

# Save changes to database
db.commit()
