import json
import os
import pprint
import time
import requests
from influxdb import InfluxDBClient

API_URL = 'https://supportxmr.com/api/miner/{0}/stats'
WALLET = os.environ['W']

def sendRequest():
	response = requests.get(api_endpoint)

	return response.json()

def sendToInflux(msg):
	val = float(msg["amtDue"]) / 1000000000000
	print(val)
	json_body = [
		{
			"measurement": "smxr",
			"tags": {
			    "w": WALLET
			},
			"time": int(time.time()), # * 1000000000,
			"fields": {
			    "due": val,
                            "hash": int(msg["hash"]),
			}
		}
	]

	params = {"precision": "s"}
	client.write_points(json_body, time_precision='s')


pp = pprint.PrettyPrinter(indent=4)
api_endpoint = API_URL.format(WALLET)
influx_host = os.environ['INFLUXDB_HOST']
influx_port = os.environ['INFLUXDB_PORT']
influx_db = os.environ['INFLUXDB_DB']
interval = 60

print("Connecting to influxdb at {0}".format(influx_host))
client = InfluxDBClient(influx_host, influx_port, '', '', influx_db)

while (1): 
	resp = sendRequest()
	pp.pprint(resp)
	sendToInflux(resp)
	time.sleep(interval)
	


