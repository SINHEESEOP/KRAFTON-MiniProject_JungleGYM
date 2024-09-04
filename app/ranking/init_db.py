from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.mydatabase  # 'dbjungle'라는 이름의 db를 만듭니다.


def insert_all():
    participant_ids = ['qwer1234', '1234qwer']

    doc = {
        'category': "Running",  # 카테고리: 예시로 'Running'
        'date': "2024-09-10",  # 날짜: YYYY-MM-DD 형식으로 지정
        'time': "14:00",  # 시간: 예시로 오후 2시
        'max_people': 10,  # 최대 인원: 예시로 10명
        'location': "Seoul, South Korea",  # 위치: 예시로 '서울, 대한민국'
        'notice': "Bring your running shoes.",  # 공지사항: '운동화 가져오기'
        'equipment': "Water Bottle",  # 준비물: 예시로 '물병'
        'leader_info': "qwer1234",  # 리더 정보: 사용자 ID (예: 'user12345')
        'latitude' : 127.04165290893805,
        'longitude' : 37.5032863658958,
        'participant_ids' : participant_ids,
        'created_at' : "2024-09-04T18:25:08.468+0000"
    }


    db.meetings.insert_one(doc)

if __name__ == '__main__':
    # db.gym.drop()
    insert_all()
