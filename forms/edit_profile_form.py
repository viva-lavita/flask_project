from flask_wtf import FlaskForm
from wtforms import (
    StringField, DateTimeField, TelField,
)
from wtforms.validators import Length, Optional


class EditProfileForm(FlaskForm):
    name = StringField("Имя", validators=[Length(max=25)])
    surname = StringField("Фамилия", validators=[Length(max=25)])
    birth_date = DateTimeField("Дата рождения (гггг.мм.дд)", format="%Y.%m.%d", default='', validators=[Optional()])
    phone = TelField("Телефон", validators=[Length(max=25)])
    city = StringField("Город", validators=[Length(max=25)])
    profession = StringField("Профессия", validators=[Length(max=40)])
    site = StringField("Сайт", validators=[Length(max=100)])
    github = StringField("GitHub", validators=[Length(max=100)])
