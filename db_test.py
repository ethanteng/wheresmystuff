#!/usr/bin/python3
import MySQLdb
import config
	
def find_user_by_package(tracking_code):
	# Setup MySQL Connection
	db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
	cursor = db.cursor()
	
	# Find user & description associated with this package
	find_user_query = """SELECT user_id, description FROM packages WHERE tracking_code = %s"""
	cursor.execute(find_user_query, [tracking_code])
	user_id = cursor.fetchone()
	
	return(user_id)
	

def get_user_info(user_id):
	# Setup MySQL Connection
	db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
	cursor = db.cursor()

	# Get user name and email
	query_users = """SELECT firstname, lastname, email FROM users WHERE id = %s"""
	cursor.execute(query_users, [user_id])
	user = cursor.fetchone()
	
	return(user)


user_id = find_user_by_package("LY330942479CN")
print(user_id[0])
print(user_id[1])
#user = get_user_info(1)
#print(user[0])
#print(user[1])
#print(user[2])
