# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 18:19:01 2022

@author: tommasoficara
"""

## This script creates a DataFrame used in the main Data Analysis Script to associate Brands with their corresponding Country of Origin

import os
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import datetime
import pandas as pd

crawl=1
write=1

s = requests.Session()

def crawlURL(url_path):
    attempts=0
    #time.sleep(random.randint(0.0001, 0.001))
    pageContent=''
    global s
    while attempts<5:
        #print(requests.get(url_path))
        try:
            pageContent = s.get(url_path).text
            attempts = 10 # dummy break condition
        except:
            attempts+=1;    
            print('crawl error URL')
            
            #ErrorFile.write(str(url_path)+"\n")
    return pageContent
     
if crawl==1:
    content=crawlURL('https://www.craftbeer-shop.com/laender')
    soup=BeautifulSoup(content, 'html.parser')
    soupstring=str(soup)

countries=re.findall(r'<a class="subcategory-card__title" href="(.*?)">', content)

country_page=[]
for country in countries:     
    content=crawlURL('https://www.craftbeer-shop.com/'+country)
    soup=BeautifulSoup(content, 'html.parser')
    soupstring=str(soup)
    string=(str(soup.find('ul',{"class":"dropdown-menu"})))
    brandlist=re.findall(r'</i>\n                        (.*?)\n                    </span>', string)
    for brand in brandlist:
        country_dict={}
        country_dict["Brand"]=brand
        country_dict['Land']=country.capitalize()
        country_page.append(country_dict)
        
if write==1:
    country_data=pd.DataFrame(country_page)
    dn= datetime.datetime.now()
    country_data.to_csv('Country_list.csv')           
        
   
    
    

