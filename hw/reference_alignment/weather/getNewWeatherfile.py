import csv
import json
from itertools import chain


def convertDictToString(thisDict):
    myString = ''
    count = 0
    for x in thisDict:
        if count == 0:
            myString = x
            count += 1
        elif',' in x:
            myString = myString + ',' + '"' + x + '"'
        else:
            myString = myString + ',' + x
    return myString + '\n'

def headerStuff(headers):
    myString = ''
    count = 0
    for x in headers:
        if count == 0:
            myString = x
            count += 1
        else:
            myString = myString + ',' + x
    return myString + '\n'

if __name__ == '__main__':
    //this file is on git with similar title but different
    oldWeather = csv.reader(open('Ohare_Chicago_Weather.csv', 'r'))
    oldWeather_help = []

    '''for x in oldWeather:
        oldWeather_help.append(x)'''
    dictReference = {}

    data = {}
    count = 0

    dates = csv.reader(open('dates.csv', 'r'))
    dates_list = []

    for x in dates:
        dates_list.append(x)
    dates_list = list(chain.from_iterable(dates_list))

    header = {}
    for x in oldWeather:
        if header == {}:
            header = x
        else:
            data = x
            data_dict = dict(zip(header, data))

            #comparevalues here
            
            //might need to change depending on if you opened excel and it modified the file
            date = data_dict['DATE'].split(' ')[0]
            month, day, year = date.split('/')
            //turn to 20xx
            year = '20' + year

            for w in dates_list:
                if w != '\n' or w != '':
                    //this might also need to be changed do to excel changing the format
                    w = w.split(' ')[0]
                    mm, dd, yyyy = w.split('/')

                    if int(yyyy) >= 2016:

                        if int(yyyy) == int(year):
                            # a b d f j l m p r s w
                            if int(mm) == int(month):
                            #if businessAttributes['zipcode'] in zipcode:
                                if int(dd) == int(day):
                                    dictReference[count] = data_dict
                                    count += 1



    newReference = open('newWeatherNow.csv', 'w')
    newReference.write(headerStuff(header))

    for x in dictReference.values():
        newReference.write(convertDictToString(x.values()))
        print(x.values())

    newReference.close()

    print(dates_list)

