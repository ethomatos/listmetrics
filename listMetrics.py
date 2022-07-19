from argparse import ArgumentParser
import sys
import csv
import json
import requests

# set debug and active flags
debug = False
active = True

# Read in a csv file
def csvReader(options, file):
	with open(file, 'r') as file:
		csvreader = csv.reader(file)
		for row in csvreader:
			if (row[0] != 'Metric Name'):
				print("checking metric: " + row[0])
				runQuery(options, row[0])

# Read in API keys from a file
# The file format should be like this:
# apiKey:123456789
# appKey:123456789
def getAPIkeys(file):
	apiKey = None
	appKey = None
	with open(file) as apis:
		for line in apis:
			line.rstrip()	
			tag = line.split(':')
			if (tag[0] == "apiKey"):
				apiKey = tag[1]
				if (debug):
					print("apiKey = " + apiKey, end="")
			elif (tag[0] == "appKey"):
				appKey = tag[1]
				if (debug):
					print("appKey = " + appKey, end="")
	return(apiKey, appKey)

def runQuery(options, query):
	headers = { 
		'Content-Type': 'application/json',
		'DD-API-KEY': options['api_key'],
		'DD-APPLICATION-KEY': options['app_key']
	}
	query = 'https://api.datadoghq.com/api/v2/metrics/' + query + '/all-tags' 
	tags = requests.get(url=query, headers=headers)

	# Turn requested object into Python list
	json_tags = json.loads(json.dumps(tags.json()))
	for tag in json_tags['data']['attributes']['tags']:
		print(tag)

# Main routine of the program
def main(apifile):
	# Initialize Datadog API
	(apiKey, appKey) = getAPIkeys(apifile)
	options = {
		'api_key':apiKey.rstrip(),
		'app_key':appKey.rstrip()
	}

	if active:
		csvReader(options, './input.csv')

# Only executed as a standalone program, not from an import from another program
if __name__ == "__main__":
	parser = ArgumentParser(description='Get the tags for a metric ')
	helpText = "Enter a file to read in the API and APP keys each one on a separate line with this format:\n"
	helpText += "apiKey:123   appKey:123\n"
	parser.add_argument('-i', help=helpText, required=True)
	args = parser.parse_args()
	apifile = args.i if args.i else 'api.txt'
	main(apifile)
