import requests
from utils import arguments_check as decorator
import xmljson
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import json

@decorator(requests.Response)
def xmltodata(response):
  return bf.data(fromstring(response.text))

@decorator(dict)
def datatojson(data):
  return json.dumps(data, indent=4, ensure_ascii=False)

@decorator(str)
def jsontodata(jsdata):
  return json.loads(jsdata)

