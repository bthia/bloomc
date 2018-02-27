#!/bin/sh

#  itemprop_sm.py
#  
#
#  Created by Boon Sing Thia on 27/2/18.
#  

import requests
from bs4 import BeautifulSoup as bs

urlstring = "https://www.bloomberg.com/quote/700:HK"

response = requests.get(urlstring)

htmltext = response.text

html = bs(htmltext,"lxml")

quoteinfo = html.select_one("div.schema-org-financial-quote") # the tag with class

data = quoteinfo.select("meta")

results = [{i['itemprop']:i['content']} for i in data]

print(results)
