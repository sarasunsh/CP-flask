# -*- coding: utf-8 -*-
"""

@author: SSunshine
"""

# Third Party Library Imports
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, time, timedelta

#Local package imports
from countdown import countdown
from cookie_parser import cookie_parser

# Data needed for requests to server
studio_URL = "https://classpass.com/a/VenueClassSchedule"
fave_URL = "https://classpass.com/favorites"
upcoming_URL = "https://classpass.com/upcoming"
signup_URL = "https://classpass.com/a/PassportReserveDialog"

raw_cook = '__cfduid=d6e427245483d3e8ebe91b77c89b0edf21403099090103; km_ai=AsqNnwuqhKFg0io8vbrqZEZf2M4%3D; km_lv=x; TrackJS=5f317f37-5b03-4966-9bac-cb8a5ab83e01; _hp2_id.1165694113=2478143952259425.0739197400.2191247799; km_uq=; optimizelyEndUserId=oeu1422464448920r0.9521982800215483; __ar_v4=4FVLTQMN6JG6JOZ7FW6XXC%3A20150225%3A204%7CLMDV4NAO45EOZLWOSAQ5LJ%3A20150225%3A253%7CKJDLOVCT6VF4TBYXFFRSW3%3A20150225%3A253%7CLX4JV2JFOJEQBCLI4P74B5%3A20150315%3A8; _hp2_id.3868021954=6349802044283751.3780338889.1752130478; __insp_slim=1458137781396; __insp_wid=324523599; __insp_nv=true; __insp_ref=d; __insp_targlpu=https%3A%2F%2Fclasspass.com%2F; __insp_targlpt=ClassPass; __insp_norec_sess=true; cpExperimentId=56; fs_uid=www.fullstory.com`174QC`5137659743698944:5629499534213120`37181`false; sailthru_hid=9fcf94234a5f45ec8b2a806ffd511e3f548099032912ffa80a8b57e07101ad1fa4e325a0524db63ce59d0c40; cpVisitorId=654614771553664e8d2dbf; cpGuestView=6; cpBasePlan=15; cpCohort=false_base_2; cpUtmValues={"initial_url":"/start/new-york"}; bounceClientVisit1678v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgMZgCGKKEFKAdMQPYC2RKCZATgkQHYCmAdwC0ATwYcA1iAA0IDjBAgAvkA; cpUser=ZTU0OWU2ZTJkYWQzOWMyYzNmYmI0NzEzYTkxOTYwZWQwYmRkMTRjNTJiNWRjNTI3ODQ5YWY0M2U5MTRmNjU4Nw%3D%3D%7CMzcxODE%3D; cpSearchStudios=list_view; classpass=262b751751c15eaed3349450086d2f66; _gat=1; cpUserType=subscribed; optimizelySegments=%7B%222331020308%22%3A%22false%22%2C%222347780571%22%3A%22gc%22%2C%222362360229%22%3A%22direct%22%2C%223537322437%22%3A%22none%22%7D; optimizelyBuckets=%7B%223544160422%22%3A%220%22%2C%225988150335%22%3A%225977650583%22%2C%226157120793%22%3A%226153880753%22%7D; _ga=GA1.2.345824304.1403099091; _fbuy=065a0850555f0e51195f080505140c56070b150d030f0d19050c5b0c055d5e0c000d0b01; __srret=1; _fbuy_buckets=%7B%22bsy-f4y%22%3A%5B22716%2C1462979494108%5D%2C%22bsy-g9v%22%3A%5B26867%2C1466435077644%5D%7D; mp_13a079f3c862893a971ff2215ef81c76_mixpanel=%7B%22distinct_id%22%3A%20%2237181%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22utm_source%22%3A%20%22classpass%22%2C%22utm_medium%22%3A%20%22email%22%2C%22utm_campaign%22%3A%20%22Email%22%2C%22utm_content%22%3A%20%228212%22%2C%22msa_id%22%3A%20%221%22%2C%22msa_name%22%3A%20%22New%20York%20Metro%22%2C%22user_type%22%3A%20%22subscribed%22%2C%22count_lifetime_visits%22%3A%2012%2C%22first_visit_date%22%3A%20%222015-12-23%22%2C%22guest_view%22%3A%20%22false_base_2%22%2C%22user_id%22%3A%20%2237181%22%2C%22session_start_count%22%3A%2021%2C%22app_platform%22%3A%20%22web%22%2C%22device_type%22%3A%20%22desktop%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22Optimizely%20NYC%20Base%20Promo%20Sellpage%20-%205.12%20-%20FINAL%22%3A%20%22Graphical%20v2%22%2C%22Optimizely%20NYC%20Base%20Promo%20Sellpage%20-%205.19%20-%20Phase%20II%22%3A%20%22Ribbon%20v2%22%2C%22Optimizely%20Plan%20Pricing%20Ribbon%20-%20%2475%20NYC%20-%206.6%20-%20JC%22%3A%20%22Original%22%7D; __zlcmid=U1eXk35cY2NdnN; bounceClientVisit1678=N4IgzglgJiBcBMAOANCAZgNwC5wIwBYBWQgdnnjJRA2j3wDZ78BmfXQ-E3XEk51AIYB7OPEFg4ABlQYADhlG5UMWCBioANrLggAFliyywAUmYBBY-ABilqwGMNAsGFlOwAOjtCAtrbBYBACcsWwA7AFMAdwBaAE8hQIBrEFRAnRSQO2w6RhY2DlQAczs02Hp+EG8pZVpVcslJQkRESU5EUkRcekQ+DI1s2AJc5kJJFpk4UABXMHDAgH1w7wEIDTg0AQ1Z1AAvCFl5ryhw9c3tkHCMOfmNIULC8Kh5iFC4LECp8NRlg-8pqAgQjAhyEU1COFg0kqAgOdggWFi81CAm8J1UADkogACACaCWSqBm1wRsjR4CmACMwCUIBTHhkoAIAvNvGABId4YjkaidJjIrj8ViALLhd4iZRM9ms9kUoRQREONw6WSBIRoVbhMBY2Xy6LRY4BVbauWxPX+CB2RKmtBCIRYOZY1zOWQJHAAX1QdhRrgghVCElgAG0ALqoXR2ea6Hxo3BuoA; optimizelyPendingLogEvents=%5B%5D; mp_mixpanel__c=2; mp_mixpanel__c3=3770; mp_mixpanel__c4=3641; mp_mixpanel__c5=18'
COOKIES = cookie_parser(raw_cook)

