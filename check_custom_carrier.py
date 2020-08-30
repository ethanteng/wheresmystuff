#!/usr/bin/python3

def check_amazon(tracking_code):
	
	return((str(tracking_code).startswith('TBA') or str(tracking_code).startswith('TBC') or str(tracking_code).startswith('TBM')))


def check_custom_carrier(tracking_code, carrier):

	return(carrier == "ECom Express" or carrier == "NZ Post" or check_amazon(tracking_code))