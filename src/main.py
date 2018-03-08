from bs4 import BeautifulSoup
import urllib
import requests
import json
import re
import time as sleep

from dataClasses import User
from dataClasses import Business
from dataClasses import Review


def website_parse(url, bussinessID):
    sleep.sleep(6)
    print(url)
    #Initialise dictionary to be returned
    data_dict = {}
    response_page = urllib.request.urlopen(url)
    html_page = response_page.read()
    soup = BeautifulSoup(html_page, 'html.parser')

    # Retrieve all other required info from 'More Business info'
    div = soup.find_all('div', {'class': 'ywidget'})
    span = soup.find_all('a', {'target': '_blank', 'rel': 'noopener'}, href=re.compile("website_link"))

    #this gets address from website
    address = soup.find_all('address')
    if address.len == 3:
        address = address[1].contents[0].strip()
        data_dict['Address'] = address
    else:
        data_dict['Address'] = ''

    #this gets the official website if it exist
    data_dict['URL'] = ''
    for thisSpan in span:
        data_dict['URL'] = thisSpan.contents[0]

    #this retrieves other website stuff
    for each_div in div:
        req_text = each_div.find(text='More business info')
        if req_text:

            #Retrieve the price range
            price = soup.find('dd', {'class': 'nowrap price-description'})
            if price:
                data_dict['Price'] = price.text.strip()
            else:
                data_dict['Price'] = ''

            #Retrieve the hours
            hours = soup.find('div', {'class': 'ywidget biz-hours'})
            if hours:
                hours_table = hours.find('table', {'class': 'table table-simple hours-table'})
                if hours_table:
                    hours_row = hours_table.find_all('tr')
                    if hours_row:
                        req_hours=''

                        for each in hours_row:
                            hours_day = each.find('th')
                            hours_time = each.find('td')
                            time = ''
                            each_seg = hours_time.find_all('span', {'class': 'nowrap'})
                            for each_part in each_seg:
                                time = time + '-' + each_part.text.strip()
                            req_hours = req_hours + hours_day.text.strip() + time + ' '

                        data_dict['Hours'] = req_hours.strip()
                    else:
                        data_dict['Hours'] = ''
                else:
                    data_dict['Hours'] = ''
            else:
                data_dict['Hours'] = ''

            req_div = each_div
            req_data = req_div.find_all('dl')

            for each in req_data:
                a = each.find('dt').text
                b = each.find('dd').text

                key = a.strip()

                if key not in data_dict:
                    data_dict[key] = []
                data_dict[key] = b.strip()

            # Retrieve author and review details
            review_div = soup.find('div', {'class': 'review-list'})
            review_li = review_div.find_all('li')

            for each_li in review_li[1:]:
                userID_div = each_li.find_all('div', {'class': 'review review--with-sidebar'})
                if (userID_div):
                    id = (userID_div)[0]['data-signup-object']
                    req_id = id[8:]
                    authors.write(req_id)
                    authors.write(',')

                    name = userID_div[0].find_all('li', {'class': 'user-name'})
                    name1 = name[0].find_all('a')
                    authors.write(name1[0].text.strip())
                    authors.write(',')

                    location = userID_div[0].find_all('li', {'class': 'user-location'})
                    if (location):
                        authors.write(location[0].text.strip().replace(',', ''))
                        authors.write(',')
                    else:
                        authors.write(',')

                    review_count = userID_div[0].find_all('li', {'class': 'review-count'})
                    if (review_count):
                        authors.write(review_count[0].text.strip()[0:-8])
                        authors.write(',')
                    else:
                        authors.write(',')

                    friend_count = userID_div[0].find_all('li', {'class': 'friend-count'})
                    if (friend_count):
                        authors.write(friend_count[0].text.strip()[0:-8])
                        authors.write(',')
                    else:
                        authors.write(',')

                    photo_count = userID_div[0].find_all('li', {'class': 'photo-count'})
                    if (photo_count):
                        authors.write(photo_count[0].text.strip()[0:-7])
                        authors.write('\n')
                    else:
                        authors.write('\n')

            return data_dict


