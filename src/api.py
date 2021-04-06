import flask 
import hashlib
from flask import jsonify, request
from slack_sdk.webhook import WebhookClient
import requests 
import json 
import redis

app = flask.Flask(__name__)
app.config["DEBUG"] = True
r = redis.Redis(host='localhost')


@app.route('/', methods=['GET'])
def home():
    return "<h1>TCMG 412 API Docker Project</h1>"

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
    if n == 1:
        return jsonify(input=n, output=False)
    elif (n==2):
        return jsonify(input=n, output=True)
    else:
        for i in range(2,n-1):
            if(n % i == 0):
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
		print(response.status_code)
		if(response.status_code == 200):
			posted = True
	except:
		print("An exception had occured!")
	return jsonify({"input:": message,"posted:": posted})

@app.route('/keyval/<string:key>', methods = ['DELETE', 'GET'])
def keyvaldg(key):
	json = {
		"command":"",
		"key":key,
		"value":"",
	}
	json["command"] = 'GET' if request.method == "GET" else "DELETE"
	try:
		testing = r.get(json["key"])
	except:
		json["error"] = "Cannot connect to redis."
		return jsonify(json), 400

	if testing == None:
		json["error"] = "Key value pair doesn't exist, cannot get/delete record."
		return jsonify(json), 404

	if request.method == 'GET':
		json["value"] = r.get(key)
		json["result"]=True
		return jsonify(json), 200
	elif request.method == 'DELETE':
		json["value"] = r.get(key)
		r.delete(key)
		json["result"]=True
		return jsonify(json), 200


@app.route('/keyval/', methods = ['POST', 'PUT'])
def keyvalpp():
	json = {
		"command":"",
		"key":"",
		"value":"",
	}
	json["command"] = 'CREATE' if request.method == "POST" else "UPDATE"
	try:
		payload = request.get_json()
		json["key"] = payload["key"]
		json["value"] = payload["value"]
		json["command"] += f" {payload['key']}/{payload['value']}"
	except:
		json["error"] = "Missing or malformed JSON in client request."
		return jsonify(json)

	try:
		testing = r.get(json["key"])
	except:
		json["error"] = "Cannot connect to redis."
		return jsonify(json)
	
	if request.method == "POST" and not testing == None:
		json["error"] = "Key value pair already exists, cannot create new record."
		return jsonify(json)
	
	elif request.method == "PUT" and testing == None:
		json["error"] = "Key doesn't exist, cannot update record."
		return jsonify(json), 404

	else:
		if(r.mset({payload["key"]:payload["value"]}) == False):
			json["error"] = "Could not set the value in Redis"
			return jsonify(json), 400
		else:
			json["result"] = True
			return jsonify(json), 200
			
app.run(host='0.0.0.0', port=5000, debug=True)
