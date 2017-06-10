from flask import Flask, request, redirect, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from scrape import scrape, ping
import random
import threading

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api")
def serve_schedule():
	schedule = scrape('http://cambridgema.iqm2.com/Citizens/Detail_LegalNotice.aspx?ID=1008')
	return jsonify(schedule)

@app.route("/monkey2", methods=['GET', 'POST'])
def hello_monkey2():
	"""Respond to incoming calls with a simple text message."""

	test = scrape('http://cambridgema.iqm2.com/Citizens/Detail_LegalNotice.aspx?ID=1008')
	randy = test[random.randint(0,len(test)-10)]
	preface = "Hi Beta Tester, here's a random meeting: "
	mess = preface+randy['date']+" "+randy['time']+" "+randy['agenda']
	resp = MessagingResponse().message(mess)
	return str(resp)

# Try adding your own number to this list!
callers = {
    "+14158675309": "Curious George",
    "+14158675310": "Boots",
    "+14158675311": "Virgil",
    "+17733541500": "Jimbo",
    "+16172837517": "Naseem",
}

@app.route("/monkey", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""

    from_number = request.values.get('From', None)
    if from_number in callers:
        message = "Hi " + callers[from_number] + ", is it creepy that I know your name?"
    else:
        message = "Monkey, thanks for the message!"

    incoming = request.values.get('Body', None)

    message = message + '. Your message was ' + '-' + incoming + '-'

    resp = MessagingResponse()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
	app.run(debug=False)


