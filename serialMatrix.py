import dateutil.parser
import pytz
import datetime
import serial
import urllib
import json
import geojson

dock = serial.Serial(port="/dev/ttyS1", baudrate=57600)
dock.write("Script Running...\n")

now = datetime.datetime.now(pytz.timezone('US/Eastern'))

dock.write(datetime.datetime.strftime(now, "%x") + "   |   ")

url = "https://api.blockchain.info/stats"
response = urllib.urlopen(url)
data = json.loads(response.read())
# print(data)
dock.write("BTC = $" + str(data['market_price_usd']) + "   |   ")

url2 = "http://api.weather.gov/points/39.1945,-84.0546/forecast"
response2 = urllib.urlopen(url2)
forecast = geojson.loads(response2.read()) 
summary = forecast['properties']['periods']
for period in summary:
	startTime = dateutil.parser.parse(period['startTime'])
	endTime = dateutil.parser.parse(period['endTime'])
	if (datetime.datetime.now(pytz.utc) < endTime) and (datetime.datetime.now(pytz.utc) > startTime):
		dock.write(str(period['detailedForecast']) + "\n")

offTime = now.replace(hour=21, minute=0)
onTime = now.replace(hour=7, minute=0)
if((now > offTime) & (now < onTime)):
	dock.write('\nOFF')
