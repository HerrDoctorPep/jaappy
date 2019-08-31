#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Jaap.nl scraping - main script
By dr.Pep
"""

# Built-in/Generic imports

# Libs
import time
# import numpy as np
import pandas as pd
import logging

# Own modules

import ScrapeJaap

# Authorship
__author__ = 'dr.Pep'
__copyright__ = 'Copyright 2019, dr.Pep'
__credits__ = 'Thanks to the magnificent Py4e and PCC'
__licence__ = 'All rights reserved'
__version__ = '0.0.1'
__maintainer__ = 'dr.Pep'
__email__ = 'python@vdlaan.eu'
__status__ = 'In development'

# Set some constants

URL = 'https://www.jaap.nl/koophuizen/zuid+holland/groot-rijnmond/rotterdam/50+-woonopp/' # The jaap.nl main page for scraping (Rotterdam, 50m²+)
MAXPAGE = ScrapeJaap.get_max_page(URL) # The number of summary pages to be scraped
TODAY = time.strftime("%Y%m%d") # The current date in the standard format YYYYMMDD
PROJECTDATA = 'data\\processed\\'
LOGFILE = 'data\\raw\\log_'+TODAY+'.txt'

logging.basicConfig(filename=LOGFILE,level=logging.DEBUG)
logging.info('Time stamp: '+str(time.asctime()))
logging.info('Website to be scraped: '+str(URL))
logging.info('Number of pages: '+str(MAXPAGE))

for p in range(MAXPAGE):
    print('Scraping summary page '+str(p))
    df_houses_read = ScrapeJaap.read_summary_page(URL,p+1)
    if p == 0:
        df_houses_summary = df_houses_read
    else:
        df_houses_summary = pd.concat([df_houses_summary,df_houses_read],
                                      ignore_index=True,
                                      sort =False)         
df_houses_summary.to_csv(PROJECTDATA+'houses_summary_'+str(TODAY)+'.csv',
                         index=False,
                         header=True)
logging.info('Summary of all',len(df_houses_summary), 'houses have been written to file!')


for i in df_houses_summary.index:
    print('Scraping detail page '+ str(i))
    df_detail_read = ScrapeJaap.read_house_detail_page(df_houses_summary['link'][i],
                                                       df_houses_summary['pricetype'][i],
                                                       df_houses_summary['id'][i])
    # Some error handling - when page cannot be read
    if type(df_detail_read) == bool:
        logging.warning('Index:' + str(i) 
           + ' | Address:' + str(df_houses_summary['address'][i]) 
           + ' | ID:'+ str(df_houses_summary['id'][i]) + ' | Scraping failed')
        continue
    # Put the scraped data into a data frame
    if i == 0:
        df_houses_detail = df_detail_read
    else:
        df_houses_detail= pd.concat([df_houses_detail,df_detail_read],ignore_index=True, sort =False)
df_houses_detail.to_csv(PROJECTDATA + 'houses_detail_' + str(TODAY)+'.csv',
                        index=False,
                        header=True)
logging.info('Detail of'+str(len(df_houses_detail))+'houses have been written to file!')
