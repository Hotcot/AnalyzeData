import os
from Parser.WorldParser import WorldParser
from Parser.ScienceParser import ScienceParser
from Parser.BusinessParser import BusinessParser
from Parser.SportParser import SportParser

from CNN.NeyronNetwork import NeyronNetwork

# # clear file with data for classification
# file_clear = open("current.csv", "w")
# file_clear.truncate()
# file_clear.close()

# #data for classification
# parserWorld = WorldParser()
# print("WorldParser =============================")
# parserSport = SportParser()
# print("SportParser ============================")
# parserBusiness = BusinessParser()
# print("BusinessParser ============================")
# parserScience = ScienceParser()
# print("ScienceParser ============================")

# if(os.stat("current.csv").st_size == 0):
#     print("True")
# else:
#     print("It's a joke")




#initialize neyron network CNN
neyronNetwork = NeyronNetwork()