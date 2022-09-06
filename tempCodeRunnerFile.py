from multiprocessing.sharedctypes import Value
import requests
import pandas as pd
import json
import re
from pprint import pprint
from csv import writer
import sqlalchemy

# GETTING TOTAL PAGINATION
url = 'https://www.edgeprop.my/jwdsonic/api/v1/property/search?=&listing_type=sale&state=Kelantan&property_type=rl&start=0&size=20'
data = requests.get(url).json()

total_pages = int(data["found"]/20)
print(total_pages)

# DATA VARIABLES
property_Title = []
property_District = []
property_State = []
property_Price = []
property_Sqft = []
property_Bedroom = []
property_Bathroom = []
property_Image = []
property_Origin_URL = []

df_edge = pd.DataFrame({'property_Title': property_Title, 'property_District': property_District,
                        'property_State': property_State, 'property_Price': property_Price, 'property_Sqft': property_Sqft,
                        'property_Bedroom': property_Bedroom, 'property_Bathroom': property_Bathroom,
                        'property_Image': property_Image, 'property_Origin_URL': property_Origin_URL})

df_edge.to_excel('edgeprop_property_listing.xlsx', index=False)

# MYSQL
engine = sqlalchemy.create_engine(
    'mysql://root:''@localhost:3307/asmaraloka')
df_edge.to_sql('scrape_property', engine, if_exists='replace')