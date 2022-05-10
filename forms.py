"""Author: Nalongsone Danddank, Final Project, begin on Feb 2 2022, end on April 27, 2022, ICS499 METRO STATE """
from models import *


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = SelectField("Role", choices=[("member", "member"), ("admin", "admin")])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Add User")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


# class UpdateUserForm(FlaskForm):

#     email = StringField("Email", validators=[DataRequired(), Email()])
#     role = SelectField("Role", choices=[("member", "member"), ("admin", "admin")])
#     password = PasswordField("Password", validators=[DataRequired()])
#     confirm_password = PasswordField(
#         "Confirm Password", validators=[DataRequired(), EqualTo("password")]
#     )
#     submit = SubmitField("Update")

#     def validate_email(self, email):
#         if email.data != current_user.email:
#             user = User.query.filter_by(email=email.data).first()
#             if user:
#                 raise ValidationError(
#                     "That email is taken. Please choose a different one."
#                 )
