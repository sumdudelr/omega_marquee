# This is for writing to matrix display through Arduino dock

import serial
import datetime
import pytz
import urllib.request
import json

dock = serial.Serial(port='/dev/ttyS1', baudrate=57600)

dock.write(str.encode("Running\0"))

now = datetime.datetime.now(pytz.timezone('US/Eastern'))

dateString = now.strftime('%a %b %d, %Y')

dock.write(str.encode(dateString + '   |   '))

try:
  url = "https://api.blockchain.info/stats"
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  st = "BTC = $%(number).2f   |   " % {"number" : data['market_price_usd']}
  dock.write(str.encode(st))

  # Batavia, OH 39.1060,-84.2411  ILN Grid points 44, 38
  url = "https://api.weather.gov/gridpoints/ILN/44,38/forecast"
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  summary = data['properties']['periods'][0]
  string = summary['name'] + ': ' + summary['detailedForecast']

  dock.write(str.encode(string))
  
except:
  # Maybe no internet connection?
  dock.write(str.encode("Internet not available"))
  
finally:
  dock.write(str.encode("\0"))
  dock.close()
