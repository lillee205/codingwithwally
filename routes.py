from flask import render_template, request, jsonify, url_for, redirect
import traceback
import pcode
import json
from model import Problem
import os
from database import db
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask.blueprints import Blueprint 

wally = Blueprint('wally', __name__, template_folder = "templates", static_folder = "static")
SQLALCHEMY_ECHO=True
# stores the current problem we are on
problem = ""
contents = ""
probDict = {}


def initDict(): #adds all problems currently in database to the dictionary probDict
    global probDict 
    probs = Problem.query.all()
    for prob in probs:
        if prob.func_name not in probDict:
            addToDict(prob)
    
def addToDict(problem): #adds one problem to probDict
    global probDict
    probDict[problem.func_name] = problem
    currP = probDict[problem.func_name] 
    probDict[problem.func_name].testInputs =json.loads(currP.testInputs)
    probDict[problem.func_name].testInputAnswers = json.loads(currP.testInputAnswers)
    probDict[problem.func_name].tags = json.loads(currP.tags)


@wally.route('/', methods=["POST", "GET"])
def index():
    global addProbInputs
    global addProbOutputs 
    addProbInputs = []
    addProbOutputs = []
    
    global problem
    global contents
    global probDict

    initDict()

    problem = ""
    contents = ""

    return render_template('index.html', problems = probDict)

addProbInputs = []
addProbOutputs = []

@wally.route("/addProb", methods = ["POST", "GET"])
def addProb():
    global addProbInputs
    global addProbOutputs 


    global probDict 
    initDict()

    if request.method == "POST":
        prob = ""
        function = request.form['function']
        func_call = function[function.index('def') + 4 : function.index(':')]
        func_name = func_call[:func_call.index("(")]
        desc = request.form['desc']

        testInputs = json.dumps(addProbInputs)
        testInputAnswers = json.dumps(addProbOutputs)
        tags = json.dumps(request.form.getlist('tag'))

        prob = Problem(func_name = func_name, func_call = func_call, desc = desc, testInputs = testInputs, testInputAnswers = testInputAnswers, tags = tags, function = function)
        try:
            db.session.add(prob)
            db.session.commit()

        except exc.SQLAlchemyError:
            print("\n\nredirect")
            traceback.print_exc()
            return redirect(url_for('wally.addProb'))
        print("problem successfully added!")
        addProbInputs = []
        addProbOutputs = []
        addToDict(prob)
    return render_template('addProb.html')


@wally.route('/<problem_pg>', methods=["POST", "GET"])
def change_type(problem_pg):

    global problem
    global contents

    initDict()

    if (problem_pg) in probDict:
        problem = problem_pg
        contents = probDict[problem]
    if request.method == "POST":
        newView = request.form.to_dict()['hiddenSelect']

        if newView == "test inputs":
            return render_template("testInputs.html", function_name=contents.func_name, description=contents.desc, tests=contents.testInputs, ansKey=contents.testInputAnswers, func_call=contents.func_call, tags = contents.tags)
        elif newView == "write code":
            return render_template("writeCode.html", function_name=contents.func_name, description=contents.desc, tests=contents.testInputs, ansKey=contents.testInputAnswers, func_call=contents.func_call, tags = contents.tags)
        elif newView == "test outputs":
            return render_template("testOutputs.html", function_name=contents.func_name, description=contents.desc, tests=contents.testInputs, ansKey=contents.testInputAnswers, func_call=contents.func_call, tags = contents.tags)
        else:
            return render_template("index.html")

    return render_template("writeCode.html", function_name=contents.func_name, description=contents.desc, tests=contents.testInputs, ansKey=contents.testInputAnswers, func_call=contents.func_call, tags = contents.tags)


@wally.route('/background_process_writeCode')
def background_process_writeCode():
    code = request.args.get('code')
    try:
        exec(code)
        testInputsJSON = json.loads(request.args.get('inputs'))
        testAns = pcode.checkAnswers(code, testInputsJSON)
        return jsonify(result=testAns)
    except Exception as e:
        # traceback.print_exc()
        return jsonify(result="Error: " + str(e))


@wally.route('/background_process_testInputs')
def background_process_testInputs():

    yourOutput = json.loads(request.args.to_dict()['output'])
    input = request.args.to_dict()['input']
    try:
        correctAns = eval("pcode.{func}({input})".format(func = contents['func_name'], input = input))
        if correctAns == yourOutput:
            return jsonify(result="true")
        else:
            return jsonify(result="false")
    except Exception as e:
        traceback.print_exc()
        return jsonify(result="Error")


@wally.route('/background_process_testOutputs')
def background_process_testOutputs():
    yourInput = request.args.to_dict['input']
    output = json.loads(request.args.to_dict['output'])

    try:
        yourAns = eval("pcode.{func}({input})".format(func = contents['func_name'], input = yourInput))
        if yourAns == output:
            return jsonify(result ="true")
        else:
            return jsonify(result="false")
    except Exception as e:
        #traceback.print_exc()
        return jsonify(result="Error")

@wally.route('/background_process_testCode')
def background_process_testCode():
    global addProbInputs
    global addProbOutputs

    input = request.args.to_dict()['input']
    output = json.loads(request.args.to_dict()['output'])
    code = request.args.to_dict()['code']
    func_call = code[4:code.index("(")]

    addProbInputs += [json.loads(input)] 
    addProbOutputs += [output]

    try:
        exec(code) # try just running the code
        
    except Exception as e:
        return jsonify(result="Error: " + str(e))
    try:
        calculatedAns = eval("{}({})".format(func_call, input)) # try running code w/ given input
    except Exception as e:
        return jsonify(result="Error: " + str(e))
    if calculatedAns != output:
        return jsonify(result="Error: calculated output expected to be {}, but your output was {}.".format(calculatedAns, output)) 
    return jsonify(result = "WALLY RULES!")
    
@wally.route('/background_process_checkFuncName')
def background_process_checkFuncName():
    func_name = request.args.to_dict()['func_name']
    if Problem.query.get(func_name) == None:
        return jsonify(result = "valid")
    else:
        return jsonify(result="invalid")