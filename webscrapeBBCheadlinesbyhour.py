import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime as dt
#from apscheduler import BackgroundScheduler

def news():
    df=pd.DataFrame(columns=["Date","News links"])
    website=requests.get("https://www.bbc.com")
    scrape=website.content

    soup=BeautifulSoup(scrape,"lxml")

    links=[]
    link_tag=soup.find_all("h3",{"class":"media__title"})

    for item in link_tag:
        tags=item.find("a")
        if "news" and "world" in (tags.attrs["href"]):
            links.append("https://www.bbc.com"+tags.attrs["href"])
        else:
            continue
    print(links)

    for i in links:
        df=df.append({"Date":dt(dt.now().year,dt.now().month,dt.now().day,dt.now().hour, dt.now().minute), "News links":i},ignore_index=True)

    def get_filename_datetime():
        return "BBC_links_date_" + str((dt.now().year,dt.now().month,dt.now().day)) + "_hour_" + str(dt.now().hour) + ".csv"

    df.to_csv(get_filename_datetime())

news()

print("News headline scrapped")
    #for tag in link_tag:
    #    links.append(link_tag.attrs["href"])
    #
    #for i in links:
    #    print(i)
    #    print('\n')
