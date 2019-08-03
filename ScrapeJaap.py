#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Supporting functions for scraping jaap.nl

    - get_max_page finds the number of summary pages to be scraped
    - read_summary_page reads the houses advertised on one page

By dr.Pep, all rights reserved
"""

# Libs
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import ssl
# import numpy as np
import pandas as pd

def get_max_page(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # Scrape the page
    html = urllib.request.urlopen(url,context=ctx).read()
    soup = BeautifulSoup(html,'html.parser')
    
    page_info = soup.find('span',class_ = 'page-info')
    max_page = int(re.findall('[0-9]+',page_info.get_text())[1]) # second numer is the last page
    return max_page

def read_summary_page(url_mainpage,page_number):
    # construct page ur
    url = url_mainpage + "p" + str(page_number)
    print('Scraping webpage ....',url)
        
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # get the html 
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
       | len(id_html) != len(pricetype_html)):
        # if lengths not equal: print error message and return None
        print('ERROR: Not all scraped lists of equal length!')
        
        return {'id': len(id_html), 
                'link': len(link_html),
                'address': len(address_html),
                'PC': len(PC_html),
                'price': len(price_html),
                'pricetype': len(pricetype_html)}
    
    # clean scraped content
    house_id = []
    for id in id_html:
        house_id.append(str(id.decode()))
    
    link = []
    for lnk in link_html:
        link.append(str(lnk.decode()))
    
    address = []
    for addr in address_html:
        if len(addr.contents)>0:
            address.append(str(addr.contents[0]))
        else:
            address.append(None)
    
    PC = []
    for code in PC_html:
        if len(code.contents)>0:
            PC.append(str(code.contents[0]))
        else: 
            PC.append(None)
    
    pricetype = []
    for prct in pricetype_html:
        if len(prct.contents)>0:
            pricetype.append(str(prct.contents[0]))
        else: 
            pricetype.append(None)
    
    # specific for price: get from string with € sign to integer
    price = []
    for prc in price_html:
        if len(prc.contents)>0:
            prc_temp = re.findall('[0-9]+',prc.contents[0])
            if len(prc_temp)>0:
                price.append(int(''.join(prc_temp)))
            else:
                price.append(None)
        else: 
            price.append(None)
    
    # put the cleaned lists into a data frame
    df_house_summary = pd.DataFrame({'id': house_id, 
                                     'link': link, 
                                     'address': address, 
                                     'PC': PC, 
                                     'pricetype': pricetype, 
                                     'price': price})
    
    # return the data frame
    return df_house_summary

if __name__ == '__main__':
    print('This is a test of the function get_max_page...')
    print(get_max_page('https://www.jaap.nl/koophuizen/zuid+holland/groot-rijnmond/rotterdam/50+-woonopp/'))
    print('This is a test of the function read_summary_page...')
    df_test = read_summary_page('https://www.jaap.nl/koophuizen/zuid+holland/groot-rijnmond/rotterdam/50+-woonopp/',20)
    print(df_test)
