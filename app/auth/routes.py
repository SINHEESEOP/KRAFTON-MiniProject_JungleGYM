from flask import redirect, render_template, flash, request, jsonify, make_response
from app.auth.__init__ import auth_bp
from app.auth.services import myinfo_service, register_service, login_service
from app.auth.forms import LoginForm, RegisterForm
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies

from datetime import datetime

@auth_bp.route('/myinfo', methods=['GET'])
@jwt_required(locations=['cookies'])
def myinfo():
  current_user = get_jwt_identity()
  myinfo = myinfo_service(current_user)
  return jsonify(myinfo), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required(locations=['cookies'])
def protected():
  current_user = get_jwt_identity()
  return jsonify(logged_in_as=current_user), 200

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm(request.form)
  if request.method == 'POST':
    if form.validate():
      result = login_service(request.form.get('user_id'), request.form.get('password'))
      if result:
        access_token = create_access_token(identity=request.form.get('user_id'))
        response = make_response({'result': 'success'})
        set_access_cookies(response, access_token)
        return response
  return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
  form = RegisterForm(request.form)
  if request.method == 'POST':
    if form.validate():
      result = register_service(request.form.get('user_id'), request.form.get('password'), request.form.get('password_confirm'), request.form.get('name'), request.form.get('nickname'), request.form.get('gender'), request.form.get('age'), request.form.get('phone_number'), request.form.getlist('interests[]'))
      if result:
        return jsonify({'result': 'success'})
  return render_template('register.html')