# Function to pull specific studio's schedule
def studio_soupify(venue_id):
    next_week = datetime.now() + timedelta(days=6)
    week = next_week.strftime("20%y-%m-%d")

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
    # Get next week's schedule from studio page given venue_id and next week date
    studio_html = requests.post(
        studio_URL,
        data=payload,
        cookies=COOKIES
    )

    # Parse html to find schedule details
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

    # Pull list of favorite studios from ClassPass
    fave_html = requests.get(
        fave_URL,
        cookies=COOKIES
    )

    # Parse html to find studio details
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
    payloads = {}
    for workout in classes_in_cart:
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

    today = datetime.combine(date.today(), time(16, 22, 00))
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

# Function to check 'upcoming' page for which classes successfully signed up 
def check_upcoming(classes_in_cart):

    # Pull list of upcoming classes from ClassPass
    upcoming_html = requests.get(
        upcoming_URL,
        cookies=COOKIES
    )   

    # Parse html to find reservation details
    reserved_deets = BeautifulSoup(upcoming_html.content, "lxml")
    reservations = reserved_deets.find_all('a', class_='bt bt--outlined-warning js-cancel-reservation')
    reserved_sched_ids = [int(r.get('data-schedule-id')) for r in reservations]

    #Check which classes from those in the cart are found on 'Upcoming' page
    success = [workout for workout in classes_in_cart if workout[2] in reserved_sched_ids]
    return success

# Function to convert class details obtained as a string back into a list 
def clean_class(raw_class):
    clean = raw_class[2:-2].replace("', '", ",")
    final = clean.split(",")
    final[0], final[2], final[6] = int(final[0]), int(final[2]), int(final[6])
    return final
