import requests, json, sys
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime


def request_json():
	print 'Begin request to get the json...'

	# Try get request once
	response = requests_retry_session().get('https://api.coindesk.com/v1/bpi/currentprice/USD.json')
	if (response.status_code == 200):
		print 'Fetched price succesfully.\n'
		return response.json()

	# When above didn't succeed, retry 3 times using session 
	s = requests.Session()
	response = requests_retry_session(session=s).get(
	    'https://api.coindesk.com/v1/bpi/currentprice/USD.json'
	)
	# When requests succeeds using session
	if (response.status_code == 200):
		print 'Fetched price succesfully.\n'
		return response.json()

	print 'Couldn\'t fetch price json.'
	return 'error'


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):

    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    return session




def get_price_data(json):

	price = str(json['bpi']['USD']['rate'])
	# Strip the ',' from price, convert to float and to int
	price = int(float(price.replace(',', '')))

	return price




def main():
	# Send a request for the bitcoin price json
	priceJson = request_json()
	# Check if the request and retries failed
	if (json == 'error'):
		print 'Terminating bitcoinPrice.py script.'
		sys.exit()

	# Get the data from the response json
	priceInt = get_price_data(priceJson)

	# Get timestamp
	# Returns a datetime object containing the local time
	dateTimeObj = datetime.now()
	date = dateTimeObj.strftime("%d-%b-%Y %H:%M")
	
	# Read the colordata from colors.txt
	# The format is: '63,61' where greenCount,redCount
	fh = open('colors.txt', 'r')
	colorData = fh.read()
	gCount = colorData.split(',')[0]
	rCount = colorData.split(',')[1]

	# Create a string with the price and color data
	dataString = "{\"timestamp\": %s, \"price\": %d, \"gCount\": %s, \"rCount\": %s}" % (str(date), priceInt, gCount, rCount)
	print dataString

	# Read and write to results.txt
	fh = open('results.txt', 'a')
	fh.write(dataString + '\n')
	fh.close()
	print '\nSuccesfully saved BTC price and color data to results.txt'




if __name__ == '__main__':
    main()
