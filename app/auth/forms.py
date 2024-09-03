from wtforms import Form, StringField, PasswordField, SelectField, DateField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo
from datetime import datetime

gender_choices=[('male', '남자'), ('female', '여자')]
interests_choices=[('running', '러닝'), ('health', '헬스'), ('climbing', '클라이밍')]

class LoginForm(Form):
  user_id = StringField('아이디', validators=[DataRequired(), Length(min=4, max=20)])
  password = PasswordField('비밀번호', validators=[DataRequired(), Length(min=8, max=20)])

class RegisterForm(Form):
  user_id = StringField('아이디', validators=[DataRequired(), Length(min=4, max=20)])
  password = PasswordField('비밀번호', validators=[DataRequired(), Length(min=8, max=20)])
  password_confirm = PasswordField('비밀번호 확인', [DataRequired(), Length(min=8, max=20), EqualTo('password')])
  name = StringField('이름', validators=[DataRequired(), Length(min=1, max=30)])
  nickname = StringField('별명 (선택)', validators=[])
  gender = SelectField('성별', choices=gender_choices)
  age = StringField('생일', validators=[])
  phone_number = StringField('전화번호', validators=[DataRequired()])
  interests = SelectMultipleField('관심사', choices=interests_choices)