from pymongo import MongoClient

def connectDatabase():
    db_client = MongoClient("mongodb+srv://dbUser:dbUserPassword@cluster0.tyqod.mongodb.net/dbUser?retryWrites=true&w=majority")
    return db_client.get_database('velo_db')

