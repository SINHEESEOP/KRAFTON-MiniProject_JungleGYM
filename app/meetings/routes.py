from flask import render_template, redirect, request, jsonify, url_for
from app.meetings.__init__ import meetings_bp
from app.meetings.models import Meeting

# from app.auth.models import User
from bson.objectid import ObjectId


@meetings_bp.route("/", methods=["GET", "POST"])
def list_meetings():
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

        if meeting_id:
            # 수정 로직
            meeting = Meeting.get_meeting_by_id(meeting_id)
            meeting_data = {
                "category": category,
                "date": date,
                "time": time,
                "max_people": max_people,
                "location": location,
                "notice": notice,
                "equipment": equipment,
                "leader_info": leader_info,
            }
            meeting.update(meeting_data)
        else:
            # 생성 로직
            new_meeting = Meeting(
                category=category,
                date=date,
                time=time,
                max_people=max_people,
                location=location,
                notice=notice,
                equipment=equipment,
                leader_info=leader_info,
            )
            new_meeting.save()

        return redirect(url_for("meetings.list_meetings"))

    meetings = Meeting.get_all_meetings()
    return render_template("listAndDetail.html", meetings=meetings)


@meetings_bp.route("/details/<meeting_id>", methods=["GET"])
def get_meeting_details(meeting_id):
    try:
        meeting = Meeting.get_meeting_by_id(meeting_id)
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404

        # Prepare the data to be sent as JSON
        leader_info = meeting.get("leader_info", {})
        participants_info = meeting.get("participants", [])

        return jsonify({"leader": leader_info, "participants": participants_info})
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
