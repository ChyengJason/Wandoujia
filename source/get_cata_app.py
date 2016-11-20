import json
import bs4
from bs4 import BeautifulSoup
from source._const import const
import requests

class CataAppInfo(object):
    def __init__(self,cata_url):
        self.cata_url = cata_url
        self.app_count = 0
        self.app