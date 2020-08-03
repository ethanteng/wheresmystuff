#!/usr/bin/python3


# Manually entered values
tracking_code = "783361"
status = "delayed - will call to schedule delivery"
status_detail = "waiting for another item to arrive (Latta Beach Sand Dining Table for 8)"
est_delivery_date = datetime.date(2020, 8, 13)
carrier = "City Business 415-900-9118"
origin = None
destination = "SAN FRANCISCO, CA"
current_city = "SAN FRANCISCO"
current_state = "CA"
current_country = "US"
public_url = "https://www.article.com/login?next=%2Faccount"


send_email_helper.send_email(tracking_code, status, status_detail, est_delivery_date, carrier, origin, destination, current_city, current_state, current_country, public_url)