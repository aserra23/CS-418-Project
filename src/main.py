from bs4 import BeautifulSoup
import urllib
import requests
import json

from dataClasses import User
from dataClasses import Business
from dataClasses import Review

if __name__ == '__main__':

    #this opens or creates author.csv , review.csv, restaurant.csv
    authors = open('user.csv', 'w')
    reviews = open('review.csv', 'w')
    restaurant = open('restaurant.csv', 'w')

    #used to get inputs from attributes.json
    attributes_File = open('attributes.json', 'r').read()
    attributes = json.loads(attributes_File)

    #used to track index and if it should keep on trying to make calls to api.yelp
    offset = 0
    stillGettingFiles = True
    totalSize = 0

    #empty api format
    url = 'https://api.yelp.com/v3/businesses/search?offset={}&limit=50&categories={}&location={}'
    header = '"Authorization": "Bearer {}"'

    #filled api information to make a call
    urlNew = url.format(str(offset), attributes['categories'], attributes['location'])
    headerNew = '{' + header.format(attributes['api_key']) + '}'
    headerNew = json.loads(headerNew)

    websiteData = urllib.request.Request(urlNew, headers=headerNew, method='GET')
    websiteData = urllib.request.urlopen(websiteData).read().decode('utf8')
    listOfBusinesses = json.loads(websiteData)

    totalSize = listOfBusinesses['total']

    #loops until we get all businesses
    while offset < totalSize:

        #do code here to check each business and update the csv files
        #we get 50 businesses so check array from 0 to 49
        for i in range(0,49):
            jsonBusiness = listOfBusinesses['businesses'][i]
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
        urlNew = url.format(str(offset), attributes['categories'], attributes['location'])
        websiteData = urllib.request.Request(urlNew, headers=headerNew, method='GET')
        websiteData = urllib.request.urlopen(websiteData).read()
        listOfBusinesses = json.loads(websiteData)
