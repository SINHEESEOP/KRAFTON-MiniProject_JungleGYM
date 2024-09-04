from app import mongo
from datetime import datetime
from bson.objectid import ObjectId
import logging


class Meeting:
    def __init__(
        self,
        category,
        date,
        time,
        max_people,
        location,
        notice="",
        equipment="",
        leader_info="",
        leader_id=None,
    ):
        self.category = category
        self.date = date
        self.time = time
        self.max_people = max_people
        self.location = location
        self.notice = notice
        self.equipment = equipment
        self.leader_info = leader_info
        self.leader_id = leader_id  # ID of the user who created the meeting
        self.participant_ids = []  # List of user IDs who have signed up
        self.created_at = datetime.utcnow()

    def save(self):
        meeting_data = {
            "category": self.category,
            "date": self.date,
            "time": self.time,
            "max_people": self.max_people,
            "location": self.location,
            "notice": self.notice,
            "equipment": self.equipment,
            "leader_info": self.leader_info,
            "leader_id": self.leader_id,
            "participant_ids": self.participant_ids,
            "created_at": self.created_at,
        }
        mongo.db.meetings.insert_one(meeting_data)

    @staticmethod
    def get_all_meetings():
        return list(mongo.db.meetings.find())

    @staticmethod
    def get_meeting_by_id(meeting_id):
        return mongo.db.meetings.find_one({"_id": ObjectId(meeting_id)})

    def update(self, data):
        update_data = {
            "category": data.get("category", self.category),
            "date": data.get("date", self.date),
            "time": data.get("time", self.time),
            "max_people": data.get("max_people", self.max_people),
            "location": data.get("location", self.location),
            "notice": data.get("notice", self.notice),
            "equipment": data.get("equipment", self.equipment),
            "leader_info": data.get("leader_info", self.leader_info),
        }
        mongo.db.meetings.update_one({"_id": self._id}, {"$set": update_data})

    @staticmethod
    def delete(meeting_id):
        return mongo.db.meetings.delete_one({"_id": ObjectId(meeting_id)})

    def __repr__(self):
        return f"<Meeting {self.category}>"
