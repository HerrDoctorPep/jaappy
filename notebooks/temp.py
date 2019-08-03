#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
First exercise of scraping with Python
By dr.Pep, all rights reserved
"""

# Built-in/Generic imports

# Libs
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import ssl
# import numpy as np
import pandas as pd

# Own modules

# Authorship
__author__ = 'dr.Pep'
__copyright__ = 'Copyright 2019, dr.Pep'
__credits__ = 'Thanks to the magnificent Py4e and PCC'
__licence__ = 'All rights reserved'
__version__ = '0.0.1'
__maintainer__ = 'dr.Pep'
__email__ = 'python@vdlaan.eu'
__status__ = 'In development'

#
# THIS IS WHERE THE FUN STARTS
#

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read the webpage
url = 'https://www.jaap.nl/koophuizen/zuid+holland/groot-rijnmond/rotterdam/'
html = urllib.request.urlopen(url,context=ctx).read()
soup = BeautifulSoup(html,'html.parser')

# The second number mentioned in page_info is the maximum number of pages
page_info = soup.find(class_ = 'page-info')
max_pages = int(re.findall('[0-9]+',page_info.contents[0])[1])

# get key data from one page

# for id and link, the straightforward regular expression approach is easiest
# as it gets rid of Ad boxes that otherwise get in the way
id_html = re.findall(b'id="(house_result_.+)"',html)
link_html = re.findall(b'<a class="property-inner" href="(.+?)\?',html)
# for other fields, beautifulsoup is the easiest solution
address_html = soup.find_all(class_ = 'property-address-street')
PC_html = soup.find_all(class_ = 'property-address-zipcity')
price_html = soup.find_all(class_ = 'property-price')
pricetype_html = soup.find_all(class_ = 'pricetype')

# check if lengths of the scraped lists matches number of houses
print (len(id_html) == len(link_html)
       & len(id_html) == len(address_html)
       & len(id_html) == len(PC_html)
       & len(id_html) == len(price_html)
       &len(id_html) == len(pricetype_html), len(id_html))

# clean scraped content
house_id = []
for id in id_html:
    house_id.append(id.decode())

link = []
for lnk in link_html:
    link.append(lnk.decode())

address = []
for addr in address_html:
    address.append(addr.contents[0])

PC = []
for code in PC_html:
    PC.append(code.contents[0])

pricetype = []
for prt in pricetype_html:
    pricetype.append(prt.contents[0])

# specific for price: get from string with € sign to integer
price = []
for prc in price_html:
    price.append(int(''.join(re.findall('[0-9]+',prc.contents[0]))))

df_house_summary = pd.DataFrame({'id': house_id, 
                                 'link': link, 
                                 'address': address, 
                                 'PC': PC, 
                                 'pricetype': pricetype, 
                                 'price': price})

print(df_house_summary)


