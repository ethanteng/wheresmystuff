#!/usr/bin/python3
import MySQLdb

# Setup MySQL Connection
db = MySQLdb.connect(host="localhost", user="root", passwd="wheresmystuffC0", db="wheresmystuff")
cursor = db.cursor()

# Create a new user
cursor.execute("INSERT INTO packages (user_id, tracking_code, description) VALUES (1, 'EZ2000000002', 'Fake package 5')")

# Save changes to database
db.commit()
