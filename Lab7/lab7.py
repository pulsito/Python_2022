from flask import Flask
from geopy.geocoders import Nominatim
from datetime import datetime
import requests


app = Flask(__name__)

@app.route("/")
def index():
	now = datetime.now()
	current_time = "Current time: "+now.strftime("%H:%M:%S")
	return current_time


@app.route("/<cityname>")
def timezone(cityname):
	try:
		geolocator = Nominatim(user_agent="MyApp")
		location = geolocator.geocode(cityname)
		uri = f"http://api.timezonedb.com/v2.1/get-time-zone?key=Q7GZ79LDSATA&format=json&by=position&lat={location.latitude}&lng={location.longitude}"
		response = requests.get(uri)
		data = response.json()
		gmt = int(data.get("gmtOffset")/3600)
		gmt_str = gmt if gmt < 0 else f"+{gmt}"
		time_now = datetime.utcfromtimestamp(data.get("timestamp")).strftime('%Y-%m-%d %H:%M:%S')
		info = f"Location: {location} |\
			 Longitude: {location.longitude} |\
			 Latitude:{location.latitude} |\
			 Time Zone: GMT {gmt_str}  |\
			 Current time: {time_now}"
		return info
	except:
		return "Wrong city name\n" 


if __name__ == '__main__':
    app.run()

