from flask import render_template, request, jsonify, make_response
from app.auth.__init__ import auth_bp
from app.auth.services import myinfo_service, register_service, login_service
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
import re

@auth_bp.route('/myinfo', methods=['GET'])
@jwt_required(locations=['cookies'])
def myinfo():
  current_user = get_jwt_identity()
  myinfo = myinfo_service(current_user)
  return render_template('myinfo.html', myinfo=myinfo)

@auth_bp.route('/protected', methods=['GET'])
@jwt_required(locations=['cookies'])
def protected():
  current_user = get_jwt_identity()
  return jsonify(logged_in_as=current_user), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
  response = jsonify({'result': 'success', "msg": "logout successful"})
  unset_jwt_cookies(response)
  return response


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    user_id=request.form.get('user_id')
    password=request.form.get('password')

    if not user_id or not password:
      return jsonify({'result': 'failed', 'msg': '아이디 또는 비밀번호가 비어있습니다.'})
    
    if len(user_id) < 4 or 20 < len(user_id):
      return jsonify({'result': 'failed', 'msg': '아이디는 4자 이상 20자 이하로 작성해주세요.'})
    
    if len(password) < 8 or 20 < len(password):
      return jsonify({'result': 'failed', 'msg': '비밀번호는 8자 이상 20자 이하로 작성해주세요.'})
    
    result = login_service(request.form.get('user_id'), request.form.get('password'))

    if not result:
      return jsonify({'result': 'failed', 'msg': '아이디 또는 비밀번호가 틀렸습니다.'})
    
    access_token = create_access_token(identity=request.form.get('user_id'))
    response = make_response({'result': 'success'})
    set_access_cookies(response, access_token)
    return response
  return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    user_id=request.form.get('user_id')
    password=request.form.get('password')
    password_confirm=request.form.get('password_confirm')
    name=request.form.get('name')
    nickname=request.form.get('nickname')
    gender=request.form.get('gender')
    age=request.form.get('age')
    phone_number=request.form.get('phone_number')
    interests=request.form.getlist('interests[]')
    
    if not user_id or not password or not password_confirm or not name or not gender or not age or not phone_number:
      return jsonify({'result': 'failed', 'msg': '입력칸을 확인해주세요.'})

    if len(user_id) < 4 or 20 < len(user_id):
      return jsonify({'result': 'failed', 'msg': '아이디는 4자 이상 20자 이하로 작성해주세요.'})
    
    if len(password) < 8 or 20 < len(password):
      return jsonify({'result': 'failed', 'msg': '비밀번호는 8자 이상 20자 이하로 작성해주세요.'})
    
    if len(password_confirm) < 8 or 20 < len(password_confirm):
      return jsonify({'result': 'failed', 'msg': '비밀번호 확인은 8자 이상 20자 이하로 작성해주세요.'})
    
    if password != password_confirm:
      return jsonify({'result': 'failed', 'msg': '동일한 비밀번호를 작성했는지 확인해주세요.'})
    
    if len(name) < 1 or 30 < len(name):
      return jsonify({'result': 'failed', 'msg': '이름은 1자 이상 30자 이하로 작성해주세요.'})
  
    if not age.isnumeric() or int(age) < 0 or 200 < int(age):
      return jsonify({'result': 'failed', 'msg': '올바른 나이를 입력해주세요. (0~200)'})
    
    regex = re.compile(r'[0-9]{3}-[0-9]{4}-[0-9]{4}')
    if not regex.match(phone_number):
      return jsonify({'result': 'failed', 'msg': '올바른 전화번호를 입력해주세요.'})

    result = register_service(user_id, password, name, nickname, gender, age, phone_number, interests)
    if not result:
      return jsonify({'result': 'failed', 'msg': '회원가입 실패'})
    return jsonify({'result': 'success'})
  return render_template('register.html')
