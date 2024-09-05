from traceback import print_tb

from flask import render_template, redirect, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.meetings.__init__ import meetings_bp
from app.meetings.models import Meeting
from flask_jwt_extended import jwt_required, get_jwt_identity

# from app.auth.models import User
from bson.objectid import ObjectId

from app.ranking.models import User
from app.meetings.services import clean_leader_info
from app.auth.services import myinfo_service
from datetime import datetime

from app import mongo


@meetings_bp.route("/", methods=["GET", "POST"])
@jwt_required(locations=["cookies"])
def list_meetings():
    current_user = get_jwt_identity()

    if request.method == "POST":
        meeting_id = request.form.get("meeting_id")
        title = request.form.get("title")
        category = request.form.get("category")
        date = request.form.get("date")
        time = request.form.get("time")
        max_people = request.form.get("max_people")
        location = request.form.get("location")
        notice = request.form.get("notice")
        equipment = request.form.get("equipment")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        if meeting_id:
            # 수정 로직
            meeting = Meeting.get_meeting_by_id(meeting_id)
            meeting_data = {
                "_id": meeting_id,
                "title": title,
                "category": category,
                "date": date,
                "time": time,
                "max_people": max_people,
                "location": location,
                "notice": notice,
                "equipment": equipment,
                "leader_id": current_user,
                "latitude": latitude,
                "longitude": longitude,
            }
            print('update', meeting_data)
            Meeting.update(meeting_data)
        else:
            # 생성 로직
            new_meeting = Meeting(
                title=title,
                category=category,
                date=date,
                time=time,
                max_people=max_people,
                location=location,
                notice=notice,
                equipment=equipment,
                leader_id=current_user,
                latitude=latitude,
                longitude=longitude,
            )
            new_meeting.save()

        return jsonify({"result": "success"})

    meetings = Meeting.get_all_meetings()


    # 오름차순 정렬을 위한 함수 정의
    def parse_meeting_datetime(meeting):
        combined_datetime = f"{meeting['date']} {meeting['time']}"
        try:
            return datetime.strptime(combined_datetime, "%Y-%m-%d %H:%M")
        except ValueError:
            # 파싱이 실패한 경우 가장 오래된 날짜로 설정 (정렬을 방해하지 않도록)
            return datetime.min

    # 날짜와 시간에 따라 오름차순 정렬
    meetings.sort(key=parse_meeting_datetime)

    owner_meetings=[]
    participant_meetings=[]
    except_meetings=[]
    for i in range(0, len(meetings)):
        meetings[i]["participant_cnt"] = str(len(meetings[i]["participant_ids"]))
        meetings[i]['is_owner'] = meetings[i]['leader_id'] == current_user
        meetings[i]['is_participant'] = any(el == current_user for el in meetings[i]['participant_ids'])
        if meetings[i]['is_owner']:
            owner_meetings.append(meetings[i])
        elif meetings[i]['is_participant']:
            participant_meetings.append(meetings[i])
        else:
            except_meetings.append(meetings[i])
    myinfo = myinfo_service(current_user)
    my_total_ex_time = myinfo.get("total_ex_time")

    return render_template(
        "listAndDetail.html",
        meetings=(owner_meetings+participant_meetings+except_meetings),
        current_user=current_user,
        level=int(my_total_ex_time / 100),
        progress=int(my_total_ex_time % 100),
        my_total_ex_time=my_total_ex_time,
    )

@meetings_bp.route("/info/<meeting_id>", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_meeting_info(meeting_id):
    meeting = Meeting.get_meeting_by_id(meeting_id)
    if meeting:
        return jsonify({"result": "success", "meeting": {
            "title": meeting["title"],
            "category": meeting["category"],
            "date": meeting["date"],
            "time": meeting["time"],
            "max_people": meeting["max_people"],
            "location": meeting["location"],
            "notice": meeting["notice"],
            "equipment": meeting["equipment"],
        }})
    return jsonify({"result": "fail"})


@meetings_bp.route("/details/<meeting_id>", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_meeting_details(meeting_id):
    try:
        meeting = Meeting.get_meeting_by_id(meeting_id)
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404

        title = meeting.get("title", {})
        # Prepare the data to be sent as JSON
        leader_id = meeting.get("leader_id", {})
        leader_info = clean_leader_info(User.find_one(leader_id))

        latitude = meeting.get("latitude")
        longitude = meeting.get("longitude")

        participants_info2 = meeting.get("participant_ids", [])

        participants_info = []
        for info in participants_info2:
            participants_info.append(Meeting.find_one(info))

        return jsonify({"title": title, "leader": leader_info, "participants": participants_info,
                        "latitude": latitude, "longitude": longitude})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@meetings_bp.route("/attend/<meeting_id>", methods=["POST"])
@jwt_required(locations=["cookies"])
def attend_meeting(meeting_id):
    current_user = get_jwt_identity()
    meeting = Meeting.get_meeting_by_id(meeting_id)

    if not meeting:
        return jsonify({"result": "error", "msg": "Meeting not found"}), 404

    if current_user in meeting["participant_ids"]:
        return (
            jsonify({"result": "error", "msg": "Already attending this meeting"}),
            400,
        )

    if int(meeting['max_people']) == len(meeting["participant_ids"]):
        return (
            jsonify({"result": "error", "msg": "빈 자리가 없습니다."}),
            400,
        )

    meeting["participant_ids"].append(current_user)
    mongo.db.meetings.update_one(
        {"_id": ObjectId(meeting_id)},
        {"$set": {"participant_ids": meeting["participant_ids"]}},
    )

    return jsonify({"result": "success"})


@meetings_bp.route("/cancel/<meeting_id>", methods=["POST"])
@jwt_required(locations=["cookies"])
def cancel_attendance(meeting_id):
    current_user = get_jwt_identity()
    meeting = Meeting.get_meeting_by_id(meeting_id)

    if not meeting:
        return jsonify({"result": "error", "msg": "Meeting not found"}), 404

    if current_user not in meeting["participant_ids"]:
        return (
            jsonify({"result": "error", "msg": "You are not attending this meeting"}),
            400,
        )

    meeting["participant_ids"].remove(current_user)
    mongo.db.meetings.update_one(
        {"_id": ObjectId(meeting_id)},
        {"$set": {"participant_ids": meeting["participant_ids"]}},
    )

    return jsonify({"result": "success"})


@meetings_bp.route("/edit/<meeting_id>", methods=["POST"])
def edit_meeting_route(meeting_id):
    meeting = Meeting.get_meeting_by_id(meeting_id)
    return jsonify(meeting)


@meetings_bp.route("/delete/<meeting_id>", methods=["POST"])
def delete_meeting_route(meeting_id):
    Meeting.delete(meeting_id)
    return jsonify({"result": "success"})


@meetings_bp.route("/start/<meeting_id>", methods=["POST"])
@jwt_required(locations=["cookies"])
def start_meeting_route(meeting_id):
    current_user = get_jwt_identity()
    meeting = Meeting.get_meeting_by_id(meeting_id)
    if not meeting["leader_id"] == current_user:
        return jsonify({"result": "error", "msg": "리더가 아닙니다."})
