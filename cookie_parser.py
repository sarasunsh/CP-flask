# -*- coding: utf-8 -*-
"""

@author: SSunshine
"""
# Third Party Library Imports
import re

# Function to convert the cookies obtained as a string from Chrome into dictionary
def cookie_parser(raw_cook):
    raw_cook = raw_cook.replace('ViZGU1In0=;','ViZGU1In0;')
    cook_list = re.split('=|;', raw_cook)
    i = 0
    COOKIES = {}
    while i < (len(cook_list) - 1):
        if i%2==0:
            COOKIES[cook_list[i]] = cook_list[i+1]
        i +=1

    return COOKIES