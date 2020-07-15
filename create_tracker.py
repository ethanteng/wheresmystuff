#!/usr/bin/python3
import easypost

# production key
#easypost.api_key = "EZAKd01edd046b51423e997b8bc476e0bdd9Vef6cv8HSVr9CHPH4iV6dw"

# test key
easypost.api_key = "EZTKd01edd046b51423e997b8bc476e0bdd9vQ7bjpdMMMwaRvKboxYI6A"

tracker = easypost.Tracker.create(
	tracking_code="EZ2000000002"
)
