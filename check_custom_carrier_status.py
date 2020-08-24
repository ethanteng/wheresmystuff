#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import lxml
import MySQLdb
import config
import datetime
import send_email_helper
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import random


def get_status(url, carrier):

	ua = UserAgent() # From here we generate a random user agent
	proxies = [] # Will contain proxies [ip, port]

	# Retrieve latest proxies
	proxies_req = Request(config.proxy_list_url)
	proxies_req.add_header('User-Agent', ua.random)
	proxies_doc = urlopen(proxies_req)

	# Save proxies in the array
	for proxy_line in proxies_doc:

		full_ip = proxy_line.decode('utf8').rstrip()
		split_ip = full_ip.split(":")
		proxies.append({
			'ip': split_ip[0],
			'port': split_ip[1]
		})

	# Choose a random proxy
	proxy_index = random_proxy(proxies)
	proxy = proxies[proxy_index]

	req = Request(url)
	req.add_header('User-Agent', ua.random)
	req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'https')

	#for n in range(1, len(proxies)): # Try all available proxies
	for n in range(1, 20): # Try max 20 times
		try:
			source = urlopen(req, timeout=5).read().decode('utf8')
			soup = BeautifulSoup(source, 'lxml')

			if carrier == "ECom Express":
				delivery_status = soup.find(id="item_status")
			else:	# Amazon 
				delivery_status = soup.find(id="primaryStatus")

			if delivery_status is not None:
				return(delivery_status.text)
			else:
				return(delivery_status)
		except Exception as e:			
			del proxies[proxy_index]
			proxy_index = random_proxy(proxies)
			proxy = proxies[proxy_index] # New proxy
			req = Request(url)
			req.add_header('User-Agent', ua.random) # New user agent
			req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'https')


# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy(proxies):
	return random.randint(0, len(proxies) - 1)


# Setup MySQL Connection
db = MySQLdb.connect(host="localhost", user="root", passwd=config.db_password, db="wheresmystuff")
cursor = db.cursor(MySQLdb.cursors.DictCursor)

query = """SELECT * FROM custom_carrier_deliveries INNER JOIN packages ON custom_carrier_deliveries.package_id = packages.id"""
cursor.execute(query)
deliveries = cursor.fetchall()

for delivery in deliveries:

	pkg_id = delivery["package_id"]
	url = delivery["tracking_url"]
	carrier = delivery["carrier"]
	old_status = str(delivery["status"])

	if "Delivered" not in old_status:

		new_status = str(get_status(url, carrier))
		if ((old_status != new_status) and (new_status != "None")):
			
			update = """UPDATE custom_carrier_deliveries SET status = %s, updated_at = %s where package_id = %s"""
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
