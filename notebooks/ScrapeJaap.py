#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scraping the Jaap.nl housing site
By HerrDoctorPep
"""

# Built-in/Generic imports

# Libs
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
# import re
import ssl
import numpy as np
import pandas as pd

# Own modules

# Authorship
__author__ = 'HerrDoctorPep'
__copyright__ = 'Pepijn van de Laan, 2019'
__credits__ = 'Thanks to the magnificent Py4e and Deloitte A&C PCC'
__licence__ = 'DSB-3 clause'
__version__ = '0.1.0'
__maintainer__ = 'HerrDoctorPep'
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
url = 'https://www.jaap.nl/koophuizen/zuid+holland/groot-rijnmond/rotterdam/p1'
html = urllib.request.urlopen(url,context=ctx).read()
soup = BeautifulSoup(html,'html.parser')

# Print the anchor tags
tags = soup.find_all(class_ = 'property-address-street')

content =[]
for tag in tags:
    print(tag)
    print(tag.contents[0])
    content.append(tag.getText())

print(content)

print(type(content))

