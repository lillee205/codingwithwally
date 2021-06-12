from flask import Flask, render_template, request, jsonify, session, flash
import traceback
import pcode
import html
import random
import json
from problems import *
"""
from flask_sqlalchemy import SQLAlchemy
"""
app = Flask(__name__)
"""
app.config['SQLACHEMY_DATABSE_URI'] = 'sqlite:///problems.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Problem(db.Model):
    func_name = db.Column("func_name", db.String(50), primary_key = True)
    func_call = db.Column(db.String(70), nullable = False)
    desc = db.Column(db.String, nullable = False)
    testInputs = db.Column(db.String, nullable = False)
    testInputAnswers = db.Column(db.String, nullable = False)
    tags = db.Column(db.String, nullable = False)
    function = db.Column(db.String, nullable = False)
    
    def __repr__(self):
        return '<Problem %r' % self.func_name
"""
# stores the current problem we are on
problem = ""
contents = ""


@app.route('/', methods=["POST", "GET"])
def index():
    global problem
    global contents

    problem = ""
    contents = ""

    if request.method == "POST":
        problem = request.form.to_dict()['hiddenChoose']
        if problem in probDict:
            contents = probDict[problem]

    return render_template('index.html', problems = probDict)


@app.route('/<problem_pg>', methods=["POST", "GET"])
def change_type(problem_pg):
    global problem
    global contents
    if (problem_pg) in probDict:
        problem = problem_pg
        contents = probDict[problem]
    if request.method == "POST":
        newView = request.form.to_dict()['hiddenSelect']

        if newView == "test inputs":
            return render_template("testInputs.html", function_name=contents['func_name'], description=contents['desc'], tests=contents['testInputs'], ansKey=contents['testInputAnswers'], func_call=contents['func_call'], tags = contents['tags'])
        elif newView == "write code":
            return render_template("writeCode.html", function_name=contents['func_name'], description=contents['desc'], tests=contents['testInputs'], ansKey=contents['testInputAnswers'], func_call=contents['func_call'], tags = contents['tags'])
        elif newView == "test outputs":
            return render_template("testOutputs.html", function_name=contents['func_name'], description=contents['desc'], tests=contents['testInputs'], ansKey=contents['testInputAnswers'], func_call=contents['func_call'], tags = contents['tags'])
        else:
            return render_template("index.html")

    return render_template("writeCode.html", function_name=contents['func_name'], description=contents['desc'], tests=contents['testInputs'], ansKey=contents['testInputAnswers'], func_call=contents['func_call'], tags = contents['tags'])


@app.route('/background_process_writeCode')
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


@app.route('/background_process_testInputs')
def background_process_testInputs():

    yourOutput = json.loads(request.args.get('output'))
    input = request.args.get('input')
    try:
        correctAns = eval("pcode.{func}({input})".format(func = contents['func_name'], input = input))
        if correctAns == yourOutput:
            return jsonify(result="true")
        else:
            return jsonify(result="false")
    except Exception as e:
        traceback.print_exc()
        return jsonify(result="Error")


@app.route('/background_process_testOutputs')
def background_process_testOutputs():
    yourInput = request.args.get('input')
    output = json.loads(request.args.get('output'))
    print(yourInput)
    print(output)
    try:
        yourAns = eval("pcode.{func}({input})".format(func = contents['func_name'], input = yourInput))
        print("the answer u get is " + str(yourAns))
        if yourAns == output:
            return jsonify(result ="true")
        else:
            return jsonify(result="false")
    except Exception as e:
        traceback.print_exc()
        return jsonify(result="Error")


if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)
