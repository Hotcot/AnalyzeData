import os
from Parser.WorldParser import WorldParser
from Parser.ScienceParser import ScienceParser
from Parser.BusinessParser import BusinessParser
from Parser.SportParser import SportParser

from CNN.NeyronNetwork import NeyronNetwork
from SendBot.TelBot import TelBot

# # clear file with data for classification
file_clear = open("current.csv", "w")
file_clear.truncate()
file_clear.close()
print("Clear file for classification")

# #data for classification
parserWorld = WorldParser()
print("End parsing WorldParser")
parserSport = SportParser()
print("End parsing SportParser")
parserBusiness = BusinessParser()
print("End parsing BusinessParser")
parserScience = ScienceParser()
print("End parsing ScienceParser")

if(os.stat("current.csv").st_size == 0):
    print("No data for classification")
else:
    # initialize neyron network CNN
    neyronNetwork = NeyronNetwork()
    current_data, result_theme = neyronNetwork.get_data()
    # telBot = TelBot(current_data, result_theme)


