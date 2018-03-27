import csv

#this is for sorting the dict data
def sortByChar(tempDict):
    x = tempDict['name'].lower()
    x = x[0]

    if x == 'a':
        return 0
    elif x == 'b':
        return 1
    elif x == 'c':
        return 2
    elif x == 'd':
        return 3
    elif x == 'e':
        return 4
    elif x == 'f':
        return 5
    elif x == 'g':
        return 6
    elif x == 'h':
        return 7
    elif x == 'i':
        return 8
    elif x == 'j':
        return 9
    elif x == 'k':
        return 10
    elif x == 'l':
        return 11
    elif x == 'm':
        return 12
    elif x == 'n':
        return 13
    elif x == 'o':
        return 14
    elif x == 'p':
        return 15
    elif x == 'q':
        return 16
    elif x == 'r':
        return 17
    elif x == 's':
        return 18
    elif x == 't':
        return 19
    elif x == 'u':
        return 20
    elif x == 'v':
        return 21
    elif x == 'w':
        return 22
    elif x == 'x':
        return 23
    elif x == 'y':
        return 24
    elif x == 'z':
        return 25
    else:
        return 26

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
    oldReference = csv.reader(open('restaurants_60601-60606.csv', 'r'))

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

            categories = data_dict['categories'].lower()
            firstLetter = data_dict['name'].lower()
            firstLetter = firstLetter[0]
            #if categories contains restaurant proceed to next if
            if 'restaurant' in categories:
                # a b d f j l m p r s w
                #if first letter of name of restaurant starts with t or r proceed
                if firstLetter == 't' or firstLetter == 'r':
                    #add data to dictReference and increment counter
                    dictReference[count] = data_dict
                    count += 1
    
    #sort the data by first char
    tempe = sorted(dictReference.values(), key=sortByChar)
    
    #create file to store data in
    newReference = open('newReference.csv', 'w')
    
    #add header
    newReference.write(headerStuff(header))
    
    #add data
    for x in tempe:
        newReference.write(convertDictToString(x.values()))
        #print(x.values())
        
    #close file
    newReference.close()
