from requests import session
from .AbstractParser import *
import datetime

class ScienceParser(AbsParser):

    urlScience = "https://habr.com/ru/hub/popular_science/"  # link for parsing
    tempCounter = 0  # delete then
    
    def __init__(self):
        startTime = datetime.datetime.now()
        print(startTime)        
        
        # listParsLinks = self.ParsingLinks()
        # print(listParsLinks)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.get_gather_data())
        
        finishTime = datetime.datetime.now() - startTime
        print(finishTime)


    async def get_page_data_links(self, session, page):
            
            url_pages = f"https://habr.com/ru/hub/popular_science/page{page}/"
            
            async with session.get(url=url_pages, headers=self.headers) as response:
                response_text = await response.text()
                
                soup = BeautifulSoup(response_text, "lxml")
                
                link_items = soup.find_all("a", class_="tm-article-snippet__title-link")
                for item in link_items:
                    self.list_links.append(item.get("href"))
    
            return self.list_links
    
    async def get_gather_data(self):
        async with aiohttp.ClientSession() as session:
            # response = await session.get(url=self.urlScience, headers=self.headers)
            # soup = BeautifulSoup(await response.text(), "lxml")
            # allLinksHref = soup.find_all("a", class_="tm-article-snippet__title-link")            
            tasks = []
            
            for page in range(1,3):
                # print(f"{page} ////////////////////")
                # task = asyncio.create_task(self.get_page_data_links(session, page))
                listLinks = await self.get_page_data_links(session, page)
                # tasks.append(task)
                await asyncio.sleep(0.03)
            
            print(len(listLinks))
            # await asyncio.gather(*tasks)         

    # def ParsingLinks(self):

    #     self.tempCounter = 0
    #     # header для того что бы сайт думал что мы не бот
    #     response = requests.get(self.urlScience, headers=self.headers)
    #     soup = BeautifulSoup(response.text, "lxml")
    #     allLinksHref = soup.find_all("a", class_="tm-article-snippet__title-link")
        
    #     # parsing links of posts on first page
    #     for item in allLinksHref:
    #         self.listLinks.append(self.urlAll[:-1] + item.get("href"))
    #         # self.tempCounter += 1
            
    #     return self.listLinks      
        
       
    # def ParsingTitles(self, listLinks):
    #     # print(listLinks)
    #     for item in listLinks:
    #         response = requests.get(item, headers=AbsParser.headers)
    #         soup = BeautifulSoup(response.text, "lxml")
    #         postTitle = soup.find("h1", class_="tm-article-snippet__title tm-article-snippet__title_h1").find("span").text
            
    #     print("ok")
        
    #     return postTitle