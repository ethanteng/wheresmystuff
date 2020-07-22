#!/usr/bin/python3
import MySQLdb
import config

def create_user(firstname, lastname, email):
	# Setup MySQL Connection
	db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
	cursor = db.cursor()

	# Create a new user
	insert_stmt = """INSERT INTO users (firstname, lastname, email) VALUES (%s, %s, %s)"""
	insert_values = (firstname, lastname, email)
	return_user_id = -1

	try:
		cursor.execute(insert_stmt, insert_values)
		return_user_id = cursor.lastrowid
		db.commit()
	except:
		select_stmt = """SELECT id from users WHERE email = %s"""
		select_values = [email]
		cursor.execute(select_stmt, select_values)
		return_user_id = cursor.fetchone()[0]

	return(return_user_id)