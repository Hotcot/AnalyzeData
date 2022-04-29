import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp


class AbsParser:
    
    links = [] # list of links
    titles = [] # list of titles
    texts = [] # list fo Text
    data_format_linux = [] # list of Data format Linux
    data_format_normal = [] # list of Data normal format
    
    url_general = "https://habr.com"
    
    # agent for browser
    headers = {
        "Accept": "*/*",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Mobile Safari/537.36 Edg/100.0.1185.36"
    }
    
    async def get_page_link_articles():
        pass
    
    # def ParsingTitles():
    #     pass
    
    # def ParsingTexts():
    #     pass
    
    # def ParsingData():
    #     pass