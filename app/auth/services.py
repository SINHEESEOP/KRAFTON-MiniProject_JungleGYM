from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo

def myinfo_service(user_id):
  user = mongo.db.users.find_one({"user_id": user_id}, {'_id': False, 'password': False})
  print(user)
  if user:
    return user
  return None

def login_service(user_id, password):
  user = mongo.db.users.find_one({"user_id": user_id})
  if user and check_password_hash(user['password'], password):
  # if user and user['password'] == password:
    return user
  return None

def register_service(user_id, password, name, nickname, gender, age, phone_number, interests):
  user = mongo.db.users.find_one({"user_id": user_id})
  if user:
    return None
  # 비밀번호 해싱 및 사용자 저장
  # hashed_password = generate_password_hash(password)
  ## in local MAC
  hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
  new_user = mongo.db.users.insert_one({
    "user_id": user_id, "password": hashed_password, "name": name, "nickname": nickname, "gender": gender, "birth": age, "phone_number": phone_number, "interests": interests, "total_ex_time": 50
  })
  return new_user
  