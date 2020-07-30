#!/usr/bin/python3

def check_amazon(tracking_code):
	
	return((str(tracking_code).startswith('TBA') or str(tracking_code).startswith('TBC') or str(tracking_code).startswith('TBM')))