from flask import Flask, request,  render_template
import requests


app = Flask(__name__)

@app.route("/")
def index():
	ip_addr = requests.get("https://checkip.amazonaws.com/").text
	print(ip_addr)
	uri = "http://api.ipstack.com/"+ip_addr[:13]+"?access_key=548029d93135a606cd06a47b8b5955ec"
	response = requests.get(uri)
	data = response.json() 	
	return render_template('index.html', data = data)



if __name__ == '__main__':
    app.run()

