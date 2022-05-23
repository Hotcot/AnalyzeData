from requests import session
from .AbstractParser import *

import datetime

class BusinessParser(AbsParser):

    __topic_article = "business" # Theme articles
    __url_business = "https://www.bbc.com/news/business"  # Link for parsing
    __url_root_link = "https://www.bbc.com"
    __categories = 3
    temp_counter = 0  # delete then
    
    def __init__(self):
        # start work programm
        startTime = datetime.datetime.now()
        print(startTime)                
        
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # потрібно для уникненння внутрішньої помилки при виклику асинхроної функції        
        link_articles = asyncio.run(self.get_page_link_articles()) # pars links articles
        
        if(link_articles != 0):
            asyncio.run(self.get_data_article(link_articles))
                
            self.__write_date_toCSV()
            
            self.__save_data()
        
        self.__clear_lists() #clear data of global lists
        
        
        finishTime = datetime.datetime.now() - startTime
        print(finishTime) # ended work programm


    async def get_page_link_articles(self):
        async with aiohttp.ClientSession() as session:         
            
            for page in range(1,2):
                url_pages = self.__url_business                
                
                async with session.get(url=url_pages, headers=self.headers) as response:
                    
                    response_text = await response.text()                    
                    soup = BeautifulSoup(response_text, "lxml")
                    
                    # archive-list mh-section mh-group                    
                    item_articles = soup.find_all("article", class_="qa-post gs-u-pb-alt+ lx-stream-post gs-u-pt-alt+ gs-u-align-left")
                    
                    for item in item_articles:
                        #make check data-parse with db data
                        if(len(item.get("id"))==13):
                            #check data with db
                            id_article = item.get("id")[-8:]
                            if(self.__check_repeatability_data_db(id_article)):
                                # print("//////////////////////false/////////////////")# qa-heading-link lx-stream-post__header-link  
                                continue                                                             
                            else:
                                if(item.find("a").get("class") == ['qa-heading-link', 'lx-stream-post__header-link']):                                
                                    self.__get_id_article(item)
                                    self.__get_link_article(item)                                
                                else:
                                    continue                                                           
                        else:
                            continue  
                        
                    # await asyncio.sleep(0.03) # затримка для виключення втрат даних при зверненню на сайт (втрачаются дані при )
            # print(f"[INFO] Process page : {page}\n")                       
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
                    print(url_article)                

        
    def __get_id_article(self, item):
        self.id_article.append(item.find("a", class_="qa-heading-link lx-stream-post__header-link").get("href")[-8:])
        
    def __get_link_article(self, item):
        self.links.append(item.find("a", class_="qa-heading-link lx-stream-post__header-link").get("href"))
        
    def __get_title_article(self, soup):
        self.titles.append(soup.find("h1").text)
    
    def __get_text_article(self, soup):
        self.texts.append(soup.find("article").text)
        
    # def __get_date_article(self, soup):
    #     temp_date = soup.find("time", {"data-testid": "timestamp"}).get("datetime")
    #     self.data_time.append(datetime.datetime.strptime(f'{temp_date}', '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d-%m-%Y'))
         
    def __write_date_toCSV(self):        
        for data in range(len(self.links)):
            
            res = [self.__categories, self.titles[data], self.texts[data]]
            
            with open("test.csv", "a", encoding="utf-8", newline='') as file:
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
        for instance in session.query(Article).filter(Article.id_article ==  id_article):
            result = instance.id_article
        return result

       