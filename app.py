from flask import Flask, request, redirect, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from scrape import scrape, ping, people, pLayer
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
# callers2 = {
#     "+17733541500": "Jimbo",
#     "+16172837517": "Naseem",
#     "+16178524638": "Nadeem",
#     "+14349067428": "Papa Nic *shudder*",
#     "+17123105096": "Vidge Boy",
#     "+14145814507": "CarBar, JimJam loves you! Also"
# }

@app.route("/monkey", methods=['GET', 'POST'])
def hello_monkey():
	"""Respond and greet the caller by name."""

	
	test = scrape('http://cambridgema.iqm2.com/Citizens/Detail_LegalNotice.aspx?ID=1008')
	nextmtg = test[0]

	peoples = people()
	sheet = pLayer()

	# GET ROW NUMBER OF IDENTIFIED PERSON

	# this is a string
	incoming = request.values.get('Body', None)
	from_number = request.values.get('From', None)

	cnt = 0
	for key, val in peoples.items():
		cnt += 1
		if key == from_number:
			break

	incoming = incoming.lower()
	if 'start' in incoming:
		message = "Welcome back! MeetingBot here, you may remember me. If not, here's my deal. I only do one thing, but I do it well. For a weekly reminder of City Council meetings say weekly, for monthly say monthly, and to see the very next meeting say next. You can say stop or unsubscribe at any time."

	elif 'weekly' in incoming:
		message = "I'm on it. I'll send you a text once a week with details for the next two meetings. You can switch to monthly or stop getting alerts at any time, just say monthly or stop."

	elif 'monthly' in incoming:
		message = "I'm on it. I'll send you a text the day before the first meeting of each month with details for all of that month's meetings. You can switch to weekly or stop getting alerts at any time, just say weekly or stop."

	elif 'next' in incoming:
		preface = "Sure thing! Here's the next meeting: "
		meeting = nextmtg['date']+" "+nextmtg['time']+" "+nextmtg['agenda']
		message = preface + meeting

	else:
		if from_number in peoples:
			# write a cheeky message here cause they're trying to chat you up (or we have them on a member list)
			if peoples[from_number][2] == '1':
				message = "Hey " + peoples[from_number][1] + '... Are you trying to chat me up? I told you that I only do meeting alerts :)'
			else:
				message = "Hi " + peoples[from_number][1] + ", I'm the City Council MeetingBot. Is it creepy that I know who you are?"
				message = message + ' ' + 'I only do one thing, but I do it well. For a weekly reminder say "weekly", for monthly say "monthly" and to see only the very next meeting say "next". You can say "stop" or "unsubscribe" at any time.'
				sheet.update_cell(cnt+1, 4, "1")
		else:
			message = "Hi Beta Tester, I'm the City Council MeetingBot."
			message = message + ' ' + 'I only do one thing, but I do it well. For a weekly reminder say "weekly", for monthly say "monthly" and to see only the very next meeting say "next". You can say "stop" or "unsubscribe" at any time.'
			# ADD NEW LINE TO SHEET

		

	resp = MessagingResponse()
	resp.message(message)

	return str(resp)


if __name__ == "__main__":
	app.run(debug=False)
