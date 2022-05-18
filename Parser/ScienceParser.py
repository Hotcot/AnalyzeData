from requests import session
from .AbstractParser import *

import datetime
import time

class ScienceParser(AbsParser):

    __topic_article = "science" # Theme articles
    __url_science = "https://scitechdaily.com/news/science/"  # Link for parsing
    __science = 4
    temp_counter = 0  # delete then
    
    def __init__(self):
        # start work programm
        startTime = datetime.datetime.now()
        print(startTime)                
        
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # потрібно для уникненння внутрішньої помилки при виклику асинхроної функції        
        link_articles = asyncio.run(self.get_page_link_articles()) # pars links articles
        
        asyncio.run(self.get_data_article(link_articles))
        # self.get_data_article(link_articles) # pars data of articles
                
        self.__write_date_toCSV()     
        
        self.__clear_lists() #clear data of global lists
        
        
        finishTime = datetime.datetime.now() - startTime
        print(finishTime) # ended work programm


    async def get_page_link_articles(self):
        async with aiohttp.ClientSession() as session:         
            
            for page in range(1,2):
                # pattern link (https://scitechdaily.com/news/science/page/2/)
                url_pages = f"{self.__url_science}page/{page}"                
                
                async with session.get(url=url_pages, headers=self.headers) as response:
                    
                    response_text = await response.text()                    
                    soup = BeautifulSoup(response_text, "lxml")
                    
                    # archive-list mh-section mh-group                    
                    item_articles = soup.find_all("article", class_="content-list")
                    
                    for item in item_articles:
                        self.links.append(item.find("a").get("href"))
                    # await asyncio.sleep(0.03) # затримка для виключення втрат даних при зверненню на сайт (втрачаются дані при )
            print(f"[INFO] Process page : {page} and count links {self.temp_counter}\n")                       
            return self.links       
            # return self.links
        
    # function for get full data of articles
    async def get_data_article(self, links):
        
        async with aiohttp.ClientSession() as session:
            for article_link in links:
                                
                async with session.get(url=article_link, headers=self.headers) as response:
                    
                    response_text = await response.text()           
                    soup = BeautifulSoup(response_text, "lxml")
                    
                    self.__get_title_article(soup)
                    self.__get_text_article(soup)
                    self.__get_date_article(soup)
                    # return 0                       

        
    def __get_title_article(self, soup):
        self.titles.append(soup.find("h1", class_="entry-title").text)
        # print(self.titles)
    
    def __get_text_article(self, soup):
        self.texts.append(soup.find("div", class_="entry-content clearfix").text)
        
    def __get_date_article(self, soup):
        temp_date = soup.find("span", class_="entry-meta-date updated").text
        temp_date = temp_date.replace(',',"")
        edit_date = datetime.datetime.strptime(f'{temp_date}', '%B %d %Y').strftime('%d-%m-%Y')
        self.data_time.append(edit_date)
         
    def __write_date_toCSV(self):        
        for data in range(len(self.links)):
            
            res = [self.__science, self.titles[data], self.texts[data]]
            
            with open("train.csv", "a", encoding="utf-8", newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL) 
                writer.writerow(res)
             
    def __clear_lists(self):
        self.links.clear()
        self.titles.clear()
        self.texts.clear()
        self.data_time.clear()
        

       