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
    #download file from chicago data
    oldReference = csv.reader(open('Crimes_-_2001_to_present.csv', 'r'))
    
    #need to manually update json file for your parameters
    attributes_File = open('crimeAttributes.json', 'r').read()
    crimeAttributes = json.loads(attributes_File)

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

            district = data_dict['District'].lower()
            beat = data_dict['Beat'].lower()
            block = data_dict['Block'].lower()
            
            #parse by district, beat, and block
            if crimeAttributes['district'] in district:
                if crimeAttributes['beat'] in beat:
                    if crimeAttributes['block'] in block:
                        dictReference[count] = data_dict
                        count += 1
                        
    #add data to a new csv file
    newReference = open('newCrime.csv', 'w')
    newReference.write(headerStuff(header))

    for x in dictReference.values():
        newReference.write(convertDictToString(x.values()))
        print(x.values())

    newReference.close()
