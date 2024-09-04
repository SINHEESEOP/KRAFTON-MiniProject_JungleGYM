from .models import Meeting


def create_meeting(
    category, date, time, max_people, location, notice, equipment, leader_info
):
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
    return new_meeting


def get_meeting_list():
    return Meeting.get_all_meetings()


def get_meeting_details(meeting_id):
    return Meeting.get_meeting_by_id(meeting_id)


def update_meeting(meeting_id, data):
    meeting = Meeting.get_meeting_by_id(meeting_id)
    if meeting:
        meeting.update(data)
        return meeting
    return None


def delete_meeting(meeting_id):
    return Meeting.delete(meeting_id)
