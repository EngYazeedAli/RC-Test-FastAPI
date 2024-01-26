from pymongo import MongoClient

client = MongoClient("mongodb+srv://royal_db:royaltest0548@royaldb.nlsajw5.mongodb.net/")

db = client.Royal_Challenge

user_collection = db["Users"]
attendance_collection = db["Attendances"]