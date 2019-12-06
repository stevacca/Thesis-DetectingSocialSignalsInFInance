from bs4 import BeautifulSoup
import requests
import pandas as pd

from requests import get
url = 'https://coinmarketcap.com/currencies/ripple/historical-data/?start=20130428&end=20180802'
response = get(url)
print(response.text[:500])