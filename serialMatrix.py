import dateutil.parser
import pytz
import datetime
import serial
import urllib
import json
import geojson

dock = serial.Serial(port="/dev/ttyS1", baudrate=57600)
dock.write("Script Running...\n")

dock.write(datetime.datetime.strftime(datetime.datetime.now(pytz.utc), "%x") + "   |    ")

url = "https://api.blockchain.info/stats"
response = urllib.urlopen(url)
data = json.loads(response.read())
# print(data)
dock.write("BTC = $" + str(data['market_price_usd']) + "   |   ")
blocksToSegWit = 481824 - data['n_blocks_total']
timeToSegWit = blocksToSegWit * data['minutes_between_blocks'] / 60
dock.write("SegWit activates in " + str(blocksToSegWit) + " blocks or approx. " + "{:.1f}".format(timeToSegWit) + " hours   |   ")

url2 = "http://api.weather.gov/points/39.1056,-84.2416/forecast"
response2 = urllib.urlopen(url2)
forecast = geojson.loads(response2.read()) 
summary = forecast['properties']['periods']
for period in summary:
	startTime = dateutil.parser.parse(period['startTime'])
	endTime = dateutil.parser.parse(period['endTime'])
	if (datetime.datetime.now(pytz.utc) < endTime) and (datetime.datetime.now(pytz.utc) > startTime):
		dock.write(str(period['detailedForecast']) + "\n")
		print(type(period['startTime']))

