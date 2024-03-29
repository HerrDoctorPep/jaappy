#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Jaap.nl scraping - main script
By dr.Pep
"""

# Built-in/Generic imports

# Libs
# import time
# import numpy as np
from datetime import date, datetime
import pandas as pd
import logging
import os, uuid, sys
# from azure.storage.blob import BlockBlobService, PublicAccess, ContentSettings

# Own modules

import ScrapeJaap
from MyConstants import * # This way you get the constants without filename as prefix

# Authorship
__author__ = 'dr.Pep'
__copyright__ = 'Copyright 2019, dr.Pep'
__credits__ = 'Thanks to the magnificent Py4e and PCC'
__licence__ = 'All rights reserved'
__version__ = '0.0.1'
__maintainer__ = 'dr.Pep'
__email__ = 'python@vdlaan.eu'
__status__ = 'In development'

# Set up logging
logging.basicConfig(filename = LOGDATA + LOGFILE,
                    level = logging.DEBUG)
logging.info('Running script MainJaap.py | Time stamp: ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
logging.info('Website to be scraped: ' + str(URL))
logging.info('Number of pages: ' + str(MAXPAGE))

# Scrape all summary pages
for p in range(MAXPAGE):
    # Log where we are
    # logging.info('Scraping summary page ' + str(p+1))
    # Read page
    df_houses_read = ScrapeJaap.read_summary_page(URL,p+1)
    if p == 0:
        df_houses_summary = df_houses_read
    else:
        df_houses_summary = pd.concat(
            [df_houses_summary,df_houses_read],
            ignore_index=True,
            sort =False
        )         

# Write summary to file
df_houses_summary.to_csv(PROJECTDATA + SUMMARYFILE,index=False,header=True)

logging.info('Summaries of all ' + str(len(df_houses_summary)) + ' houses have been written to file!')

# Scrape all detail pages
for i in df_houses_summary.index:
    # Start with logging where we are
    # logging.info('Scraping detail page '+ str(i))

    # Read the page with details
    df_detail_read = ScrapeJaap.read_house_detail_page(
        df_houses_summary['link'][i],
        df_houses_summary['pricetype'][i],
        df_houses_summary['id'][i]
    )

    # Some error handling - when page cannot be read
    if type(df_detail_read) == bool:
        logging.warning(
            'Index:' + str(i) 
            + ' | Address:' + str(df_houses_summary['address'][i]) 
            + ' | ID:'+ str(df_houses_summary['id'][i]) + ' | Scraping failed'
        )
        continue
    
    # Put the scraped data into a data frame
    if i == 0:
        df_houses_detail = df_detail_read
    else:
        df_houses_detail= pd.concat(
            [df_houses_detail,df_detail_read],
            ignore_index=True, 
            sort =False
        )

# Write data frame with all house details to file
df_houses_detail.to_csv(PROJECTDATA + DETAILFILE,index=False,header=True)

# Log our success
logging.info('Details of '+str(len(df_houses_detail))+' houses have been written to file!')

# Write Summary and Detail files to blobs
# THE BELOW DOES NOT WORK WITHOUT SAS TOKEN (currently empty)
#
# blob_service = BlockBlobService(account_name = ACCOUNT_NAME, account_key = None, sas_token = SAS_TOKEN)
#
# blob_service.create_blob_from_path(
#     CONTAINER_NAME, 
#     LOGFILE, 
#     RAWDATA + LOGFILE)
# blob_service.create_blob_from_path(
#     CONTAINER_NAME, 
#     SUMMARYFILE, 
#     PROJECTDATA + SUMMARYFILE)
# blob_service.create_blob_from_path(
#     CONTAINER_NAME, 
#     DETAILFILE, 
#     PROJECTDATA + DETAILFILE)
