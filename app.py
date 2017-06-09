from flask import Flask, request, redirect, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from scrape import scrape
import random

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api")
def serve_schedule():
	schedule = scrape('http://cambridgema.iqm2.com/Citizens/Detail_LegalNotice.aspx?ID=1008')
	return jsonify(schedule)

@app.route("/monkey", methods=['GET', 'POST'])
def hello_monkey():
	"""Respond to incoming calls with a simple text message."""

	test = scrape('http://cambridgema.iqm2.com/Citizens/Detail_LegalNotice.aspx?ID=1008')
	randy = test[random.randint(0,len(test)-10)]
	preface = "Hi test monkey, here's a random meeting: "
	mess = preface+randy['date']+" "+randy['time']+" "+randy['agenda']
	resp = MessagingResponse().message(mess)
	return str(resp)

if __name__ == "__main__":
	app.run(debug=False)
