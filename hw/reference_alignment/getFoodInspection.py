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
    #get csv from this website
    #https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5/data
    oldReference = csv.reader(open('Food_Inspections.csv', 'r'))

    attributes_File = open('foodInspectionAttributes.json', 'r').read()
    inspectionAttributes = json.loads(attributes_File)

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

            address = data_dict['Address'].lower()
            city = data_dict['City'].lower()
            state = data_dict['State'].lower()
            zipcode = data_dict['Zip'].lower()
            
            #these variables are here just incase restaurant is in a mall and multiple bussinesses are given back
            #add a final if statement within multiple statements below
            #if inspectionAttributes['name'] in nameAKA or inspectionAttributes['name'] in nameDBA:
            nameAKA = data_dict['AKA Name'].lower()
            nameDBA = data_dict['DBA Name'].lower()
            
            #try to find business inspections by address
            if inspectionAttributes['city'] in city:
                # a b d f j l m p r s w
                if inspectionAttributes['state'] in state:
                    if inspectionAttributes['zipcode'] in zipcode:
                        if inspectionAttributes['address'] in address:
                            dictReference[count] = data_dict
                            count += 1

    newReference = open('newFoodInspection.csv', 'w')
    newReference.write(headerStuff(header))

    for x in dictReference.values():
        newReference.write(convertDictToString(x.values()))
        print(x.values())

    newReference.close()
