#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import lxml
import MySQLdb
import config
import datetime


def get_status(url):
	source = requests.get(url).text
	soup = BeautifulSoup(source, 'lxml')

	delivery_status = soup.find(id="primaryStatus")
	return(delivery_status.text)


# Setup MySQL Connection
db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
cursor = db.cursor(MySQLdb.cursors.DictCursor)

query = """SELECT * FROM amazon_delivery"""
cursor.execute(query)
deliveries = cursor.fetchall()

for delivery in deliveries:

	pkg_id = delivery["package_id"]
	url = delivery["tracking_url"]
	status = get_status(url)

	update = """UPDATE amazon_delivery SET status = %s, updated_at = %s where package_id = %s"""
	updated_at = datetime.datetime.now()
	values = (status, updated_at, pkg_id)
	cursor.execute(update, values)
	db.commit()