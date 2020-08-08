#!/usr/bin/python3
import easypost
import config

easypost.api_key = None
if config.env == "test":
	easypost.api_key = config.easypost_test_api_key
else:
	easypost.api_key = config.easypost_prod_api_key

def create_tracker(tracking_code, carrier):

	try:
		if (carrier is None):
			tracker = easypost.Tracker.create(

				tracking_code=tracking_code
			)
		else:
			tracker = easypost.Tracker.create(

				tracking_code=tracking_code,
				carrier=carrier
			)
	except easypost.Error as e:
		print("Error while creating EasyPost tracker for: " + str(tracking_code))
		print(e.json_body["message"])