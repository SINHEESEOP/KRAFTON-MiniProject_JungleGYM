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


@meetings_bp.route("/", methods=["GET", "POST"])
@jwt_required(locations=['cookies'])
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
        user_id = request.form.get('user_id')
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
            leader_info=current_user,
            latitude=latitude,
            longitude=longitude
        )
        new_meeting.save()

        return jsonify({'result': 'success'})

    meetings = Meeting.get_all_meetings()
    print(meetings)
    for i in range(0, len(meetings)):
        meetings[i]['participant_cnt'] = str(len(meetings[i]['participant_ids']))
    myinfo = myinfo_service(current_user)
    my_total_ex_time = myinfo.get('total_ex_time')
    return render_template("listAndDetail.html", meetings=meetings, current_user=current_user,
                           level=int(my_total_ex_time / 100), progress=int(my_total_ex_time % 100),
                           my_total_ex_time=my_total_ex_time)


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

        latitude = meeting.get("latitude")
        longitude = meeting.get("longitude")
        print(latitude, longitude)

        participants_info = meeting.get("participant_ids", [])
        # print(participants_info2)
        #
        # participants_info = []
        # for info in participants_info2:
        #     participants_info.append(User.find_one_object_del(info))
        #
        # print(participants_info)



        return jsonify({"leader": leader_info, "participants": participants_info,
                        "latitude": latitude, "longitude": longitude})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@meetings_bp.route("/edit/<meeting_id>", methods=["POST"])
def edit_meeting_route(meeting_id):
    meeting = Meeting.get_meeting_by_id(meeting_id)
    return jsonify(meeting)


@meetings_bp.route("/delete/<meeting_id>", methods=["POST"])
def delete_meeting_route(meeting_id):
    Meeting.delete(meeting_id)
    return jsonify({"result": "success"})


@meetings_bp.route("/start/<meeting_id>", methods=["POST"])
@jwt_required(locations=['cookies'])
def start_meeting_route(meeting_id):
    current_user = get_jwt_identity()
    meeting = Meeting.get_meeting_by_id(meeting_id)
    if not meeting["leader_id"] == current_user:
        return jsonify({"result": "error", "msg": "리더가 아닙니다."})
