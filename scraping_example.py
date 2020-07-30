#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import lxml

source = requests.get('https://www.amazon.com/progress-tracker/package/ref=pe_386300_442618370_scr_pt_asin?_encoding=UTF8&from=gp&itemId=&orderId=112-1436433-3901035&packageIndex=0&shipmentId=36692701829301').text
soup = BeautifulSoup(source, 'lxml')

#print(soup.prettify())
delivery_status = soup.find(id="primaryStatus")
print(delivery_status.text)