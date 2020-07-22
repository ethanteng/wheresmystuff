#!/usr/bin/python3
import easypost
import config

easypost.api_key = config.easypost_test_api_key
#easypost.api_key = config.easypost_prod_api_key

def create_tracker(tracking_code):

	tracker = easypost.Tracker.create(

		tracking_code=tracking_code
	)