if __name__ == '__main__':

    #this opens or creates author.csv , review.csv, restaurant.csv
    authors = open('user.csv', 'w')
    reviews = open('review.csv', 'w')
    restaurant = open('restaurant.csv', 'w')

    #used to get inputs from attributes.json
    attributes_File = open('attributes.json', 'r').read()
    attributes = json.loads(attributes_File)
    locationSize = attributes['location']['size']

    #counters
    size = 0
    offset = 0
    totalSize = 0

    #empty api format
    url = 'https://api.yelp.com/v3/businesses/search?offset={}&limit=50&categories={}&location={}'
    header = '"Authorization": "Bearer {}"'

    #filled api information to make a call
    urlNew = url.format(str(offset), attributes['categories'], attributes['location']['list'][size])
    headerNew = '{' + header.format(attributes['api_key']) + '}'
    headerNew = json.loads(headerNew)

    websiteData = urllib.request.Request(urlNew, headers=headerNew, method='GET')
    websiteData = urllib.request.urlopen(websiteData).read().decode('utf8')
    listOfBusinesses = json.loads(websiteData)

    #used to track index and if it should keep on trying to make calls to api.yelp
    totalSize = listOfBusinesses['total']

    #totalSize = listOfBusinesses['total']
    countZip = 0
    countZipAndOnePlus = 0
    countZipAndTwentyPlus = 0

    #loops through all locations(zip codes) in our json file
    while size < locationSize:

        #loops until we get all businesses
        while offset < totalSize:

            #do code here to check each business and update the csv files
            #we get 50 businesses so check array from 0 to 49
            if totalSize - offset < 50:
                x = totalSize - offset
            else:
                x = 49

            for i in range(0, x):
                jsonBusiness = listOfBusinesses['businesses'][i]

                #if we see required zipcode value do following
                if jsonBusiness['location']['zip_code'] == '60602' or jsonBusiness['location']['zip_code'] == '60612' or jsonBusiness['location']['zip_code'] == 60602 or jsonBusiness['location']['zip_code'] == 60612:

                    #if business mets minimum reviews do the following
                    if jsonBusiness['review_count'] >= 17:

                        #getting website info pass url and biz id
                        website_data = website_parse(jsonBusiness['url'], jsonBusiness['id'])

                        if website_data:
                            #Retrieve from the yelp API
                            Business.businessID = jsonBusiness['id']
                            Business.name = jsonBusiness['name']

                            #Convert location from dict to string
                            a = []
                            value = ''
                            a.append(jsonBusiness['location']['address1'])
                            a.append(jsonBusiness['location']['address2'])
                            a.append(jsonBusiness['location']['address3'])
                            a.append(jsonBusiness['location']['city'])
                            a.append(jsonBusiness['location']['state'])
                            a.append(jsonBusiness['location']['zip_code'])
                            a.append(jsonBusiness['location']['country'])

                            for each in a:
                                if each:
                                    value = value + each + " "

                            Business.location = value.strip()    #concatenate or display as such?
                            Business.reviewCount = str(jsonBusiness['review_count'])
                            Business.rating = str(jsonBusiness['rating'])

                            #Convert categories from list to single string
                            a = jsonBusiness['categories']
                            text = ''
                            for each in a:
                                for key in each:
                                    text = text + key + ':' + each[key] + ' '

                            Business.categories = text.strip() #concatenate or display as such?
                            Business.phoneNumber = str(jsonBusiness['phone'])

                            #Retrieve from website
                            Business.address = website_data.get('Address', '')
                            Business.webSite = website_data.get('URL', '')
                            Business.Hours = website_data.get('Hours', '')
                            Business.GoodforKids = website_data.get('Good for Kids', '')
                            Business.AcceptsCreditCards = website_data.get('Accepts Credit Cards', '')
                            Business.Parking = website_data.get('Parking','')
                            Business.Attire = website_data.get('Attire','')
                            Business.GoodforGroups = website_data.get('Good for Groups','')
                            Business.PriceRange = website_data.get('Price','')
                            Business.TakesReservations = website_data.get('Takes Reservations','')
                            Business.Delivery = website_data.get('Delivery','')
                            Business.Takeout = website_data.get('Take-out','')
                            Business.WaiterService = website_data.get('Waiter Service','')
                            Business.OutdoorSeating = website_data.get('Outdoor Seating','')
                            Business.WiFi = website_data.get('Wi-Fi','')
                            Business.GoodFor = website_data.get('Good For','')
                            Business.Alcohol = website_data.get('Alcohol','')
                            Business.NoiseLevel = website_data.get('Noise Level','')
                            Business.Ambience = website_data.get('Ambience','')
                            Business.HasTV = website_data.get('Has TV','')
                            Business.Caters = website_data.get('Caters','')
                            Business.WheelchairAccessible = website_data.get('Wheelchair Accessible','')

                            data = [Business.businessID,Business.name,Business.location,Business.reviewCount,Business.rating,Business.categories,Business.address,Business.Hours,Business.GoodforKids,Business.AcceptsCreditCards,Business.Parking,Business.Attire,Business.GoodforGroups,Business.PriceRange,Business.TakesReservations,Business.Delivery,Business.Takeout,Business.WaiterService,Business.OutdoorSeating,Business.WiFi,Business.GoodFor,Business.Alcohol,Business.NoiseLevel,Business.Ambience,Business.HasTV,Business.Caters,Business.WheelchairAccessible,Business.webSite,Business.phoneNumber,Business.reviewCount]
                            #print (data)
                            for count,each in enumerate(data):
                                if count != len(data)-1:
                                    restaurant.write(each)
                                    restaurant.write(',')
                                else:
                                    restaurant.write(each)
                            restaurant.write('\n')


                #check if business is within the zipcode we desire and has more then 0 reviews if so continue
                '''
                if in zipcode:
                    #do code to extract business info from yelp api to Business.class
                    #do code to fetch yelp business page
                    #do code to view reviews and parse through array of reviews and add to review csv
                            #if user is not in user.csv:
                                #get user data
                '''

            #increase offset
            offset += 50

            #get next set of businesses
            urlNew = url.format(str(offset), attributes['categories'], attributes['location']['list'][size])
            websiteData = urllib.request.Request(urlNew, headers=headerNew, method='GET')
            websiteData = urllib.request.urlopen(websiteData).read()
            listOfBusinesses = json.loads(websiteData)

        #increase the location increment
        size += 1

        if size < locationSize:
            #used to track index and if it should keep on trying to make calls to api.yelp
            offset = 0

            #get next set of businesses using next location
            urlNew = url.format(str(offset), attributes['categories'], attributes['location']['list'][size])
            websiteData = urllib.request.Request(urlNew, headers=headerNew, method='GET')
            websiteData = urllib.request.urlopen(websiteData).read()
            listOfBusinesses = json.loads(websiteData)

            #used to track index and if it should keep on trying to make calls to api.yelp
            totalSize = listOfBusinesses['total']

    print(countZip)
