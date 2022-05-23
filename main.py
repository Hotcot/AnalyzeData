from Parser.WorldParser import WorldParser
from Parser.ScienceParser import ScienceParser
from Parser.BusinessParser import BusinessParser


#pars data for train CNN
parserScience = WorldParser()
print("WorldParser =============================")
parserSport= ScienceParser()
print("ScienceParser ============================")
parserBusiness = BusinessParser()
print("BusinessParser ============================")
