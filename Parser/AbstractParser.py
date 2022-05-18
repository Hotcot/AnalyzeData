import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import csv

import psycopg2

from Models.config import host, user, password, db_name


class AbsParser:
    
    links = [] # list of links
    titles = [] # list of titles
    texts = [] # list fo Text
    # data_format_iso = [] # list of Data format Linux
    data_time = [] # list of Data normal format
    tags = []
    
    # agent for browser
    headers = {
        "Accept": "*/*",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Mobile Safari/537.36 Edg/100.0.1185.36"
    }
    
    async def get_page_link_articles():
        pass
    
    async def get_data_article():
        pass
        