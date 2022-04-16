# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 18:24:21 2021

@author: Tommaso
"""

import os
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import datetime
import pyperclip
 

write=2
crawl=2

website='craftbeershop'

os.chdir("C:/Users/tomma/Desktop/craftbeer")

url_data=pd.read_csv('Craftbeershop_sitemap.csv')

url_list=url_data.iloc[:,0]

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
    l=[]
    for url in url_list:
        print(url)
        content=crawlURL(url)
        soup=BeautifulSoup(content, 'html.parser')
        soupstring=str(soup)
        contents={}
        try:
            contents['title']=soup.find('h1', {'class':'fn product-title'}).text
            contents['URL']=url
            contents['soupstring']=soupstring   
            contents['soup']=soup
            l.append(contents)   
            dataset=pd.DataFrame(l)
            dn= datetime.datetime.now()
            dataset.to_csv('contents_{}.csv'.format(website))
        except:
            print("failure")
            pass
   
content_data=pd.read_csv('contents_Craftbeershop.csv')

dict_list=[]  

for i in range(len(content_data))[0:100]:     
    attributes={}
    attributes['URL']=content_data['URL'][i]
    soup=BeautifulSoup(content_data['soup'][i], 'html.parser')
    soupstring=content_data['soupstring'][i]
    
    try:
        attributes['Produkt']=soup.find('h1', {'class':'fn product-title'}).text
    except:
        attributes['Produkt']=''
    try: 
        attributes['Artikel nr.']=soup.find('td', {'itemprop':'sku'}).text
    except:
        attributes['Artikel nr.']=''
    try: 
        attributes['Hersteller']=soup.find('td', {'itemprop':'manufacturer'}).text
    except:
        attributes['Hersteller']=''
    try: 
        attributes['Inhalt']=re.findall(r'Inhalt‍: </td>\n<td class=\"attr-value\">(.*?)</td>',soupstring)[0] 
    except:
        attributes['Inhalt']='' 
    try:
        attributes['Vollpreis']=soup.find('meta', {'id':'itemprop-price'}).get('content')
    except:
        attributes['Vollpreis']=''
    try:
        attributes['zzgl. Pfand']=soup.find('div', {'class':'pfand-info'}).text.replace('\n','').replace('zzgl. Pfand ','').replace('€','')
    except:
        attributes['zzgl. Pfand']=''    
    try:
        attributes['Beschreibung']=soup.find('div', {'class':'desc'}).text.replace('\n','').replace('\t','').strip()
    except:
        attributes['Beschreibung']=''    
    try:
        attributes['Bewertung']=soup.find('span', {'class':'rating'}).get('title').split()[-1]
    except:
        attributes['Bewertung']='' 
    try:
        attributes['Anzahl Bewertungen']=soup.find('span', {'style':'margin-left:2em'}).text
    except:
        attributes["Anzahl Bewertungen"]=""     
    try: 
        attributes['Versandgewicht']=soup.find('td', {'class':'attr-value weight-unit'}).text
    except:
        attributes['Versandgewicht']=''
    try: 
        attributes['Herkunft']=re.findall(r'Herkunft: \n        </td>\n<td class="attr-value">\n            (.*?)\n        </td>',soupstring)[0] 
    except:
        attributes['Herkunft']=''
    try: 
        attributes['Zutaten']=re.findall(r'Zutaten: \n        </td>\n<td class="attr-value">\n            (.*?)\n        </td>',soupstring).replace('<strong>','')[0] 
    except:
        attributes['Zutaten']=''
    try: 
        attributes['Alkoholgehalt']=float(re.findall(r'href="(.*?)-vol">',soupstring)[0])/10
    except:
        attributes['Alkoholgehalt']=''
    try: 
        attributes['Genusstemperatur']=float(re.findall(r'href="(.*?)-Celsius"',soupstring)[0])
    except:
        attributes['Genusstemperatur']=''
    try:
        retext=re.findall(r'Hopfen‍:(.*?)</tr>',soupstring, re.DOTALL)[0]
        attributes['Hopfen']=''
        Hopfen=re.findall(r'href="(.*?)"', retext)
        for i in range(len(Hopfen)):
            attributes['Hopfen']+=Hopfen[i].capitalize()
            if i!=len(Hopfen)-1:
                
                attributes['Hopfen']+=', '
            else:
                attributes['Hopfen']+='.'
    except:
        attributes['Hopfen']=''  
    try:
        retext=re.findall(r'Malz‍:(.*?)</tr>',soupstring, re.DOTALL)[0]
        attributes['Malz']=''
        Malz=re.findall(r'href="(.*?)"', retext)
        for i in range(len(Malz)):
            attributes['Malz']+=Malz[i].capitalize()
            if i!=len(Malz)-1:
                
                attributes['Malz']+=', '
            else:
                attributes['Malz']+='.'
    except:
        attributes['Malz']='' 
        
    try:
        retext=re.findall(r'Hefe‍:(.*?)</tr>',soupstring, re.DOTALL)[0]
        attributes['Hefe']=''
        Hefe=re.findall(r'href="(.*?)"', retext)
        for i in range(len(Hefe)):
            attributes['Hefe']+=Hefe[i].capitalize()
            if i!=len(Hefe)-1:      
                attributes['Hefe']+=', '
            else:
                attributes['Hefe']+='.'  
    except:
        attributes['Hefe']=''                   
    
    try:
        retext=re.findall(r'Bittereinheiten‍:(.*?)</tr>',soupstring, re.DOTALL)[0]
        attributes['Bittereinheiten‍']=''
        a=re.findall(r'href="(.*?)"', retext)
        for i in range(len(a)):
            attributes['Bittereinheiten‍']+=a[i].capitalize()
            if i!=len(a)-1:      
                attributes['Bittereinheiten‍']+=', '
            else:
                attributes['Bittereinheiten‍']+='.'  
    except:
        attributes['Bittereinheiten‍']=''                   
        
    
    try:
        retext=re.findall(r'Aroma(.*?)<td class="attr-label word-break">',soupstring, re.DOTALL)[0]
        attributes['Aroma']=''
        Aroma=re.findall(r'a href="(.*?)"class="label label-primary"', retext)
        for i in range(len(Aroma)):
            attributes['Aroma']+=Aroma[i].capitalize()
            if i!=len(Aroma)-1:      
                attributes['Aroma']+=', '
            else:
                attributes['Aroma']+='.'  
   
    except:
        attributes['Aroma']=''                   
    
    try: 
        attributes['Genusstemperatur']=re.findall(r'href="(.*?)-Celsius"',soupstring)[0]
    except:
        attributes['Genusstemperatur']=''    
    try: 
        attributes['Haltbar bis']=re.findall(r'<span>Haltbar bis:(.*?)</span>', soupstring)[0].strip()
    except:
        attributes['Haltbar bis']=''       
        #get aroma
    
    
    dict_list.append(attributes)

     
if write==1:
    dataset=pd.DataFrame(dict_list)
    dn= datetime.datetime.now()
    dataset.to_csv('%02d%02d%02d_{}.csv'.format(website)%(dn.year,dn.month,dn.day))   
    dataset.to_excel('%02d%02d%02d_{}.xlsx'.format(website)%(dn.year,dn.month,dn.day))   
        

    