from bson.objectid import ObjectId
import getBicycleStation
import connectMongo
import datetime

def firstData():
    db = connectMongo.connectDatabase()

    bicycleData = getBicycleStation.getLilleData()
    data_collection = db["data"]
    station_collection = db["station"]

    available_lille = "EN SERVICE"
    connected_lille = "CONNECTED"
    type_lille = "AVEC TPE"

    print("Populate Database with first Data")
    for i in range(len(bicycleData)):
        object_id = ObjectId()
        data_item = {
            "bikes_available" : bicycleData[i]['fields']['nbvelosdispo'],
            "stands_available" : bicycleData[i]['fields']['nbplacesdispo'],
            "is_operating": bicycleData[i]['fields']['etat'] == available_lille,
            "is_connected": bicycleData[i]['fields']['etatconnexion'] == connected_lille,
            "date": datetime.datetime.strptime(bicycleData[i]['fields']['datemiseajour'], "%Y-%m-%dT%H:%M:%S+00:00"),
            "station_id": object_id
        }
        station_item = {
            "_id": object_id,
            "station_name" : bicycleData[i]['fields']['nom'],
            "tpe": bicycleData[i]['fields']['type'] == type_lille,
            "address" : {
                "city": bicycleData[i]['fields']['commune'],
                "street": bicycleData[i]['fields']['adresse'],
            },
            "total_stands": int(bicycleData[i]['fields']['nbplacesdispo']) + int(bicycleData[i]['fields']['nbvelosdispo']),
            "geometry": bicycleData[i]['geometry']
        }
        data_collection.insert_one(data_item)
        station_collection.insert_one(station_item)

        print("Inserted Document", i+1)

    print("Insertion Successful")
