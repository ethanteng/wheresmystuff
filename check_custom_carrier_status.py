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
from scraper_api import ScraperAPIClient
import requests


def get_status(url, carrier):

	try:
		if carrier == "ECom Express":
			proxies = {
			  "http": "http://scraperapi:" + config.scraperapi_api_key + "@proxy-server.scraperapi.com:8001",
			  "https": "http://scraperapi:" + config.scraperapi_api_key + "@proxy-server.scraperapi.com:8001"
			}
			result = requests.get(url, proxies=proxies, verify=False).text
			soup = BeautifulSoup(result, 'lxml')
			delivery_status = soup.find(id="item_status")
		elif carrier == "NZ Post":
			proxies = {
			  "http": "http://scraperapi.render=true:" + config.scraperapi_api_key + "@proxy-server.scraperapi.com:8001",
			  "https": "http://scraperapi.render=true:" + config.scraperapi_api_key + "@proxy-server.scraperapi.com:8001"
			}
			result = requests.get(url, proxies=proxies, verify=False).text
			soup = BeautifulSoup(result, 'lxml')
			delivery_status = soup.find(class_="timeline-status")
		elif carrier == "HK Post":
			proxies = {
			  "http": "http://scraperapi.render=true:" + config.scraperapi_api_key + "@proxy-server.scraperapi.com:8001",
			  "https": "http://scraperapi.render=true:" + config.scraperapi_api_key + "@proxy-server.scraperapi.com:8001"
			}
			result = requests.get(url, proxies=proxies, verify=False).text
			soup = BeautifulSoup(result, 'lxml')
			delivery_status = soup.find(class_="message")
		elif carrier == "AliExpress":
			proxies = {
			  "http": "http://scraperapi.render=true:" + config.scraperapi_api_key + "@proxy-server.scraperapi.com:8001",
			  "https": "http://scraperapi.render=true:" + config.scraperapi_api_key + "@proxy-server.scraperapi.com:8001"
			}
			result = requests.get(url, proxies=proxies, verify=False).text
			soup = BeautifulSoup(result, 'lxml')
			delivery_status = soup.find(class_="waybill_title")
		else:	# Amazon 
			proxies = {
			  "http": "http://scraperapi:" + config.scraperapi_api_key + "@proxy-server.scraperapi.com:8001",
			  "https": "http://scraperapi:" + config.scraperapi_api_key + "@proxy-server.scraperapi.com:8001"
			}
			result = requests.get(url, proxies=proxies, verify=False).text
			soup = BeautifulSoup(result, 'lxml')
			delivery_status = soup.find(id="primaryStatus")

		if delivery_status is not None:
			return(delivery_status.text)
		else:
			return(delivery_status)
	except Exception as e:			
		print(e)


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
			carrier = delivery["carrier"]
			status = new_status
			public_url = url

			send_email_helper.send_email(tracking_code, status, status_detail, est_delivery_date_obj, carrier, origin, destination, current_city, current_state, current_country, public_url)
