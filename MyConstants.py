# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 21:52:04 2019

@author: Pep
"""

import ScrapeJaap
from datetime import date, datetime
# Scrape stuff
URL = 'https://www.jaap.nl/koophuizen/zuid+holland/groot-rijnmond/rotterdam/50+-woonopp/' # The jaap.nl main page for scraping (Rotterdam, 50m²+)
PROJECTDATA = 'data/processed/'
LOGDATA = 'data/logs/'

# Inferrred constants

MAXPAGE = ScrapeJaap.get_max_page(URL) # The number of summary pages to be scraped
TODAY = date.today().strftime("%Y%m%d") # The current date in the standard format YYYYMMDD
LOGFILE = 'log_'+TODAY+'.txt'
SUMMARYFILE = 'houses_summary_'+str(TODAY)+'.csv'
DETAILFILE = 'houses_detail_' + str(TODAY)+'.csv'

# Azure stuff
ACCOUNT_NAME = 'dorpsstraat'
CONTAINER_NAME = 'schraper-data'
SAS_TOKEN = '' # need to add SAS token locally
