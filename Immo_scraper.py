# -*- coding: utf-8 -*-

#AUTHOR: Tommaso Ficara
"""
Created on Tue March 7 2019 17:10:36
"""

import requests 
import os
from bs4 import BeautifulSoup
import math
import re 
import pandas as pd
import datetime


os.chdir('') #Insert Directory


# Choose parameters for research

Max_miete=1000 #max rent
Min_flaeche=0 # Min size

# Choose distict from following list and appened them to 'districts' list:

Prenzlauer_Berg='pankow/prenzlauer-berg'
Mitte='mitte-mitte'
Kreuzberg='kreuzberg-kreuzberg'
Schöneberg='schoeneberg-schoeneberg'
Neukölln='neukoelln-neukoelln'
Charlottenburg='charlottenburg-charlottenburg'


districts=[Mitte]


dn= datetime.datetime.now();

s = requests.Session()

def crawlURL(url_path):
    attempts=0
    pageContent=''
    global s
    while attempts<5:
        try:
            pageContent = s.get(url_path).text
            attempts = 10 # dummy break condition
        except:
            attempts+=1;    
            print('crawl error URL')
            #ErrorFile.write(str(url_path)+"\n")
    return pageContent



dict_list=[]
for i in range(len(districts)):
    dist_url=(''.format(districts[i])) #Insert actual link 
    response=requests.get(dist_url)
    
    #print(response)
    #print(type(response))
    
    
    pagecontent=crawlURL(dist_url)
    
    #print(pagecontent)
    soup = BeautifulSoup(pagecontent,'html.parser')
    soupString = str(soup)
    
    total_results=soup.find('span', {'class': "font-normal no-of-results-highlighter"}).text;print('Current number of ads for {}: '.format(str(districts[i]).split('-')[0]) + total_results)
    total_results=int(total_results)
    
    
    
    last_page=math.ceil(total_results/20)+1;#print(last_page)
    
    #print('last page is: {}'.format(last_page))
    
    page=1
    page_ads=[]
    list=[]
    for link in range(last_page):
        landing_page=str(dist_url)+'?pagenumber='+str(page)
        list.append(landing_page)
        pagecontentiterate=crawlURL(landing_page)
        soupiterate=BeautifulSoup(pagecontentiterate, 'html.parser')
        soupiteratestring=str(soupiterate)
        id=re.findall(r'data-result-id="(.*?)"', soupiteratestring)
        
        for i in range(len(id)):
            ad_link=''.format(id[i])
            page_ads.append(ad_link)
        page+=1
    page_ads=page_ads[0:total_results]
    print('Successfully crawled ads: {}'.format(len(page_ads)))
    x=0
    
    for ad in page_ads:
        adcontent=crawlURL(ad)
        soupad=BeautifulSoup(adcontent, 'html.parser')
        soupadstring=str(soupad)
        '''
        if soupad.find('dd', {'class': 'is24qa-gesamtmiete grid-item three-fifths font-bold'}).text.replace(' ','').replace('+','').replace('€','').replace(',','.').replace('(zzgl.Heizkosten)','').replace('(zzgl.Nebenkosten)',''     )[-3]=='.':
            treshold=float(str(soupad.find('dd', {'class': 'is24qa-gesamtmiete grid-item three-fifths font-bold'}).text.replace(' ','').replace('+','').replace('€','').replace(',','.').replace('(zzgl.Heizkosten)','').replace('(zzgl.Nebenkosten)',''     )[0:-3].replace('.','')))
        else: 
            treshold= float(soupad.find('dd', {'class': 'is24qa-gesamtmiete grid-item three-fifths font-bold'}).text.replace(' ','').replace('+','').replace('€','').replace(',','.').replace('(zzgl.Heizkosten)','').replace('(zzgl.Nebenkosten)',''     ))
        if treshold > Max_miete:'''
            
        attributes={}
        attributes['URL']=ad
        
        attributes['Crawl date']='%02d%02d%02d'%(dn.year,dn.month,dn.day)
        try:
            attributes['Adresse']=soupad.find('span', {'data-qa': 'is24-expose-address'}).text
        except:
            attributes['Adresse']=''
        try:    
            attributes['Bezirk']=re.findall(r'\((.*?)\)',str(soupad.find('span', {'data-qa': 'is24-expose-address'}).text))[0] 
        except:
            attributes['Bezirk']='' 
    
        try:
            attributes['Fläche m²']=soupad.find('div', {'class': 'is24qa-flaeche is24-value font-semibold'}).text.replace(' ','').replace('m²','').replace(',','.')
            attributes['Fläche m²']=float(attributes['Fläche m²'])
        except:
            attributes['Fläche m²']=''
        attributes['Gesamtmiete']=soupad.find('dd', {'class': 'is24qa-gesamtmiete grid-item three-fifths font-bold'}).text
        
        if 'Heizkosten' in attributes['Gesamtmiete']:
                attributes['Extra Heizkosten']=1
        else:
                attributes['Extra Heizkosten']=0
                
        try:
            attributes['Gesamtmiete']=soupad.find('dd', {'class': 'is24qa-gesamtmiete grid-item three-fifths font-bold'}).text.replace(' ','').replace('+','').replace('€','').replace(',','.').replace('(zzgl.Heizkosten)','').replace('(zzgl.Nebenkosten)',''     )
            if attributes['Gesamtmiete'][1]=='.':
                    attributes['Gesamtmiete']=attributes['Gesamtmiete'].replace('.','',1)
                    attributes['Gesamtmiete']=float(attributes['Gesamtmiete'])
            else:
                    attributes['Gesamtmiete']=attributes['Gesamtmiete']
                    attributes['Gesamtmiete']=float(attributes['Gesamtmiete'])
        except:
            attributes['Gesamtmiete']=0
        
        
        try:
            attributes['Kaltmiete']=soupad.find('div', {'class': 'is24qa-kaltmiete is24-value font-semibold is24-preis-value'}).text.replace(' ','').replace('+','').replace('€','').replace(',','.');
            if attributes['Kaltmiete'][1]=='.':
                    attributes['Kaltmiete']=attributes['Kaltmiete'].replace('.','',1)
                    attributes['Kaltmiete']=float(attributes['Kaltmiete'])
                
            else:
                    attributes['Kaltmiete']=(attributes['Kaltmiete'])
                    attributes['Kaltmiete']=float(attributes['Kaltmiete'])
        except:
            attributes['Kaltmiete']=''
        if attributes['Kaltmiete']=='':
            attributes['Kaltmiete']=0
        try:
            attributes['Kaltmiete/m²']=round((attributes['Kaltmiete']/attributes['Fläche m²']),2)
    
        except:
            attributes['Kaltmiete/m²']=''
        try:
            attributes['Nebenkosten']=soupad.find('dd', {'class': 'is24qa-nebenkosten grid-item three-fifths'}).text.replace(' ','').replace('+','').replace('€','').replace(',',('.'))
            '''if attributes['Nebenkosten'][len(attributes['Nebenkosten'])-3]==',':
                    attributes['Nebenkosten']=attributes['Nebenkosten'][0:-3]
            else:
                attributes['Nebenkosten']=attributes['Nebenkosten']     
            '''    
            attributes['Nebenkosten']=float(attributes['Nebenkosten'])
        except:
            attributes['Nebenkosten']=0
         
        if -10 < attributes['Gesamtmiete']-attributes['Nebenkosten']-attributes['Kaltmiete'] < 10:
            attributes['Heizkosten']=0
        else:
            attributes['Heizkosten']=attributes['Gesamtmiete']-attributes['Nebenkosten']-attributes['Kaltmiete'];
       
        try: 
            attributes['Heizkosten inkludiert?']=soupad.find('dd', {'class': 'is24qa-heizkosten grid-item three-fifths'}).text.replace(' ','').replace('+','').replace('€','').replace(',',('.'))
            #attributes['Heizkosten']=float(attributes['Heizkosten'])
        except:
            attributes['Heizkosten']='' 
        
        try:
            attributes['Zimmer']=soupad.find('div', {'class': 'is24qa-zi is24-value font-semibold'}).text.replace(' ','').replace(',','.');attributes['Zimmer']=float(attributes['Zimmer'])
        except:
            attributes['Zimmer']=''
        #PRINT TYPE KEY print(type(attributes['']))
        
        # TAGS
        try:
            attributes['Balkon/Terrasse']=soupad.find('span', {'class': 'is24qa-balkon-terrasse-label palm-hide'}).text;
            attributes['Balkon/Terrasse']=1
        except:
            attributes['Balkon/Terrasse']=0
        try:
            attributes['Keller']=soupad.find('span', {'class': 'is24qa-keller-label palm-hide'}).text;
            attributes['Keller']=1
        except:
            attributes['Keller']=0
       
        try:
            attributes['Personenaufzug']=soupad.find('span', {'class': 'is24qa-personenaufzug-label lap-hide desk-hide'}).text;
            attributes['Personenaufzug']=1
        except:
            attributes['Personenaufzug']=0
                 
        try:
            attributes['Einbauküche']=soupad.find('span', {'class': 'is24qa-einbaukueche-label palm-hide'}).text;
            attributes['Einbauküche']=1
        except:
            attributes['Einbauküche']=0
        try:
            attributes['Garten/ -mitbenutzung']=soupad.find('span', {'class': 'is24qa-garten-mitbenutzung-label palm-hide'}).text;
            attributes['Garten/ -mitbenutzung']=1
        except:
            attributes['Garten/ -mitbenutzung']=0
        try:
            attributes['Gäste WC']=soupad.find('span', {'class': 'is24qa-gaeste-wc-label lap-hide desk-hide'}).text;
            attributes['Gäste WC']=1
        except:
            attributes['Gäste WC']=0
        try:
            attributes['Stufenloser Zugang']=soupad.find('span', {'class': 'is24qa-stufenloser-zugang-label lap-hide desk-hide'}).text;
            attributes['Stufenloser Zugang']=1
        except:
            attributes['Stufenloser Zugang']=0
        try:    
            attributes['Schlafzimmer']=soupad.find('dd', {'class': 'is24qa-schlafzimmer grid-item three-fifths'}).text;    
            attributes['Schlafzimmer']=float(attributes['Schlafzimmer'])
        except:
            attributes['Schlafzimmer']=''
        try:    
            attributes['Badezimmer']=soupad.find('dd', {'class': 'is24qa-badezimmer grid-item three-fifths'}).text;
            attributes['Badezimmer']=float(attributes['Badezimmer'])
            
        except:
            attributes['Badezimmer']=''    
            
        try:    
            attributes['Baujahr']=soupad.find('dd', {'class': 'is24qa-baujahr grid-item three-fifths'}).text;    
        except:
            attributes['Baujahr']=''
        
        try:    
            attributes['Sanierung']=soupad.find('dd', {'class': 'is24qa-modernisierung-sanierung grid-item three-fifths'}).text;    
        except:
            attributes['Sanierung']=''    
        try:    
            attributes['Objektzustand']=soupad.find('dd', {'class': 'is24qa-objektzustand grid-item three-fifths'}).text;    
        except:
            attributes['Objektzustand']=''
        try:    
            attributes['Ausstattung']=soupad.find('dd', {'class': 'is24qa-qualitaet-der-ausstattung grid-item three-fifths'}).text;    
        except:
            attributes['Ausstattung']=''       
        try:    
            attributes['Heizungsart']=soupad.find('dd', {'class': 'is24qa-heizungsart grid-item three-fifths'}).text;    
        except:
            attributes['Heizungsart']=''
        try:    
            attributes['Wesentliche Energiträger']=soupad.find('dd', {'class': 'is24qa-wesentliche-energietraeger grid-item three-fifths'}).text;    
        except:
            attributes['Wesentliche Energiträger']=''
        try:    
            attributes['Energieausweis']=soupad.find('dd', {'class': 'is24qa-energieausweis grid-item three-fifths'}).text;    
        except:
            attributes['Energieausweis']=''    
        try:    
            attributes['Energieausweistyp']=soupad.find('dd', {'class': 'is24qa-energieausweistyp grid-item three-fifths'}).text;    
        except:
            attributes['Energieausweistyp']=''    
        try:    
            attributes['Endenergiebedarf']=soupad.find('dd', {'class': 'is24qa-endenergiebedarf grid-item three-fifths'}).text;    
        except:
            attributes['Endenergiebedarf']=''    
        try:    
            attributes['Energieeffizienzklasse']=soupad.find('dd', {'class': 'is24qa-energieeffizienzklasse grid-item three-fifths'}).text;    
        except:
            attributes['Energieeffizienzklasse']=''    
               
        
    #x+=round(attributes['Kaltmiete']/len(page_ads),2)    
        dict_list.append(attributes)
dataset=pd.DataFrame(dict_list)
#dataset_sorted=dataset.sort_values(by='Kaltmiete/m²')

dataset_filter=dataset[(dataset['Gesamtmiete']<Max_miete) & dataset['Gesamtmiete']!=0]
dataset_filter=dataset_filter[dataset_filter['Fläche m²']>Min_flaeche]

dataset.to_csv('%02d%02d%02d_scrapeCSV.csv'%(dn.year,dn.month,dn.day))
dataset.to_excel('%02d%02d%02d_scrape.xlsx'%(dn.year,dn.month,dn.day))
dataset_filter.to_excel(('%02d%02d%02d_scrape_filtered.xlsx'%(dn.year,dn.month,dn.day)))
#dataset.to_csv('scrape1.xlsx')

#Plotting the data


dataset.plot(y='Gesamtmiete', x='Fläche m²', kind='scatter')




