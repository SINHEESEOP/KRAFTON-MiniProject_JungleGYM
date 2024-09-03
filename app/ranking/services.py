from app.ranking.models import User

# """모든 사용자들의 랭킹 리스트를 가져옵니다."""
def get_all_rankings():

    print(get_level("66d68db009fbe46933d24416"))

    userUpDate = []

    user = User.find_all()
    for user in user:
        totalExTime = user.get('totalExTime')
        hours, minutes = minutes_to_time(totalExTime)

        if minutes != 0:
            user['totalExTime'] = f"{hours}시간 {minutes}분"
        else:
            user['totalExTime'] = f"{hours}시간"

        userUpDate.append(user)

    sorted_data = sorted(userUpDate, key=lambda x: x['level'], reverse=True)
    return sorted_data


def get_level(userId):
    user = User.find_one(userId)
    if user:
        totalExTime = user.get('totalExTime', 0)

        hours, minutes = minutes_to_time(totalExTime)

        # 레벨 계산: 10시간마다 1레벨 증가
        level = (hours // 10) + 1

        return level
    return None


def minutes_to_time(totalExTime):
    hours = totalExTime // 60
    minutes = totalExTime % 60
    return (hours, minutes)
