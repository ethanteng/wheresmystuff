#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import lxml
import MySQLdb
import config
import datetime
import send_email_helper


def get_status(url):
	source = requests.get(url).text
	soup = BeautifulSoup(source, 'lxml')

	delivery_status = soup.find(id="primaryStatus")
	if delivery_status is not None:
		return(delivery_status.text)
	else:
		return(delivery_status)


# Setup MySQL Connection
db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
cursor = db.cursor(MySQLdb.cursors.DictCursor)

query = """SELECT * FROM amazon_delivery INNER JOIN packages ON amazon_delivery.package_id = packages.id"""
cursor.execute(query)
deliveries = cursor.fetchall()

for delivery in deliveries:

	pkg_id = delivery["package_id"]
	url = delivery["tracking_url"]
	old_status = str(delivery["status"])

	if "Delivered" not in old_status:

		new_status = str(get_status(url))
		if ((old_status != new_status) and (new_status != "None")):
			update = """UPDATE amazon_delivery SET status = %s, updated_at = %s where package_id = %s"""
			updated_at = datetime.datetime.now()
			values = (new_status, updated_at, pkg_id)
			cursor.execute(update, values)
			db.commit()

			# Send update email
			tracking_code = None
			tracker_id = None
			status = None
			origin = None
			destination = None
			carrier = None
			est_delivery_date_obj = None
			status_detail = None
			current_city = None
			current_state = None
			current_country = None
			public_url = None

			tracking_code = delivery["tracking_code"]
			status = new_status
			public_url = url

			send_email_helper.send_email(tracking_code, status, status_detail, est_delivery_date_obj, carrier, origin, destination, current_city, current_state, current_country, public_url)
