from flask import Flask, render_template, request, jsonify
import traceback
import pcode

app = Flask(__name__)

@app.route('/', methods = ["POST", "GET"])
def index():
    return render_template('writeCode.html')

@app.route('/background_process_writeCode')
def background_process_writeCode():
  code = request.args.get('code')
  try:
    exec(code)
    testInputs = [
    [1, 2, 2, 1],
    [1,1],
    [1,2,2,1,13]
    ]
    correctAns, testAns = pcode.checkAnswers(code, pcode.correctFunc, testInputs)
    return jsonify(result = "the correct ans is {} and you had {}".format(correctAns, testAns))
  except Exception as e: 
    return jsonify(result = "there was an error. " + str(e))


@app.route('/background_process_testInputs')
def background_process_testInputs():
  input = eval(request.args.get('input'))
  ans = pcode.correctFunc(input)
  return jsonify(result = "the answer is " + str(ans))

@app.route('/background_process_testOutputs')
def background_process_testOutputs():
  output = eval(request.args.get('output'))
  ans = pcode.correctFunc(output)
  if ans == 9:
    return jsonify(result = "correct, an input of " + str(output) + " works")
  else:
    return jsonify(result = "incorrect, an input of {} gives you an output of {}".format(str(output), ans) )


@app.route('/change_type', methods = ["POST"])
def change_type():
  if request.method == "POST":
    newView = request.form.get("formChangeType")
    if newView == "testInputs":
      return render_template('testInputs.html')
    elif newView == "writeCode":
      return render_template("writeCode.html")
    elif newView == "testOutputs:":
      return render_template("testOutputs.html")
    else:
      return render_template("testOutputs.html")
if __name__ == "__main__":
    app.run(debug = True)

