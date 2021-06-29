from flask_wtf.recaptcha import validators
from initialize import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, SelectMultipleField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from wtforms import widgets
from wtforms.widgets import TextArea

class Problem(db.Model):
    __table_args__ = {'extend_existing': True}
    func_name = db.Column("func_name", db.String(50), primary_key = True)
    func_call = db.Column(db.String(70), nullable = False)
    author = db.Column(db.String(40), nullable = False)
    desc = db.Column(db.String, nullable = False)
    testInputs = db.Column(db.String, nullable = False)
    testInputAnswers = db.Column(db.String, nullable = False)
    tags = db.Column(db.String, nullable = False)
    function = db.Column(db.String, nullable = False)
    
    def __repr__(self):
        return """
            func_name = {func_name}\n
            function = {function}\n
            inputs = {inputs}\n
            outputs = {outputs}\n
            tags = {tags}\n
        """.format(func_name =self.func_name, function = self.function, inputs = self.testInputs, outputs = self.testInputAnswers, tags = self.tags)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean(), default = False)

    def __repr__(self):
        return self.email + ". is admin?  " + str(self.admin)

#WTFORMS CLASSES

#custom validator that will raise an error if email is not HMC
class HMCEmail(object):
    def __init__(self, message=None):
        if not message:
            message = u'Email must be a HMC email.'
        self.message = message 
    def __call__(self, form, field):
        if "@hmc.edu" not in field.data and "@g.hmc.edu" not in field.data:
            raise ValidationError("Email must be a HMC email.")

class LoginForm(FlaskForm):
    email = StringField('email', validators = [InputRequired(), Email()])
    password = PasswordField('password', validators = [InputRequired()])

class RegisterForm(FlaskForm):
    email = StringField('email', validators = [InputRequired(), Email(check_deliverability = True), HMCEmail()])
    password = PasswordField('password', validators = [InputRequired(), Length(min=8, max = 20)])

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()



class ProblemForm(FlaskForm):
    author = StringField('author')
    desc = HiddenField('desc', validators = [InputRequired(), Length(min = 50, max = 150)] )
    tags = MultiCheckboxField('tags', validators = [InputRequired()])
    code = HiddenField('code', validators=[InputRequired()])
    testInputs = HiddenField('testInputs', validators = [InputRequired()])
    testOutputs = HiddenField('testOutputs', validators = [InputRequired()])
    buggyCode = HiddenField('buggycode')
    
    


    