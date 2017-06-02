from flask import Flask, jsonify
from scrapetest import scrape

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api")
def serve_schedule():
	schedule = scrape('http://cambridgema.iqm2.com/Citizens/Detail_LegalNotice.aspx?ID=1008')
	return jsonify(schedule)

if __name__ == "__main__":
	app.run(debug=False)
