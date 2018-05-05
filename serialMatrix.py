import dateutil.parser
import pytz
import datetime
import serial
import urllib
import json

dock = serial.Serial(port="/dev/ttyS1", baudrate=57600)

now = datetime.datetime.now(pytz.timezone('US/Eastern'))
if((now.hour > 21) or (now.hour < 7)):
	print('off/')
	dock.write('\nOFF')
else:
	dock.write("Script Running...\n")
	
	dock.write(datetime.datetime.strftime(now, "%x") + "   |   ")

	url = "https://api.blockchain.info/stats"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	# print(data)
	dock.write("BTC = $%(number).2f   |   " % {"number" : data['market_price_usd']})

	url2 = "http://api.weather.gov/points/39.1945,-84.0546/forecast"
	response2 = urllib.urlopen(url2)
	forecast = json.loads(response2.read()) 
	summary = forecast['properties']['periods']
	for period in summary:
		startTime = dateutil.parser.parse(period['startTime'])
		endTime = dateutil.parser.parse(period['endTime'])
		if (datetime.datetime.now(pytz.utc) < endTime) and (datetime.datetime.now(pytz.utc) > startTime):
			dock.write(str(period['detailedForecast']) + "\n")
