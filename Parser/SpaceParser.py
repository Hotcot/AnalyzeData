from requests import session
from .AbstractParser import *
import datetime
import time


class SpaceParser(AbsParser):

    __topic_article = "space" # Theme articles
    __url_space = "https://habr.com/ru/hub/space/"  # Link for parsing
    __space = 4
    temp_counter = 0  # delete then
    
    def __init__(self):
        # start work programm
        startTime = datetime.datetime.now()
        print(startTime)                
        
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # потрібно для уникненння внутрішньої помилки при виклику асинхроної функції
        
        link_articles = asyncio.run(self.get_page_link_articles()) # pars links articles
        
        # asyncio.run(self.get_data_article(link_articles))
        self.get_data_article(link_articles) # pars data of articles
                
        self.__write_date_toCSV()      
        
        self.__clear_lists() #clear data of global lists
        
        
        finishTime = datetime.datetime.now() - startTime
        print(finishTime) # ended work programm


    async def get_page_link_articles(self):
        async with aiohttp.ClientSession() as session:         
            
            for page in range(1,51):
                
                url_pages = f"{self.__url_space}page{page}/"
                
                async with session.get(url=url_pages, headers=self.headers) as response:
                    
                    response_text = await response.text()
                    
                    soup = BeautifulSoup(response_text, "lxml")
                    
                    link_items = soup.find_all("a", class_="tm-article-snippet__title-link")
                    
                    for item in link_items:
                        self.links.append(item.get("href"))
                    await asyncio.sleep(0.03) # затримка для виключення втрат даних при зверненню на сайт (втрачаются дані при )
            print(f"[INFO] Process page : {page} \n")                       
            return self.links     
    
    def get_data_article(self, links):
        
        for article in links:     
                       
            url_article = f"{self.url_general}{article}"                            
            req = requests.get(url=url_article, headers=self.headers)     
            soup = BeautifulSoup(req.text, "lxml")
            self.__get_title_article(soup)
            self.__get_text_article(soup)
            # self.__get_date_article(soup)
            # self.__get_tags_article(soup)               

        
    def __get_title_article(self, soup):
        self.titles.append(soup.find("h1", class_="tm-article-snippet__title tm-article-snippet__title_h1").text)
    
    def __get_text_article(self, soup):
        self.texts.append(soup.find("div", {"id": "post-content-body"}).text)
        
    def __get_date_article(self, soup):
        self.data_time.append(soup.find("time").get("datetime"))
         
    def __write_date_toCSV(self):        
        for data in range(len(self.links)):
            
            res = [self.__space, self.titles[data], self.texts[data]]
            
            with open("train.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL) 
                writer.writerow(res)
                
    # def __get_tags_article(self, soup):
    #     soup.find_all("")
                
    def __clear_lists(self):
        self.links.clear()
        self.titles.clear()
        self.texts.clear()
        self.data_time.clear()
        

       