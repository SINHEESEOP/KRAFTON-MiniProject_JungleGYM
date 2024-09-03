from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.mydatabase                      # 'dbjungle'라는 이름의 db를 만듭니다.


def insert_all():
  doc = {
    'level' : 2,
    'name' : '김진모',
    'totalExTime' : 600
  }

  db.gym.insert_one(doc)


if __name__ == '__main__':
    # db.gym.drop()
    insert_all()