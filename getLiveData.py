import getBicycleStation
import connectMongo
import populateDatabase
import datetime

db = connectMongo.connectDatabase()
collection_names = db.list_collection_names()

if (len(collection_names) == 0):
    populateDatabase.firstData()
else:
    bicycleData = getBicycleStation.getLilleData()
    data_collection = db["data"]
    station_collection = db["station"]

    available_lille = "EN SERVICE"
    connected_lille = "CONNECTED"

    print("Updating with Live Data")
    for i in range(len(bicycleData)):
        assoc_station = station_collection.find_one({'station_name':bicycleData[i]['fields']['nom'], 'address.street':bicycleData[i]['fields']['adresse']})
        data_item = {
            "bikes_available" : bicycleData[i]['fields']['nbvelosdispo'],
            "stands_available" : bicycleData[i]['fields']['nbplacesdispo'],
            "is_operating": bicycleData[i]['fields']['etat'] == available_lille,
            "is_connected": bicycleData[i]['fields']['etatconnexion'] == connected_lille,
            "date": datetime.datetime.strptime(bicycleData[i]['fields']['datemiseajour'], "%Y-%m-%dT%H:%M:%S+00:00"),
            "station_id": assoc_station['_id']
        }

        data_collection.insert_one(data_item)

        print("Inserted Live update document", i+1)

    print("Live Data Document Insertion Successful")
