# -*- coding: utf-8 -*-
"""

@author: SSunshine
"""

# Third Party Library Imports
import requests
import re
from bs4 import BeautifulSoup
from datetime import date, datetime, time, timedelta

#Local package imports
from countdown import countdown

# Data needed for requests to server
studio_URL = "https://classpass.com/a/VenueClassSchedule"
fave_URL = "https://classpass.com/favorites"
signup_URL = "https://classpass.com/a/PassportReserveDialog"
raw_cook = ''

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

# Function to pull specific studio's schedule
def studio_soupify(venue_id):
    next_week = datetime.now() + timedelta(days=6)
    week = next_week.strftime("20%y-%m-%d")
    COOKIES = cookie_parser(raw_cook)

    payload = {
        'venue_id':venue_id, 
        'passport':1,
        'passport_sell':0,
        'passport_reservable':1,
        'passport_status':'default',
        'passportType':'CLASSPASS',
        'week_date': week,
        'direction':'next',
        'less_days':7,
    }

    studio_html = requests.post(
        studio_URL,
        data=payload,
        cookies=COOKIES
    )

    soup = BeautifulSoup(studio_html.content, "lxml")
    studio_classes = soup.find_all("li", class_="venue-class clearfix inactive")

    classes = []
    for available_class in studio_classes:
        classes.append([
            available_class.get('data-class-id'),
            available_class.get('data-class-name'),
            available_class.get('data-schedule-id'),
            available_class.get('data-start-time'),
            available_class.get('data-end-time'),
            available_class.get('data-class-date'),
            venue_id
        ])

    return classes

# Function to pull list of favorite studios
def fave_soupify():
    COOKIES = cookie_parser(raw_cook)

    # Pull list of favorite studios from ClassPass
    fave_html = requests.get(
        fave_URL,
        cookies=COOKIES
    )

    studio_deets = BeautifulSoup(fave_html.content, "lxml")
    favorites = studio_deets.find_all("li", class_="grid__item md-1/2 lg-1/3")
    studio_dict = {}
    for fave in favorites:
        blurb = fave.find("h2")
        url = blurb.a["href"].split("/")
        venue_id = fave.find("a").get("data-venue-id")
        studio_dict[url[-1]] = venue_id

    return studio_dict

# Function to handle sign-up process
def sign_up(classes_in_cart):
    COOKIES = cookie_parser(raw_cook)
    payloads = {}
    for workout in classes_in_cart:
        print workout       
        payloads[workout[1]] =  {
            'schedule_id': workout[2], 
            'class_id': workout[0],
            'venue_id': workout[6],
            'mode': 'confirm',
            'user_id': 37181,
            'passport_venue_attended': 0,
            'passportType': 'CLASSPASS',
            'passportUsersId': 16661,
        }

    today = datetime.combine(date.today(), time(12, 00, 10))
    subject = "Classpass Signups Open"
    countdown(today, "ClassPass Signups Open")
    print('Classes are open! Signing up for classes now!')

    for class_name, class_payload in payloads.iteritems():
        print('Signing up for class: {0}'.format(class_name))
        _ = requests.post(
            signup_URL,
            data=class_payload,
            cookies=COOKIES,
        )

# Function to convert class details obtained as a string back into a list 
def clean_class(raw_class):
    clean = raw_class[2:-2].replace("', '", ",")
    final = clean.split(",")
    final[0], final[2], final[6] = int(final[0]), int(final[2]), int(final[6])
    return final
