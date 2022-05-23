import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

import csv

import psycopg2

from Models.alchemy_decl import Article
from Models.session_db import session

# from Models.config import host, user, password, db_name


class AbsParser:
    
    links = [] # list of links
    titles = [] # list of titles
    texts = [] # list fo Text
    data_time = [] # list of Data normal format
    id_article = []
    
    # agent for browser
    headers = {
        "Accept": "*/*",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36 Edg/101.0.1210.53"
    }
        