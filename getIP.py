import connectMongo
from pymongo import GEOSPHERE


"""
update a station
deactivate all station in an area
give all stations with a ratio bike_available/total_stand under 20% between 18h and 19h00 (monday to friday)
"""
db = connectMongo.connectDatabase()
data_collection = db["data"]
station_collection = db["station"]

station_collection.create_index([('geometry',GEOSPHERE)])

def findStation(stationName):
    search_result = station_collection.find({'station_name':{'$regex':stationName.upper()}})
    
    for index, result in enumerate(search_result):
        print("Search Result {0}\nID: {1}\nStation name: {2}\nTpe: {3}\nCity: {4}\nStreet: {5}\nNumber of stands: {6}\n".
        format(index+1,result['_id'],result['station_name'],result['tpe'],result['address']['city'],result['address']['street'],result['total_stands']))

def deactivateStations(stationName):
    find_station = station_collection.find_one({'station_name':stationName.upper()})
   
    print(find_station['station_name'])


    station_geo_point = find_station['geometry']['coordinates']
    
    surrounding_stations = station_collection.find({
        'geometry':{
            '$geoWithin':{
                '$center':[station_geo_point,0.008],
            }
        }
    })
    
    print(surrounding_stations.count())
    """
    print("Surrounding Stations", len(surrounding_stations))
    for index, station in enumerate(surrounding_stations):
        station_collection.update_one(
            {'station_name':station['station_name']},
            {'$set':{'tpe':False}}
        )
        print("Station number {0} with the details below has been SUCCESSFULLY DEACTIVATED\nStation name: {1}\nCity: {2}\nStreet: {3}\nNumber of stands: {4}\n".
        format(index+1,station['station_name'],station['address']['city'],station['address']['street'],station['total_stands']))
    """

def deleteStation(stationName):
    search_result = station_collection.find_one({'station_name':stationName.upper()})
    station_id = search_result['_id']
    station_collection.delete_one({'_id':station_id})
    data_collection.delete_many({'station_id':station_id})
    print("Station",search_result['station_name'],"with related data deleted successfully")


deactivateStations("DE gaulle")