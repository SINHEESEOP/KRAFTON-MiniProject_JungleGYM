from flask import redirect, render_template, flash, request, jsonify
from app.auth.__init__ import auth_bp, services
from app.auth.forms import LoginForm, RegisterForm

from datetime import datetime

@auth_bp.route('/', methods=['GET'])
def route_auth():
  return 'TEST'

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm(request.form)
  if request.method == 'POST':
    if form.validate():
      result = services.login(form.user_id.data, form.password.data)
      if result:
        print('로그인성공')
        return redirect('/')
  return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
  form = RegisterForm(request.form)
  if request.method == 'POST':
    if form.validate():
      result = services.register(form.user_id.data, form.password.data, form.password_confirm.data, form.name.data, form.nickname.data, form.gender.data, form.age.data, form.phone_number.data, form.interests.data)
      if result:
        return jsonify({'result': 'success'})
  return render_template('register.html')
