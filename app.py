from flask import Flask, request, redirect, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from scrape import scrape, ping, people
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
	message = preface+randy['date']+" "+randy['time']+" "+randy['agenda']
	resp = MessagingResponse().message(message)
	return str(resp)

# This should live in a csv and be occasionally unloaded into logs
callers2 = {
    "+17733541500": "Jimbo",
    "+16172837517": "Naseem",
    "+16178524638": "Nadeem",
    "+14349067428": "Papa Nic *shudder*",
    "+17123105096": "Vidge Boy",
    "+14145814507": "CarBar, JimJam loves you! Also"
}

@app.route("/monkey", methods=['GET', 'POST'])
def hello_monkey():
	"""Respond and greet the caller by name."""

	people = people()
	test = scrape('http://cambridgema.iqm2.com/Citizens/Detail_LegalNotice.aspx?ID=1008')
	nextmtg = test[0]

	#sheet = pLayer()

	# this is a string
	incoming = request.values.get('Body', None)
	from_number = request.values.get('From', None)

	# if we know them, write temp variables for use later

	#record caller, time/date (anything else?) to csv or json, do something if we're already in a convo with them

	#if they're new, don't check for keywords, otherwise see if they're already subscribed or are changing their subscription

	#check to see if they've texted us before and how long its been
	# if 'next' in incoming:
	# 	preface = "Sure thing. Here's the next meeting: "
	# 	meeting = test[0]
	# 	message = preface + meeting
	# else:
	#     from_number = request.values.get('From', None)
	#     if from_number in people:
	#         message = "Hi " + callers[from_number][1] + ", I'm the City Council MeetingBot. Is it creepy that I know who you are?"
	#     else:
	#         message = "Hi Beta Tester, I'm the City Council MeetingBot."

	if 'next' in incoming:
	        preface = "Sure thing! Here's the next meeting: "
	        meeting = nextmtg['date']+" "+nextmtg['time']+" "+nextmtg['agenda']
	        message = preface + meeting
	else:
	    
	    if from_number in people:
	        message = "Hi " + people[from_number][1] + ", I'm the City Council MeetingBot. Is it creepy that I know who you are?"
	    else:
	        message = "Hi Beta Tester, I'm the City Council MeetingBot."
	    
		    # message = message + ' Your message was ' + '-' + incoming + '- '
		    # test = scrape('http://cambridgema.iqm2.com/Citizens/Detail_LegalNotice.aspx?ID=1008')
		    # randy = test[random.randint(0,len(test)-10)]
		    # preface = "Here's a random upcoming meeting: "
		    # message = message + preface + randy['date']+" "+randy['time']+" "+randy['agenda']

		    message = message + ' ' + 'I only do one thing, but I do it well. For a weekly meeting reminder, say "weekly", for monthly, say "monthly" and to see only the very next meeting, say "next". You can say "stop" or "unsubscribe" at any time.'

	resp = MessagingResponse()
	resp.message(message)

	return str(resp)


if __name__ == "__main__":
	app.run(debug=False)


