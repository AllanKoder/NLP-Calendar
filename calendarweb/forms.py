from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, InputRequired, Length

class RegistrationForm(FlaskForm):
        username = StringField('Username', 
                            validators=[InputRequired(),
                                Length(min=4, max=15)])
        email = StringField ('Email',validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        confirmpassword = PasswordField('ConfirmPassword', validators=[DataRequired(), EqualTo('password')])
        submit = SubmitField('Sign Up') 

class LoginForm(FlaskForm):
    email = StringField ('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Sign In') 