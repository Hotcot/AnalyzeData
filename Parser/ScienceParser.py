from requests import session
from .AbstractParser import *
import datetime

class ScienceParser(AbsParser):

    topic_article = "science"
    url_science = "https://habr.com/ru/hub/popular_science/"  # link for parsing
    temp_counter = 0  # delete then
    
    def __init__(self):
        # start work programm
        startTime = datetime.datetime.now()
        print(startTime)        
        
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())# потрібно для уникненння внутрішньої помилки при виклику асинхроної функції
        link_articles = asyncio.run(self.get_page_link_articles())
        
        text_titles = asyncio.run(self.get_data_of_article(link_articles))
        
        #очистка даних зі списків
        self.clear_lists()
        # ended work programm
        finishTime = datetime.datetime.now() - startTime
        print(finishTime)


    async def get_page_link_articles(self):
        async with aiohttp.ClientSession() as session:
            # response = await session.get(url=self.urlScience, headers=self.headers)
            # soup = BeautifulSoup(await response.text(), "lxml")
            # allLinksHref = soup.find_all("a", class_="tm-article-snippet__title-link")            
            
            for page in range(1,2):
                url_pages = f"https://habr.com/ru/hub/popular_science/page{page}/"
                # print(f"{page} ////////////////////")
                # task = asyncio.create_task(self.get_page_data_links(session, page))
                async with session.get(url=url_pages, headers=self.headers) as response:
                    
                    response_text = await response.text()
                    
                    soup = BeautifulSoup(response_text, "lxml")
                    
                    link_items = soup.find_all("a", class_="tm-article-snippet__title-link")
                    for item in link_items:
                        self.links.append(item.get("href"))
                        print(item.get("href"))
                    await asyncio.sleep(0.03) # задержка для предотвращения потерь данных с сайта (пропадают данные в общем)
                    print(f"[INFO] Process page : {page} \n\n\n")
                    
            
            # print(self.list_links)    
            return self.links
        
        
    async def get_data_of_article(self, links):
        
        async with aiohttp.ClientSession() as session:
            
            for article in links:
                url_article = f"{self.url_general}{article}"
                
                async with session.get(url=url_article, headers=self.headers) as response:
                    
                    response_text = await response.text()                    
                    soup = BeautifulSoup(response_text, "lxml")
                    self.get_title_of_article(soup)
                    self.get_text_of_article(soup)
                    
                        
            
    def clear_lists(self):
        self.links.clear()
        
    def get_title_of_article(self, soup):
        self.titles.append(soup.find("h1", class_="tm-article-snippet__title tm-article-snippet__title_h1").text)
        return self.titles
    
    def get_text_of_article(self, soup):
        texts =  soup.find_all("p").text

       