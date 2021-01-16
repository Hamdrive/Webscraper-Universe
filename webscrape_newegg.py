#!/usr/bin/env python
# -*- coding: utf-8 -*-
#video link="https://www.youtube.com/watch?v=XQgXKtPSzUI"
#how to properly show rupee sign in excel: https://stackoverflow.com/questions/6002256/is-it-possible-to-force-excel-recognize-utf-8-csv-files-automatically/6488070#6488070
#if fresh install of python, pip3 install: bs4, pandas, requests, openpyxl, numpy==1.19.3(most stable version at the time of writing this comment(17/12/20))

from bs4 import BeautifulSoup as soup #to parse HTML
import pandas as pd
import requests

df=pd.DataFrame(columns=["Company", "Product", "Cost", "Link to purchase"])

my_url = "https://www.newegg.com/global/in-en/Processors-Desktops/SubCategory/ID-343/"
all_cpus=[]

def get_page_number(page_soup):
    no_of_pages = page_soup.find('div', class_='list-tool-pagination').find('strong').text.split('/')[1]
    return(no_of_pages)

def scrape_page(number=1):

    global df

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'User-Agent': user_agent}

    #opening website url and downloading page
    page_html = requests.get(my_url+"/Page-"+str(number), headers=headers)#, proxies = {"https": "http://193.117.138.126"})

    page_content = page_html.text #instead of content used text because it has UTF-8 encoding so rupee symbol will be properly parsed.
    #to parse HTML
    page_soup = soup(page_content,"html.parser")
    #print(page_soup.h2)
    #COMMENTED FOR TEMP print(page_soup)
    #grabs gcard data
    all_cpus = page_soup.find_all("div",{"class":"item-container"})
    brand = page_soup.find_all("div",{"class":"item-info"})
    money = page_soup.find_all("li",{"class":"price-current"})
    #cost = ''.join(money.text.split()[0:2])
    #print(''.join(cost.text.split()[0:2]))
    #g_card = all_gcards[0]
    #b=brand[0]
    #print(all_gcards)
    # print(g_card.a.img["title"])
    # print(b.div.a.img["title"])
    for info, b, m in zip(all_cpus, brand, money):

        company = b.div.a.img["title"]
        product = info.a.img["title"]
        cost = ''.join(m.text.split()[0:2])
        link = info.a["href"]

        print("Company: ", company)
        print("Product: ", product)
        print("Cost: ", cost)
        print("Link: ", link)
        print("\n")

        df=df.append({"Company": company, "Product": product, "Cost": cost, "Link to purchase": link}, ignore_index=True)

    return get_page_number(page_soup)
    #print(len(all_cpus))

page_number = scrape_page()

if int(page_number) > 1:
    for i in range (1, int(page_number)):
        scrape_page(i+1)

df.reset_index()
df.to_excel(r'E:\MyPrograms\proj6-webscraping\CPU_list_NewEgg.xlsx', index = True)
df.to_csv("CPU_list_NewEgg.csv")
print("Saved in excel")

# for b in brand:
#     company = b.div.a.img["title"]
#
# print(product)
# print(link)
# print(company)
