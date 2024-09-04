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


@meetings_bp.route("/", methods=["GET", "POST"])
@jwt_required(locations=["cookies"])
def list_meetings():

    current_user = get_jwt_identity()

    if request.method == "POST":
        meeting_id = request.form.get("meeting_id")
        category = request.form.get("category")
        date = request.form.get("date")
        time = request.form.get("time")
        max_people = request.form.get("max_people")
        location = request.form.get("location")
        notice = request.form.get("notice")
        equipment = request.form.get("equipment")
        leader_info = request.form.get("leader_info")
        user_id = request.form.get("user_id")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        # if meeting_id:
        #     # 수정 로직
        #     meeting = Meeting.get_meeting_by_id(meeting_id)
        #     meeting_data = {
        #         "category": category,
        #         "date": date,
        #         "time": time,
        #         "max_people": max_people,
        #         "location": location,
        #         "notice": notice,
        #         "equipment": equipment,
        #         "leader_info": user_id,
        #     }
        #     meeting.update(meeting_data)
        # else:
        # 생성 로직
        new_meeting = Meeting(
            category=category,
            date=date,
            time=time,
            max_people=max_people,
            location=location,
            notice=notice,
            equipment=equipment,
            leader_info=user_id,
            latitude=latitude,
            longitude=longitude,
        )
        new_meeting.save()

        return jsonify({"result": "success"})

    meetings = Meeting.get_all_meetings()
    for i in range(0, len(meetings)):
        meetings[i]["participant_cnt"] = str(len(meetings[i]["participant_ids"]))
    myinfo = myinfo_service(current_user)
    my_total_ex_time = myinfo.get("total_ex_time")

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

    return render_template(
        "listAndDetail.html",
        meetings=meetings,
        current_user=current_user,
        level=int(my_total_ex_time / 100),
        progress=int(my_total_ex_time % 100),
        my_total_ex_time=my_total_ex_time,
    )


@meetings_bp.route("/details/<meeting_id>", methods=["GET"])
def get_meeting_details(meeting_id):

    print(meeting_id + "이거맞냐")
    try:
        meeting = Meeting.get_meeting_by_id(meeting_id)
        print(meeting)
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404

        # Prepare the data to be sent as JSON
        leader_info1 = meeting.get("leader_info", {})
        leader_info2 = User.find_one(leader_info1)
        leader_info = clean_leader_info(leader_info2)
        print(leader_info)

        participants_info = meeting.get("participants", [])
        print(participants_info)

        return jsonify({"leader": leader_info, "participants": participants_info})
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
