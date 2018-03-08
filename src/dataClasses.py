'''
This contains classes that hold data along with some utility functions to return everything to a string value
'''


#class that holds user info
class User:
    authorID = ''       #can get from Review Class
    name = ''
    location = ''
    reviewCount = None
    friendCount = None
    photoCount = None

    #constructor
    def __init__(self):
        self.reviewCount = 0
        self.friendCount = 0
        self.photoCount = 0

    #utility functions
    def turnToString(self, value):
        if value is None:
            return ''
        return str(value)

    def toString(self):
        return self.authorID + ', ' + self.name + ', ' + self.location + ', ' + self.turnToString(self.reviewCount) + ', ' + self.turnToString(self.friendCount) + ', ' + self.turnToString(self.photoCount) + '\n'


#class that holds review info
class Review:
    businessID = ''     #can get from Business class
    reviewID = ''
    userID = ''
    date = ''
    reviewContent = ''
    rating = None
    usefulCount = None
    coolCount = None
    funnyCount = None

    #constructor
    def __init__(self, busID, revID, userID, date, content, rating, usefulCount, coolCount, funnyCount):
        self.businessID = busID
        self.reviewID = revID
        self.userID = userID
        self.date = date
        self.reviewContent = content
        self.rating = rating
        self.usefulCount = usefulCount
        self.coolCount = coolCount
        self.funnyCount = funnyCount

    #utility functions
    def turnToString(self, value):
        if value is None:
            return ''
        return str(value)

    def toString(self):
        return self.businessID + ', ' + self.reviewID + ', ' + self.userID + ', ' + self.date + ', ' + self.reviewContent + ', ' + self.turnToString(self.rating) + ', ' + self.turnToString(self.usefulCount) + ', ' + self.turnToString(self.coolCount) + ', ' + self.turnToString(self.funnyCount)

#class that holds business info
class Business:

    businessID = ''      #can get in yelp api
    name = ''            #can get in yelp api
    yelpWebsite = ''     #can get in yelp api
    reviewCount = None   #can get in yelp api
    categories = []      #can get in yelp api
    rating = None        #can get in yelp api
    location = []        #can get in yelp api
    address = ''         #can get in yelp api
    phoneNumber = ''     #can get in yelp api
    PriceRange = ''
    webSite = ''
    Hours = ''
    Attire = ''
    Ambience = ''
    GoodFor = ''
    Parking = ''
    Alcohol = ''
    NoiseLevel = ''
    WiFi = ''
    GoodforKids = None
    AcceptsCreditCards = None
    GoodforGroups = None
    TakesReservations = None
    Delivery = None
    Takeout = None
    WaiterService = None
    OutdoorSeating = None
    HasTV = None
    Caters = None
    WheelchairAccessible = None

    #constructor
    def __init__(self, resID, name, yWeb, revCount, categories, rating,location, address, phoneNumber):
        self.restaurantID = resID
        self.name = name
        self.yelpWebsite = yWeb
        self.reviewCount = revCount
        self.categories = categories
        self.rating = rating
        self.location = location
        self.address = address
        self.phoneNumber = phoneNumber

    #utility functions
    def getZipcode(self):
        if len(self.location) >= 5:
            return self.location[4]
        else:
            return ''

    def isSameZipcode(self, zipcode):
        myZipcode = self.getZipcode()
        if myZipcode == zipcode:
            return True
        else:
            return False

    def turnToString(self, value):
        if value is None:
            return ''
        return str(value)

    def toString(self):
        return

