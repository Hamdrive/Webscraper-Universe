import requests
from bs4 import BeautifulSoup as soup
import time
import pandas as pd

df1 = pd.DataFrame(columns=["Title","Author","Chapters","Link to novel"])



def get_link(number=1):
    page_link = "http://novelfull.com/index.php/completed-novel?page=" + str(number)
    get_html = requests.get(page_link)
    content = get_html.content

    get_soup = soup(content,"html.parser")

    site = get_soup

    print("Page successful: ", number)
    #print(get_soup)

    return scrape_content(site)

def scrape_content(site):

    global df1

    for novel, author, chapter in zip(site.find_all("h3"),site.find_all(class_="author"), site.find_all("div",{"class":"col-xs-2 text-info"})):
        novel_title = novel.text.strip()
        novel_link = "novelfull.com" + novel.a["href"]
        novel_author = author.text.strip()
        chapter_number = chapter.b.text.strip()

        print("Title: ", novel_title)
        print("Author: ", novel_author)
        print("Chapters: ", chapter_number)
        print("Link: ", novel_link)
        print("\n")

        df1=df1.append({"Title": novel_title, "Author": novel_author, "Chapters": chapter_number, "Link to novel": novel_link}, ignore_index=True)

        time.sleep(1)

    #     df1.append({"Title": novel_title, "Link to novel": novel_link}, ignore_index=True)
    #
    # for author in site.find_all(class_="author"):
    #     novel_author = author.text.strip()
    #
    #     df1.append({"Author": novel_author}, ignore_index=True)
    #
    # for chapter in site.find_all("div",{"class":"col-xs-2 text-info"}):
    #     chapter_number = chapter.b.text.strip()
    #
    #     df1.append({"Chapters": chapter_number}, ignore_index=True)

    #df.append({"Title": novel_title, "Author": novel_author, "Chapters": chapter_number, "Link to novel": novel_link}, ignore_index=True)

    return get_page_number(site)


def get_page_number(site):
        last_page = site.find(class_="last").a[str("href")]
        for s in last_page.strip():
            if s.isdigit() == True:
                pages = s


        return (pages)

page_count = get_link()


if (int(page_count)) > 1:
    for i in range (1, int(page_count)-1):
        get_link(i+1)
        time.sleep(1)



df1.to_csv("Complete_Novels.csv")
print("Scrape Complete!")
