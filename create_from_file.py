#!/usr/bin/python3
import create_user
import create_package
import create_tracker

# New entry
email = "davidteng78@yahoo.com"
first_name = "David"
last_name = "Teng"
tracking_code = "EZ1000000001"
description = "Fake package 1"

user_id = create_user.create_user(first_name, last_name, email)
create_package.create_package(user_id, tracking_code, description)
create_tracker.create_tracker(tracking_code)