#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Supporting functions for scraping jaap.nl
By dr.Pep, all rights reserved
"""

# Libs
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import ssl
# import numpy as np
import pandas as pd

def read_summary_page(url_mainpage,page_number):
    # construct page ur
    url = url_mainpage + "p" + str(page_number)
        
    # get the html 
    # context already set 
    html = urllib.request.urlopen(url,context=ctx).read()
    soup = BeautifulSoup(html,'html.parser')
    
    # for id and link, the straightforward regular expression approach is easiest
    # as it gets rid of Ad boxes that otherwise get in the way
    id_html = re.findall(b'id="(house_result_.+)"',html)
    link_html = re.findall(b'<a class="property-inner" href="(.+?)\?',html)
    
    # for other fields, beautifulsoup is the easiest solution
    address_html = soup.find_all(class_ = 'property-address-street')
    PC_html = soup.find_all(class_ = 'property-address-zipcity')
    price_html = soup.find_all(class_ = 'property-price')
    pricetype_html = soup.find_all(class_ = 'pricetype')
    
    # test if all scraped lists have equal length
    if (len(id_html) != len(link_html)
       | len(id_html) != len(address_html)
       | len(id_html) != len(PC_html)
       | len(id_html) != len(price_html)
       | len(id_html) != len(pricetype_html), len(id_html)):
        # if lengths not equal: print error message and return None
        print('ERROR: Not all scraped lists of equal length!')
        return None        
    
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
    
    # put the cleaned lists into a data frame
    df_house_summary = pd.DataFrame({'id': house_id, 
                                     'link': link, 
                                     'address': address, 
                                     'PC': PC, 
                                     'pricetype': pricetype, 
                                     'price': price})
    
    # return the data frame
    return df_house_summary


