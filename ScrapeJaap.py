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
# import time
import datetime #NEW
import logging

# Take a string, strip the non-numbers, convert to integer
# Usable not just for prices, but also for other figures
def char_as_int(price_as_string):
    price_temp = re.findall('[0-9]+',price_as_string)
    if len(price_temp)>0:
        house_price = int(''.join(price_temp))
    else:
        house_price = None
    return house_price


def get_max_page(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # Scrape the page
    # Works for main page after a search on Jaap.nl
    html = urllib.request.urlopen(url,context=ctx).read()
    soup = BeautifulSoup(html,'html.parser')
    
    # Extract max page numebr from "Page 1 of [0-9]+"
    page_info = soup.find('span',class_ = 'page-info')
    max_page = int(re.findall('[0-9]+',page_info.get_text())[1]) # second numer is the last page
    return max_page

# Read a given result page (number)
def read_summary_page(url_mainpage,page_number):
    # construct page url
    url = url_mainpage + "p" + str(page_number)
    # logging.info('Scraping webpage '+str(url))
        
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
        logging.error('ERROR: Not all scraped lists of equal length!')
        
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
            price.append(char_as_int(prc.contents[0]))
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

# Give in url and pricetype to create dict with house details
def read_house_detail_page(url_detail_page,pricetype,ID):
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # get the html 
    try:
        html = urllib.request.urlopen(url_detail_page,context=ctx).read()
        soup = BeautifulSoup(html,'html.parser')
    except:
        return False
    # Get the basic info also from this page

    # Construct sub-tree of DOM to facilitate finding pricetype and sold
    detail_html = soup.find(class_ = 'detail-address')
    
    # characteristics stored in specific nodes; pricetype is empty
#    pricetype_html = detail_html.findChildren('span')[0]
    sold_html = detail_html.findChildren('span') # Produces error if not 'Verkocht (onder voorbehoud)'
    address_html = soup.find(class_ = 'detail-address-street') 
    zip_html = soup.find(class_ = 'detail-address-zipcity')
#    price_html = soup.find(class_ = 'detail-address-price')
    short_descr_html = soup.find(class_ = 'short-description')
    long_descr_html = soup.find(class_ = 'description')
    broker_html = soup.find(class_ = 'broker-name')
    
    # list of characteristics and metrics in array
    characteristics_html = soup.find_all(class_ = 'no-dots')
    metrics_html = soup.find_all(class_ = 'value')
     
#    # Need to restrict to first 27 (found by exploring all)
    n_char = 26
    
    # Now there is some cleaning to do...
    
    #make characteristics and metrics into a dictionary
    house_char_names = []
    for c in characteristics_html[0:n_char]:
        house_char_names.append(c.contents[0].replace(' ','_'))
    
    house_char_metrics = []
    for m in metrics_html[0:n_char]:
        house_char_metrics.append(m.contents[0].strip())
    
    house_characteristics = dict(zip(house_char_names,house_char_metrics))
    
    # Clean dictionary contents
    
    house_characteristics['Bouwjaar'] = char_as_int(house_characteristics['Bouwjaar'])
    house_characteristics['Woonoppervlakte'] = char_as_int(house_characteristics['Woonoppervlakte'])
    house_characteristics['Inhoud'] = char_as_int(house_characteristics['Inhoud'])
    house_characteristics['Perceeloppervlakte'] = char_as_int(house_characteristics['Perceeloppervlakte'])
    house_characteristics['Kamers'] = char_as_int(house_characteristics['Kamers'])
    house_characteristics['Slaapkamers'] = char_as_int(house_characteristics['Slaapkamers'])
    house_characteristics['Aantal_keer_getoond'] = char_as_int(house_characteristics['Aantal_keer_getoond'])
    house_characteristics['Aantal_keer_getoond_gisteren'] = char_as_int(house_characteristics['Aantal_keer_getoond_gisteren'])
    house_characteristics['Huidige_vraagprijs'] = char_as_int(house_characteristics['Huidige_vraagprijs'])
    house_characteristics['Oorspronkelijke_vraagprijs'] = char_as_int(house_characteristics['Oorspronkelijke_vraagprijs'])
    house_characteristics['Geplaatst_op'] = datetime.datetime.strptime(house_characteristics['Geplaatst_op'], "%d-%m-%Y").date()
    # Add other data points 
    # try-except for the ones that might be empty
    try:
        house_characteristics['Short_description'] = short_descr_html.get_text().strip().replace('\n', ' ').replace('\r', ' ')
    except:
        house_characteristics['Short_description'] = None
    try:
        house_characteristics['Long_description'] = long_descr_html.get_text().strip().replace('\n', ' ').replace('\r', ' ')
    except:
        house_characteristics['Long_description'] = None
    try:
        house_characteristics['Broker'] = broker_html.contents[0].strip()
    except:
        house_characteristics['Broker'] = None    
    try:
        house_characteristics['Address'] = address_html.contents[0]
    except:
        house_characteristics['Address'] = None
    try:
        house_characteristics['Zip'] = zip_html.contents[0]
    except:
        house_characteristics['Zip'] = None
    # For sold we need to be careful because field is missing when not sold
    if len(sold_html) < 2:
        house_characteristics['Sold'] = 'Te koop'
    else:
        house_characteristics['Sold'] = detail_html.findChildren('span')[1].contents[0].strip()
    # pricetype is empty, so we get it from the summary page
    house_characteristics['Pricetype'] = pricetype
    # we drag along house id to have a key to the summary info
    house_characteristics['ID'] = ID
    # price is the same as Huidige_vraagprijs, so we omit it

    return pd.DataFrame([house_characteristics])

if __name__ == '__main__':
    print('This is a test of the function get_max_page...')
    print(get_max_page('https://www.jaap.nl/koophuizen/zuid+holland/groot-rijnmond/rotterdam/50+-woonopp/'))
    print('This is a test of the function read_summary_page...')
    df_test = read_summary_page('https://www.jaap.nl/koophuizen/zuid+holland/groot-rijnmond/rotterdam/50+-woonopp/',20)
    print(df_test)
