import gi
import connectMongo
gi.require_version('Geoclue', '2.0')
from gi.repository import Geoclue
from pymongo import GEOSPHERE


clue = Geoclue.Simple.new_sync('something',Geoclue.AccuracyLevel.NEIGHBORHOOD,None)
location = clue.get_location()
user_geo_location = [location.get_property('longitude'), location.get_property('latitude')]
if (len(user_geo_location) == 2):
    print("User Geo Location successfully obtained")
else:
    print()

db = connectMongo.connectDatabase()
data_collection = db["data"]
station_collection = db["station"]

station_collection.create_index([('geometry',GEOSPHERE)])

get_geo = station_collection.find({
    'geometry':{
        '$near':{
            '$geometry':{'type':'Point', 'coordinates':user_geo_location},
            '$minDistance': 0,
            '$maxDistance': 300
        }
    }
})

for index, item in enumerate(get_geo):
    print('**** Nearest Station {0} ****\nStation name: {1}\nCity: {2}\nStreet: {3}\n\n'.format((index+1),item['station_name'],item['address']['city'],item['address']['street']))

