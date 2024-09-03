from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB 설정
client = MongoClient('localhost', 27017)
db = client.mydatabase

class User:
    def __init__(self, name, level, totalExTime):
        self.name = name
        self.level = level
        self.totalExTime = totalExTime


    @classmethod
    def find_all(cls):
        userList = db.gym.find()
        return list(userList)

    @classmethod
    def find_one(cls, userId):
        user = db['gym'].find_one({'_id': ObjectId(userId)})
        return user

