from flask import Flask, render_template, request, jsonify
import traceback
import pcode
import html
import random
import json
from problems import *
app = Flask(__name__)

#stores the current problem we are on
problem = ""
contents = ""


@app.route('/', methods=["POST", "GET"])
def index():
    global problem
    global contents

    if request.method == "POST":
        problem = request.form.to_dict()['hiddenChoose']
        if problem in probDict:
            contents = probDict[problem] 
        else:
            return render_template("index.html") # if key error, go back to index html
        return render_template("writeCode.html", function_name=contents['func_name'], description=contents['desc'], tests=contents['testInputs'], ansKey=contents['testInputAnswers'], func_call=contents['func_call'])
    else:
        return render_template('index.html')


@app.route('/change_type', methods=["POST", "GET"])
def change_type():
    global problem
    global contents

    if request.method == "POST":
        newView = request.form.to_dict()['hiddenSelect']
        if newView == "test inputs":
            return render_template("testInputs.html", function_name=contents['func_name'], description=contents['desc'], tests=contents['testInputs'], ansKey=contents['testInputAnswers'], func_call=contents['func_call'])
        elif newView == "write code":
            return render_template("writeCode.html", function_name=contents['func_name'], description=contents['desc'], tests=contents['testInputs'], ansKey=contents['testInputAnswers'], func_call=contents['func_call'])
        elif newView == "test outputs":
            return render_template("testOutputs.html", function_name=contents['func_name'], description=contents['desc'], tests=contents['testInputs'], ansKey=contents['testInputAnswers'], func_call=contents['func_call'])
        elif newView == "home":
            problem = ""
            contents = ""
            return render_template("index.html")
        elif newView == "rand":
            rand = random.choice(list(probDict.keys()))
            problem = rand
            contents = probDict[problem]
            return render_template("writeCode.html", function_name=contents['func_name'], description=contents['desc'], tests=contents['testInputs'], ansKey=contents['testInputAnswers'], func_call=contents['func_call'])
        else:
            return render_template("index.html")


@app.route('/background_process_writeCode')
def background_process_writeCode():
    code = request.args.get('code')
    try:
        exec(code)
        print(request.args.get('inputs'))
        testInputsJSON = json.loads(request.args.get('inputs'))
        testAns = pcode.checkAnswers(code, testInputsJSON)
        return jsonify(result=testAns)
    except Exception as e:
        #traceback.print_exc()
        return jsonify(result="Error: " + str(e))


@app.route('/background_process_testInputs')
def background_process_testInputs():

    yourOutput = json.loads(request.args.get('output'))
    input = json.loads(request.args.get('input'))
    try:
        correctAns = eval(
            "pcode." + contents[4][: (contents[4].index("("))] + "(" + str(input) + ")")
        if correctAns == yourOutput:
            return jsonify(result="true")
        else:
            return jsonify(result="false")
    except Exception as e:
        #traceback.print_exc()
        return jsonify(result="Error")


@app.route('/background_process_testOutputs')
def background_process_testOutputs():
    output = eval(request.args.get('output'))
    ans = eval(
        "pcode." + contents[4][: (contents[4].index("("))] + "(" + str(output) + ")")
    if ans == 9:
        return jsonify(result="Correct, an input of " + str(output) + " works")
    else:
        return jsonify(result="Incorrect, an input of {} gives you an output of {}".format(str(output), ans))


if __name__ == "__main__":
    app.run(debug=True)
