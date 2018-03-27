import csv
import json

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
    #go to website to get following file
    #https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr/data
    oldReference = csv.reader(open('Business_Licenses.csv', 'r'))

    attributes_File = open('businessLicenseAttributes.json', 'r').read()
    businessAttributes = json.loads(attributes_File)

    dictReference = {}

    header = {}
    data = {}
    count = 0

    for x in oldReference:
        if header == {}:
            header = x
        else:
            data = x
            data_dict = dict(zip(header, data))

            address = data_dict['ADDRESS'].lower()
            city = data_dict['CITY'].lower()
            state = data_dict['STATE'].lower()
            zipcode = data_dict['ZIP CODE'].lower()
            
            #if multiple results use following values to narrow down results to business name
            #add another nested if statement 
            nameLegal = data_dict['LEGAL NAME'].lower()
            nameBusiness = data_dict['DOING BUSINESS AS NAME'].lower()

            if businessAttributes['city'] in city:
                # a b d f j l m p r s w
                if businessAttributes['state'] in state:
                    if businessAttributes['zipcode'] in zipcode:
                        if businessAttributes['address'] in address:
                            #if businessAttributes['name'] in nameLegal or businessAttributes['name'] in nameBusiness:
                            dictReference[count] = data_dict
                            count += 1

    newReference = open('newBusiness.csv', 'w')
    newReference.write(headerStuff(header))

    for x in dictReference.values():
        newReference.write(convertDictToString(x.values()))
        print(x.values())

    newReference.close()
