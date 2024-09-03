from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timezone
from app.meetings.__init__ import meetings_bp

# Replace with your MongoDB connection string
client = MongoClient("mongodb://jungleGYM:jungleGYM@13.125.51.118", 27017)
db = client.gym_app

@meetings_bp.route("/")
def index():
    return render_template("meeting.html")

@meetings_bp.route("/create_gym", methods=["POST"])
def create_gym():

    print("되는거노?22")
    category = request.form.get("category")
    date = request.form.get("date")
    time = request.form.get("time")
    max_people = int(request.form.get("max_people"))
    location = request.form.get("location")
    notice = request.form.get("notice")
    equipment = request.form.get("equipment", "")
    leader_info = request.form.get("leader_info")  # Example: "John Doe, Male, 1990"

    gym_schedule = {
        "category": category,
        "date": date,
        "time": time,
        "max_people": max_people,
        "location": location,
        "notice": notice,
        "equipment": equipment,
        "leader_info": leader_info,
        "participants": [],
        "created_at": datetime.now(timezone.utc),
    }

    db.gyms.insert_one(gym_schedule)

    return jsonify({"result": "success", "msg": "운동 스케줄 생성 성공!"})


@meetings_bp.route("/get_gym_list", methods=["GET"])
def get_gym_list():

    print("되는거노?")
    gym_list = list(db.gyms.find({}, {"_id": False}).sort("created_at", -1))
    return jsonify({"result": "success", "gym_list": gym_list})


@meetings_bp.route("/get_gym_details", methods=["POST"])
def get_gym_details():
    date = request.form.get("date")
    time = request.form.get("time")
    location = request.form.get("location")

    gym_details = db.gyms.find_one(
        {"date": date, "time": time, "location": location}, {"_id": False}
    )

    return jsonify({"result": "success", "gym_details": gym_details})


@meetings_bp.route("/participate_gym", methods=["POST"])
def participate_gym():
    date = request.form.get("date")
    time = request.form.get("time")
    location = request.form.get("location")
    participant_info = request.form.get(
        "participant_info"
    )  # Example: "Jane Doe, Female, 1995"

    db.gyms.update_one(
        {"date": date, "time": time, "location": location},
        {"$addToSet": {"participants": participant_info}},
    )

    return jsonify({"result": "success", "msg": "참가 완료!"})
