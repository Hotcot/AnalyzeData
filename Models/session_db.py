from sqlalchemy.orm import sessionmaker
from .alchemy_decl import engine
from .alchemy_decl import Article

session = sessionmaker(bind=engine)

session = session()