import flask 
import hashlib
from flask import jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/md5/<string:str2hash>',methods=['GET'])
def api_md5(str2hash):
	response = {
		"input": str2hash,
		"output":((hashlib.md5(str2hash.encode())).hexdigest())
	}
	return jsonify(response)

@app.route('/factorial/<int:factorial>',methods=['GET'])
def api_factorial(factorial):
	factorial_value = 1
	for i in range(2,factorial+1):
		factorial_value = i*factorial_value
	response = {
		"input": factorial,
		"output": factorial_value
	}
	return jsonify(response)

@app.route('/fibonacci/<int:fib_input>',methods = ['GET'])
def api_fibbonacci(fib_input):
	sequence = [0,1]
	while(sequence[-1] +sequence[-2] < fib_input):
		sequence.append(sequence[-2]+sequence[-1])
	response = {
		"input": fib_input,
		"output": sequence
	}
	return jsonify(response)

@app.route('/slack-alert/<string:>')
def api_slack_alert():
   pass
app.run()
