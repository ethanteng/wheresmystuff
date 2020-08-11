#!/usr/bin/python3
import requests

response = requests.get(
    "https://www.amazon.com/progress-tracker/package/ref=pe_386300_442618370_scr_pt_asin?_encoding=UTF8&from=gp&itemId=&orderId=112-1436433-3901035&packageIndex=0&shipmentId=36692701829301",
    proxies={
        "http": "http://5fcc3abbe92641d5ad85bea1703f35ea:@proxy.crawlera.com:8010/",
    },
)
print(response.text)