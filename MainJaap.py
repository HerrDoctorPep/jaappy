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

print('Website to be scraped:', URL)
print('Number of pages:', MAXPAGE)
print('Date:',TODAY)

for p in range(MAXPAGE):
    df_houses_read = ScrapeJaap.read_summary_page(URL,p+1)
    if p == 0:
        df_houses_summary = df_houses_read
    else:
        df_houses_summary = pd.concat([df_houses_summary,df_houses_read],ignore_index=True, sort =False)
     
df_houses_summary.to_csv('houses_summary_'+str(TODAY),index=False, header=True)

print('All',len(df_houses_summary), 'houses have been written to file!')
