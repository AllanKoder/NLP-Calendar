from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, InputRequired, Length
from calendarweb.models import User

class RegistrationForm(FlaskForm):
        username = StringField('Username', 
                            validators=[InputRequired(),
                                Length(min=4, max=15)])
        email = StringField ('Email',validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
        submit = SubmitField('Sign Up') 
        def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is Taken. Please choose another one.")
        def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is already used. Please choose another one.")


class LoginForm(FlaskForm):
    email = StringField ('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Sign In') 