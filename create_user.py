#!/usr/bin/python3
import MySQLdb
import config

# Setup MySQL Connection
db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
cursor = db.cursor()

# Create a new user
cursor.execute("INSERT INTO users (firstname, lastname, email) VALUES ('Douglas','Bondick','douglasbondick@gmail.com')")

# Save changes to database
db.commit()
