from app.ranking.models import User

# """모든 사용자들의 랭킹 리스트를 가져옵니다."""
def get_all_rankings():

    user_up_date = []

    user = User.find_all()
    for user in user:
        total_ex_time = user.get('total_ex_time')
        hours, minutes = minutes_to_time(total_ex_time)

        if minutes != 0:
            user['total_ex_time'] = f"{hours}시간 {minutes}분"
        else:
            user['total_ex_time'] = f"{hours}시간"

        user['level'] = get_level(user['user_id'])

        user_up_date.append(user)

    print(user_up_date)

    return user_up_date


def get_level(user_id):
    user = User.find_one(user_id)
    if user:
        total_ex_time = user.get('total_ex_time', 0)

        hours, minutes = minutes_to_time(total_ex_time)

        # 레벨 계산: 10시간마다 1레벨 증가
        level = (hours // 10) + 1

        return level
    return None


def minutes_to_time(total_ex_time):
    hours = total_ex_time // 60
    minutes = total_ex_time % 60
    return hours, minutes


