from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB 설정
client = MongoClient('localhost', 27017)
db = client.mydatabase

class User:
    def __init__(self, name, level, total_ex_time):
        self.name = name
        self.level = level
        self.totalExTime = total_ex_time


    @classmethod
    def find_all(cls):
        user_list = db.users.find().sort("total_ex_time", -1)
        return list(user_list)

    @classmethod
    def find_one(cls, user_id):
        user = db['users'].find_one({'user_id': user_id})
        return user

    def find_one_object_del(cls, user_id):
        user = db['users'].find_one({'user_id': user_id})

        if user and '_id' in user:
            del user['_id']  # ObjectId 필드를 삭제

        return user

