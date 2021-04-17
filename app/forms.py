from flask_wtf import Form
from wtforms import IntegerField
from wtforms import TextField
from wtforms import FloatField
from wtforms import BooleanField
from wtforms.validators import DataRequired

class createCustomerform(Form):
    name = TextField('name', validators=[DataRequired()])
    email = TextField('email', validators =[DataRequired()])
    password = TextField('password', validators=[DataRequired()])
    phone = TextField('phone', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])


class login(Form):
    email = TextField('email', validators =[DataRequired()])
    password = TextField('password', validators=[DataRequired()])