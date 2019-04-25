import datetime
import requests
from utils import arguments_check as decorator
from utils import formatter

@decorator(datetime.date)
def daily_currencies(date):
  url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'
  return requests.get(url.format(formatter(date, '/')))
