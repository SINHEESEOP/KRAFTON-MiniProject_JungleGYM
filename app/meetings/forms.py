from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class MeetingForm(FlaskForm):
    category = StringField("Category", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()])
    time = StringField("Time", validators=[DataRequired()])
    max_people = IntegerField(
        "Max People", validators=[DataRequired(), NumberRange(min=1)]
    )
    location = StringField("Location", validators=[DataRequired()])
    notice = TextAreaField("Notice")
    equipment = StringField("Equipment")
    leader_info = StringField("Leader Info", validators=[DataRequired()])
    submit = SubmitField("Save")
