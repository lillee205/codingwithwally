from flask import render_template, session, request, jsonify, url_for, redirect, flash
from flask_wtf import FlaskForm
import traceback
import json
import flask_sqlalchemy
from model import Problem, User, LoginForm, RegisterForm, ProblemForm
from initialize import db, bcrypt
from sqlalchemy import exc
from flask.blueprints import Blueprint
import random
from accounts import initAdminAcc
from decorators import admin_required

wally = Blueprint('wally', __name__,
                  template_folder="templates", static_folder="static")
SQLALCHEMY_ECHO = True
# stores the current problem we are on
problem = ""
contents = ""
probDict = {}


tagList = ['python', 'java', 'easy', 'medium', 'hard', 'strings', 'booleans', 'arrays', 'recursion', 'ints',
           'higher-order functions']


def initDict():  # adds all problems currently in database to the dictionary probDict
    global probDict
    probs = Problem.query.all()
    for prob in probs:
        if prob.func_name not in probDict:
            addToDict(prob)


def addToDict(problem):  # adds one problem to probDict
    global probDict
    probDict[problem.func_name] = problem
    currP = probDict[problem.func_name]
    
    #we wrap input in a tuple so that we can extract multiple parameter arguments using *tuple

    probDict[problem.func_name].testCaseInputs = [(eval(input)) for input in json.loads(
        currP.testCaseInputs)]
    probDict[problem.func_name].testCaseOutputs = [eval(output) for output in json.loads(
        currP.testCaseOutputs)]

    probDict[problem.func_name].testInputs = json.loads(
        currP.testInputs) if (currP.testInputs != None and currP.testInputs != "") else []
    probDict[problem.func_name].testOutputs = json.loads(
        currP.testOutputs) if (currP.testOutputs != None and currP.testOutputs != "") else []

    probDict[problem.func_name].tags = json.loads(currP.tags)


@wally.route('/', methods=["POST", "GET"])
def index():

    global problem
    global contents
    global probDict
    problem = ""
    contents = ""
    initDict()
    initAdminAcc()
    if "user" not in session:
        return redirect(url_for('wally.login'))
    else:
        return render_template('index.html', problems=probDict, tagList=tagList, admin=session["isAdmin"])


@wally.route("/addProb", methods=["POST", "GET"])
@admin_required
def addProb():

    global problem
    global contents
    problem = ""
    contents = ""

    global probDict
    initDict()

    form = ProblemForm()
    form.tags.choices = [(tag, tag) for tag in tagList]

    if form.validate_on_submit():

        # extract data about function from string code
        function = form.code.data
        func_call = function[function.index('def') + 4: function.index(':')]
        func_name = func_call[:func_call.index("(")]

        param = {
            "function": function,
            "func_call": func_call,
            "func_name": func_name,

            "author": form.author.data,
            "desc": form.desc.data.replace("background-color: rgb(255, 255, 255);",
                                           "background-color: transparent;").replace("color: rgb(0, 0, 0);", "color: white;"),
            "tags": json.dumps(form.tags.data),

            "testCaseInputs": form.testCaseInputs.data,
            "testCaseOutputs": form.testCaseOutputs.data,
            "testInputs": form.testInputs.data,
            "testOutputs": form.testOutputs.data,

            "buggy_function": form.buggyCode.data
        }
        prob = Problem(**param)

        try:
            db.session.add(prob)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return redirect(url_for('wally.addProb'))
        addToDict(prob)
        return redirect(url_for("wally.index"))

    return render_template('addProb.html', form=form)


@wally.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        newUser = User(email=form.email.data, password=hashed_pass)
        db.session.add(newUser)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
        return redirect(url_for('wally.login'))

    return render_template("register.html", form=form)


@wally.route('/login', methods=["POST", "GET"])
def login():
    initAdminAcc()
    form = LoginForm()

    if form.validate_on_submit():
        logUser = User.query.filter_by(email=form.email.data).first()
        if logUser:
            if bcrypt.check_password_hash(logUser.password, form.password.data):
                session["user"] = (logUser).email
                session["isAdmin"] = logUser.admin
                return redirect(url_for('wally.index'))
    return render_template("login.html", form=form)


@wally.route('/logout', methods=["POST", "GET"])
def logout():
    session.pop("user", None)
    session.pop("isAdmin", None)
    return redirect(url_for('wally.login'))


