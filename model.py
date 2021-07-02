from flask_wtf.recaptcha import validators
from initialize import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, SelectMultipleField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from wtforms import widgets
from wtforms.widgets import TextArea


class Problem(db.Model):
    __table_args__ = {'extend_existing': True}
    func_name = db.Column("func_name", db.String(50), primary_key=True)
    func_call = db.Column(db.String(70), nullable=False)
    function = db.Column(db.String, nullable=False)

    author = db.Column(db.String(40))
    desc = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=False)

    testCaseInputs = db.Column(db.String, nullable=False)
    testCaseOutputs = db.Column(db.String, nullable=False)
    testInputs = db.Column(db.String)
    testOutputs = db.Column(db.String)
    buggy_function = db.Column(db.String)

    def __repr__(self):
        return self.func_name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.email + ". is admin?  " + str(self.admin)

# WTFORMS CLASSES

# custom validator that will raise an error if email is not HMC


class HMCEmail(object):
    def __init__(self, message=None):
        if not message:
            message = u'Email must be a HMC email.'
        self.message = message

    def __call__(self, form, field):
        if "@hmc.edu" not in field.data and "@g.hmc.edu" not in field.data:
            raise ValidationError("Email must be a HMC email.")


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired()])


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(
        check_deliverability=True), HMCEmail()])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=20)])


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ProblemForm(FlaskForm):
    author = StringField('author')
    desc = HiddenField('desc')
    tags = MultiCheckboxField('tags')
    code = HiddenField('code')
    testCaseInputs = HiddenField('testCaseInputs')
    testCaseOutputs = HiddenField('testCaseOutputs')
    testInputs = HiddenField('testInputs')
    testOutputs = HiddenField('testOutputs')
    buggyCode = HiddenField('buggyCode')
