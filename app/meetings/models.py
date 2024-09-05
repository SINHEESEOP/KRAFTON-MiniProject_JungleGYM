from app import mongo
from datetime import datetime, timezone, timedelta, date
from pytz import timezone
from bson.objectid import ObjectId
import logging


class Meeting:
    def __init__(
            self,
            title,
            category,
            date,
            time,
            max_people,
            location,
            latitude,
            longitude,
            leader_id,
            _id="",
            notice="",
            equipment="",
            leader_info="",
    ):

        self._id = _id
        self.title = title
        self.category = category
        self.date = date
        self.time = time
        self.max_people = max_people
        self.location = location
        self.notice = notice
        self.equipment = equipment
        self.leader_info = leader_info
        self.latitude = latitude
        self.longitude = longitude
        self.leader_id = leader_id  # ID of the user who created the meeting
        self.participant_ids = [leader_id]  # List of user IDs who have signed up
        self.created_at = datetime.now(timezone('Asia/Seoul'))

    def save(self):
        print(self.date, '%Y-%m-%d')
        meeting_data = {
            "title": self.title,
            "category": self.category,
            "date": datetime.strptime(self.date, '%Y-%m-%d'),
            "time": self.time,
            "max_people": self.max_people,
            "location": self.location,
            "notice": self.notice,
            "equipment": self.equipment,
            "leader_info": self.leader_info,
            "leader_id": self.leader_id,
            "participant_ids": self.participant_ids,
            "created_at": self.created_at,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
        mongo.db.meetings.insert_one(meeting_data)

    @staticmethod
    def get_all_meetings():
        return list(mongo.db.meetings.find({'date': { '$gte': datetime(date.today().year, date.today().month, date.today().day - 1) }}))

    @staticmethod
    def get_meeting_by_id(meeting_id):
        return mongo.db.meetings.find_one({"_id": ObjectId(meeting_id)})

    @staticmethod
    def update(data):
        update_data = {
            "title": data.get("title", {}),
            "category": data.get("category", {}),
            "date": data.get("date", {}),
            "time": data.get("time", {}),
            "max_people": data.get("max_people", {}),
            "location": data.get("location", {}),
            "notice": data.get("notice", {}),
            "equipment": data.get("equipment", {}),
            "leader_info": data.get("leader_info", {}),
            "latitude": data.get("latitude", {}),
            "longitude": data.get("longitude", {}),
        }
        mongo.db.meetings.update_one({"_id": ObjectId(data.get("_id", {}))}, {"$set": update_data})

    @staticmethod
    def delete(meeting_id):
        return mongo.db.meetings.delete_one({"_id": ObjectId(meeting_id)})

    @staticmethod
    def find_one(user_id):
        user = mongo.db['users'].find_one(
            {'user_id': user_id},  # 검색 조건
            {'name': 1, 'birth': 1, 'gender': 1, 'total_ex_time': 1, '_id': 0}  # 가져올 필드만 명시, _id 제외
        )
        return user

    def __repr__(self):
        return f"<Meeting {self.category}>"
