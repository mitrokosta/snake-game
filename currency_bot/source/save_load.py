import datetime
import os
from utils import arguments_check as decorator
from utils import formatter
import data_handler as dh

CacheName = 'cache'

def folder_check():
  if not CacheName in os.listdir('.'):
    os.mkdir(CacheName)

@decorator(datetime.date)
def cache_check(date):
  folder_check()
  pth = '{}.json'.format(formatter(date, '_'))
  return pth in os.listdir(CacheName)

@decorator(datetime.date, dict)
def save(date, data):
  folder_check()
  pth = '{}/{}.json'.format(CacheName, formatter(date, '_'))
  with open(pth, 'w') as output:
    output.write(dh.datatojson(data))

@decorator(datetime.date)
def load(date):
  if not cache_check(date):
    raise Exception('Cache is not present.')
  pth = '{}/{}.json'.format(CacheName, formatter(date, '_'))
  with open(pth, 'r') as _input:
    js = _input.read()
  return dh.jsontodata(js)
  
