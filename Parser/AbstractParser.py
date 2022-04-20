import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp


class AbsParser:
    
    list_links = [] # arr of links
    list_title = [] # arr of titles
    list_text = [] # arr fo Text
    list_data_format_linux = [] # arr of Data format Linux
    list_data_format_normal = [] # arr of Data normal format
    
    url_all = "https://habr.com/"
    
    # agent for browser
    headers = {
        "Accept": "*/*",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Mobile Safari/537.36 Edg/100.0.1185.36"
    }
    
    def ParsingLinks():
        pass
    
    # def ParsingTitles():
    #     pass
    
    # def ParsingTexts():
    #     pass
    
    # def ParsingData():
    #     pass