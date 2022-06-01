from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import psycopg2 as psg2



engine = create_engine("postgresql+psycopg2://postgres:programa564742@localhost/postgres", echo=True)

print(engine)

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, unique = True, primary_key=True)
    link = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    date = Column(Date(), nullable=False)
    id_article = Column(String, nullable=False)
    send_bin = Column(Integer, nullable=False)
    
    
    def __init__(self, link, title, date, id_article, send_bin):
        self.link = link
        self.title = title
        self.date = date
        self.id_article = id_article
        self.send_bin = send_bin
        
class ClassificData(Base):
    __tablename__ = 'classific_data'
    
    id = Column(Integer, unique = True, primary_key=True)
    id_article = Column(String, nullable=False)
    link = Column(String(255), nullable=False)
    theme = Column(String, nullable=False)
    
    def __init__(self, id_article, link, theme):
        self.id_article = id_article
        self.link = link
        self.theme = theme
        
class LogData(Base):
    __tablename__ = 'log_data'
    
    id = Column(Integer, unique = True, primary_key=True)
    start_processing_time = Column(Date(), nullable=False)
    end_processing_time = Column(Date(), nullable=False)
    log_message = Column(String, nullable=False)
    
    def __init__(self, start_processing_time, end_processing_time, log_message):
        self.start_processing_time = start_processing_time
        self.end_processing_time = end_processing_time
        self.log_message = log_message

Base.metadata.create_all(engine)

    