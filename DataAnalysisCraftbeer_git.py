# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 18:14:58 2022

@author: tommasoficara
"""


import os
import re
import pandas as pd
import datetime
import pyperclip
import numpy as np
import matplotlib.pyplot as plt
import random


data=pd.read_csv("20220412_craftbeershop.csv")
data_country=pd.read_csv("Country_list.csv")


#### Merge Country Data
data_country=data_country.rename(columns={"Brand":"Hersteller"})
data_country=data_country.drop(axis=1, columns=["Unnamed: 0"])
data=pd.merge(data, data_country, on="Hersteller")

# Removing remaining Non-Product Pages

data=data.dropna(subset=['Hersteller'])

########### Transforming and Cleaning Columns ############

inhalt=[]
for i in range(len(data.Inhalt)):
    if data.Inhalt[i]==None:
        content=np.nan
        inhalt.append(float(content))
    elif len(str(data.Inhalt[i]))>=9:
        content=np.nan
        inhalt.append(content)
    else:
        content=str(data.Inhalt[i]).split()[0]
        if "l" in str(data.Inhalt[i]).split():
            pass
        elif "cl" in str(data.Inhalt[i]).split():
            content=content*100
        elif "ml" in str(data.Inhalt[i]).split():
            content=content*1000
        try:
            content=content.replace(",",".")
        except:
            pass
        inhalt.append(float(content))    


inhalt=pd.Series((inhalt))
data=data.drop(columns=['Inhalt'])
data["Inhalt"]=inhalt
data["PreisLiter"]=Preis_Liter=data.Vollpreis/(data.Inhalt)


bewertung=[]
for i in range(len(data.Bewertung)):
    bewertung.append(float(data.Bewertung[i].split("/")[0]))
bewertung=pd.Series((bewertung))
data=data.drop(columns=['Bewertung'])
data["Bewertung"]=bewertung
round(data.groupby("Hersteller").Bewertung.mean(),2)


aroma=[]
supplier=[]
product=[]

for i in range(len(data.Aroma)):
    if "ttp" in str(data.Aroma[i]):
        aroma.append("nan")
        supplier.append(data.Hersteller[i])
        product.append(data.Produkt[i])
    else:
        try:
            content=re.findall(r'\'(.*?)\'', str((data.Aroma[i]).split(",")))
            for contents in content:
                aroma.append(str(contents.replace(".","").strip()))
                supplier.append(data.Hersteller[i])
                product.append(data.Produkt[i])
                
        except:
            aroma.append("nan")
            supplier.append(data.Hersteller[i])
            product.append(data.Produkt[i])
        

aroma_data=pd.DataFrame({"Supplier":supplier, "Product":product, "Aroma":aroma})
aroma_ranking=pd.DataFrame(aroma_data.Aroma.value_counts())

l=list(aroma_ranking.index)
aroma_ranking=pd.DataFrame({"Type":l,"Count":aroma_ranking["Aroma"]})
aroma_ranking=aroma_ranking.reset_index(drop=True)
aroma_ranking.drop(aroma_ranking[aroma_ranking.Type == "nan"].index, inplace=True)
aroma_ranking=aroma_ranking.sort_values("Count", ascending=False)


hopfen=[]
supplier=[]
product=[]

for i in range(len(data.Hopfen)):
    if "ttp" in str(data.Hopfen[i]):
        aroma.append("nan")
        supplier.append(data.Hersteller[i])
        product.append(data.Produkt[i])
    else:
        try:
            content=re.findall(r'\'(.*?)\'', str((data.Hopfen[i]).split(",")))
            for contents in content:
                hopfen.append(str(contents.replace(".","").strip()))
                supplier.append(data.Hersteller[i])
                product.append(data.Produkt[i])
                
        except:
            hopfen.append("nan")
            supplier.append(data.Hersteller[i])
            product.append(data.Produkt[i])

        
##### Create new dataframe for Hopfen

hopfen_data=pd.DataFrame({"Supplier":supplier, "Product":product, "hopfen":hopfen})
hopfen_ranking=pd.DataFrame(hopfen_data.hopfen.value_counts())

l=list(hopfen_ranking.index)
hopfen_ranking=pd.DataFrame({"Type":l,"Count":hopfen_ranking["hopfen"]})
hopfen_ranking=hopfen_ranking.reset_index(drop=True)
hopfen_ranking.drop(hopfen_ranking[hopfen_ranking.Type == "nan"].index, inplace=True)
hopfen_ranking=hopfen_ranking.sort_values("Count", ascending=False)

#Creating new dataframe with distrinct Supplier names

Hersteller_data=pd.DataFrame(data.groupby("Hersteller").Hersteller.count())
Hersteller_data2=pd.DataFrame(data.groupby("Hersteller").PreisLiter.mean().round(2))
Hersteller_data3=pd.DataFrame(round(data.groupby("Hersteller").Bewertung.mean(),2))

# Joining datasets

Hersteller_data=Hersteller_data.join(Hersteller_data2)
Hersteller_data=Hersteller_data.join(Hersteller_data3)
Hersteller_data=Hersteller_data.rename(columns={"Hersteller":"Sortimentbreite"})



############## P L O T S ############# 


plt.figure()
plt.title("Verteilung PreisLiter")
mean=Hersteller_data.PreisLiter.mean()
median=Hersteller_data.PreisLiter.median()
Hersteller_data.PreisLiter.plot.kde(xlim=[-10,25])
plt.axvline(mean, color="red", label="Durchschnittswert")
plt.axvline(median, color="green", label="Median")
plt.legend()

plt.figure()
plt.title("Verteilung Sortimentbreite")
mean=Hersteller_data.Sortimentbreite.mean()
median=Hersteller_data.Sortimentbreite.median()
Hersteller_data.Sortimentbreite.plot.kde(xlim=[-10,25])
plt.axvline(mean, color="red", label="Durchschnittswert")
plt.axvline(median, color="green", label="Median")
plt.legend()


plt.figure()
plt.title("Verteilung Bewertung")
mean=Hersteller_data.Bewertung.mean()
median=Hersteller_data.Bewertung.median()
Hersteller_data.Bewertung.plot.kde()
plt.axvline(mean, color="red", label="Durchschnittswert")
plt.axvline(median, color="green", label="Median")
plt.legend()

############ Generate Random Colors for Histogram

colors=[]
for j in range(50):
    rand_colors = ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
    colors.append(rand_colors[0])


plt.figure()
plt.title("Top 20 Aromas")
plt.bar(aroma_ranking.Type[0:20], aroma_ranking.Count[0:20], width=0.5, color=colors)
plt.xticks(rotation=90)
number=random.randint(1,9)


############ Plotting Histogram with Top 20 Hopfen

plt.figure()
plt.title("Top 20 Hopfen")
plt.bar(hopfen_ranking.Type[0:20], hopfen_ranking.Count[0:20], width=0.5, color=colors[0:20])
plt.xticks(rotation=90)
number=random.randint(1,9)

############
