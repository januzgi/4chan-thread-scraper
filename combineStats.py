import requests, json, sys, time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def read_json():
	fh = open('results/priceJson.txt', 'r')
	jsonData = fh.read()
	print 'Read priceJson.txt'
	return jsonData


def get_price_data(json):
	price = str(json['USD']['last'])
	# Convert to float and to int
	price = int(float(price))
	return price


def main():
	# Read BTC price from the json
	priceJson = read_json()
	# Get the data from the response json
	priceInt = get_price_data(json.loads(priceJson))
	# Get timestamp as milliseconds
	milli_sec = int(round(time.time() * 1000))
	# Add 3 hours to make it Helsinki local time
	milli_sec = milli_sec + 10800000
	
	# Read the colordata from colors.txt
	# The format is: '63,61' where greenCount,redCount
	fh = open('colors.txt', 'r')
	colorData = fh.read()
	gCount = colorData.split(',')[0]
	rCount = colorData.split(',')[1]

	# Create a string in json format with the price and color data
	dataString = "{\"timestamp\": \"%d\", \"price\": \"%d\", \"gCount\": \"%s\", \"rCount\": \"%s\"}" % (milli_sec, priceInt, gCount, rCount)
	print dataString

	# Read and write to resultsTest.txt
	fh = open('results/results.txt', 'a')
	fh.write(dataString + '\n')
	fh.close()
	print '\nSuccesfully saved BTC price and color data to results.txt'



if __name__ == '__main__':
    main()