@wally.route('/prob/<problem_pg>', methods=["POST", "GET"])
def change_type(problem_pg):

    global problem
    global contents

    initDict()

    if (problem_pg) in probDict:
        print("yes!")
        print(problem_pg)
        problem = problem_pg
    else:
        redirect(url_for('wally.index'))

    contents = probDict[problem]
    args = {
        "author": contents.author,
        "function_name": contents.func_name,
        "description": contents.desc,
        "testCaseInputs": contents.testCaseInputs,
        "testCaseOutputs": contents.testCaseOutputs,
        "testInputs": contents.testInputs,
        "testOutputs": contents.testOutputs,
        "buggyCode": contents.buggy_function,
        "func_call": contents.func_call,
        "tags": contents.tags
    }

    if request.method == "POST":
        newView = request.form.to_dict()['hiddenSelect']

        if newView == "test inputs":
            return render_template("testInputs.html", **args)
        elif newView == "write code":
            return render_template("writeCode.html", **args)
        elif newView == "test outputs":
            return render_template("testOutputs.html", **args)
        elif newView == "test bugs":
            return render_template("testBugs.html", **args)
        elif newView == "rand":
            if len(probDict) > 1:
                choice = random.choice(
                    [key for key in probDict.keys() if key != problem])
                problem = choice
                contents = probDict[problem]
                
            return redirect(url_for('wally.change_type', problem_pg=problem))
        else:
            return redirect(url_for('wally.index'))

    return render_template("writeCode.html", **args)


@wally.route('/background_process_delete')
def background_process_delete():
    global probDict
    global problem
    global contents
    func_name = request.args.to_dict()['func_name']
    Problem.query.filter_by(func_name=func_name).delete()
    probDict.pop(func_name, -1)
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        db.session.rollback()
    return redirect(url_for('wally.index'))


@wally.route('/background_process_writeCode')
def background_process_writeCode():
    code = request.args.get('code')
    try:
        exec(code)
        testAns = []
        for input in contents.testCaseInputs:
            print(str(input) + "\n\n\n")
            print(*input)
            print((contents.func_name + "({})".format(*input)))
            testAns += [eval(contents.func_name)(*input)]
        return jsonify(result=testAns)
    except Exception as e:
        traceback.print_exc()
        return jsonify(result="Error: " + str(e))


@wally.route('/background_process_testInputs')
def background_process_testInputs():

    yourOutput = json.loads(request.args.to_dict()['output'])
    input = request.args.to_dict()['input']
    try:
        exec(contents.function)
        correctAns = eval("{func}({input})".format(
            func=contents.func_name, input=input))
        if correctAns == yourOutput:
            return jsonify(result="true")
        else:
            return jsonify(result="false")
    except Exception as e:

        return jsonify(result="Error")


@wally.route('/background_process_testOutputs')
def background_process_testOutputs():
    yourInput = request.args.to_dict()['input']
    output = json.loads(request.args.to_dict()['output'])

    try:
        exec(contents.function)

        yourAns = eval("{func}({input})".format(
            func=contents.func_name, input=yourInput))
        if yourAns == output:
            return jsonify(result="true")
        else:
            return jsonify(result="false")
    except Exception:

        return jsonify(result="Error")


@wally.route('/background_process_testCode')
def background_process_testCode():
    input = (eval(json.loads(request.args.to_dict()['input'])))
    if type(input) != tuple:
        input = (input,)
    output = eval(json.loads(request.args.to_dict()['output']))
    code = request.args.to_dict()['code']
    func_call = code[4:code.index("(")]

    try:
        exec(code)  # try just running the code

    except Exception as e:
        return jsonify(result="Error: " + str(e))
    try:
        # try running code w/ given input
        print(input)
        calculatedAns = (eval(func_call))(*input)
    except Exception as e:
        traceback.print_exc()
        return jsonify(result="Error: " + str(e))
    if calculatedAns != output:
        return jsonify(result="Error: calculated output expected to be {}, but your output was {}.".format(calculatedAns, output))
    return jsonify(result="WALLY RULES!")


@wally.route('/background_process_checkFuncName')
def background_process_checkFuncName():
    func_name = request.args.to_dict()['func_name']
    if Problem.query.get(func_name) == None:
        return jsonify(result="valid")
    else:
        return jsonify(result="invalid")


@wally.route('/background_process_testBugs')
def background_process_testBugs():
    global contents
    input = json.loads(request.args.to_dict()['input'])

    exec(contents.buggy_function)

    try:
        ans = eval("{}({})".format(contents.func_name, input))
        return jsonify(result=json.dumps(ans))
    except Exception as e:
        return jsonify(result="Error: " + str(e))
