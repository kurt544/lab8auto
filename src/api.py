import flask 
import hashlib
from flask import jsonify
from slack_sdk.webhook import WebhookClient
import requests 
import json 

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

@app.route('/is-prime/<int:n>')
def prime_check(n):
    number = isinstance(n, int)
    if number == 1:
        return jsonify(input=n, output=False)
    elif (number==2):
        return jsonify(input=n, output=True)
    else:
        for i in range(2,n):
            if(number % i==0):
               return jsonify(input=n, output=False)
        return jsonify(input=n, output=True)
@app.route('/slack-alert/<string:message>')
def slack_message(message):
	posted = False
	try:
		webhook_url = "https://hooks.slack.com/services/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"
		slack_data = {'text': message}
		response = requests.post(
			webhook_url, data=json.dumps(slack_data))
		posted = True
	except:
		print("An exception had occured!")
	return jsonify({"input:": message,"posted:": posteds})
app.run()
