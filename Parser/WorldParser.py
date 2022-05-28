from requests import session
from .AbstractParser import *

import datetime

class WorldParser(AbsParser):
    
    __url_world = "https://apnews.com/hub/russia-ukraine?utm_source=apnewsnav&utm_medium=featured"  # Link for parsing    
    __url_root_link = "https://apnews.com/"
    __categories = 1
    
    def __init__(self):
        # start work programm
        startTime = datetime.datetime.now()
        print(startTime)                
        
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # потрібно для уникненння внутрішньої помилки при виклику асинхроної функції        
        link_articles = asyncio.run(self.get_page_link_articles()) # pars links articles
        
        if(link_articles != 0):
            asyncio.run(self.get_data_article(link_articles))
            # pass
                
            self.__write_date_toCSV()
            
            self.__save_data()
        
        self.__clear_lists() #clear data of global lists  
        
        finishTime = datetime.datetime.now() - startTime
        print(finishTime) # ended work programm


    async def get_page_link_articles(self):
        async with aiohttp.ClientSession() as session:         
            
            for page in range(1,2):
                url_pages = self.__url_world             
                
                async with session.get(url=url_pages, headers=self.headers) as response:
                    
                    response_text = await response.text()                    
                    soup = BeautifulSoup(response_text, "lxml")
                    
                    # archive-list mh-section mh-group                    
                    item_articles = soup.find_all("div", {"data-key": "feed-card-wire-story-with-image"})
                    for item in item_articles:
                        id_article = item.find("a").get("href")[-32:]
                        if(self.__check_repeatability_data_db(id_article)):
                            continue                                                             
                        else:
                            self.__get_id_article(item)
                            self.__get_link_article(item) 
                        
                        
                    # await asyncio.sleep(0.03) # затримка для виключення втрат даних при зверненню на сайт (втрачаются дані при )                
            return self.links       
        
    # function for get full data of articles
    async def get_data_article(self, links):
        
        async with aiohttp.ClientSession() as session:
            for article_link in links:
                
                url_article = f"{self.__url_root_link}{article_link}"
                async with session.get(url=url_article, headers=self.headers) as response:
                    
                    response_text = await response.text()           
                    soup = BeautifulSoup(response_text, "lxml")
                    
                    self.__get_title_article(soup)
                    self.__get_text_article(soup)
     
    def __get_id_article(self, item):
        self.id_article.append(item.find("a").get("href")[-32:])
        
    def __get_link_article(self, item):
        self.links.append(item.find("a").get("href"))
        
    def __get_title_article(self, soup):
        self.titles.append(soup.find("h1").text)
    
    def __get_text_article(self, soup):        
        text = soup.find("div", class_="Article")
        text = soup.find_all("p")
        text_article = ""
        for item in text:
            text_article += item.text
        text_article = text_article
        self.texts.append(text_article)
         
    def __write_date_toCSV(self):        
        for data in range(len(self.links)):
            
            res = [self.__categories, self.titles[data], self.id_article[data], self.links[data], self.texts[data]]
            
            with open("current.csv", "a", encoding="utf-8", newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL) 
                writer.writerow(res)
             
    def __clear_lists(self):
        self.links.clear()
        self.titles.clear()
        self.texts.clear()
        self.data_time.clear()
        self.id_article.clear()
        
    def __save_data(self):
        for item in range(len(self.links)):
            article = Article(
                link = ''.join((self.__url_root_link, self.links[item])),
                title = self.titles[item],
                date = datetime.datetime.now(),
                id_article = self.id_article[item],
                send_bin = 0
            )
            session.add(article)
        session.commit()
        
    def __check_repeatability_data_db(self, id_article):
        result = 0
        for instance in session.query(Article).filter(Article.id_article == id_article):
            result = instance.id_article
        return result