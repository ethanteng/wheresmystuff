#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import lxml
from urllib.request import Request, urlopen
from fake_useragent import UserAgent

#source = requests.get('https://www.amazon.com/progress-tracker/package/ref=pe_386300_442618370_scr_pt_asin?_encoding=UTF8&from=gp&itemId=&orderId=112-1436433-3901035&packageIndex=0&shipmentId=36692701829301').text
#soup = BeautifulSoup(source, 'lxml')

#print(soup.prettify())
#delivery_status = soup.find(id="primaryStatus")
#print(delivery_status.text)

ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]

proxies_req = Request('http://list.didsoft.com/get?email=ethanteng@gmail.com&pass=8jqn3w&pid=http3000&showcountry=no&https=yes')
proxies_req.add_header('User-Agent', ua.random)
proxies_doc = urlopen(proxies_req)

for proxy_line in proxies_doc:
	full_ip = proxy_line.decode('utf8').rstrip()
	print(full_ip)
	split_ip = full_ip.split(":")
	ip = split_ip[0]
	port = split_ip[1]
	print("ip " + ip + " port " + port)