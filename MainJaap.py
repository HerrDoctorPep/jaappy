#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Jaap.nl scraping - main script
By dr.Pep
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

#
# THIS IS WHERE THE FUN STARTS
#
