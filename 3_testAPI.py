import requests
import sys
import json
import time


url = 'http://192.168.1.2/api/' + hue_key + '/'

def lightsState():
	data = requests.get(url + 'lights/')
	objData = data.content.decode('utf-8')


try: 
	stato()

except KeyboardInterrupt:
	print("ciao")


