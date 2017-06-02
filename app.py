from flask import Flask, request, redirect, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from scrapetest import scrape

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

    resp = MessagingResponse().message("Hello, Mobile Monkey")
    return str(resp)

if __name__ == "__main__":
	app.run(debug=False)
