import requests
from bs4 import BeautifulSoup, Comment
import selenium.webdriver as webdriver
import pandas as pd
import time  
import random


#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}        
#binary = 'c:/chromedriver/chromedriver.exe'
binary = 'D:\chromedriver/chromedriver.exe'
# 브라우져를 인스턴스화
browser = webdriver.Chrome(binary)
# 구글의 이미지 검색 url 받아옴(아무것도 안 쳤을때의 url)

index=1401
a=0

while True:
    browser.get('https://www.melon.com/genre/song_list.htm?gnrCode=GN0300#params%5BgnrCode%5D=GN0300&params%5BdtlGnrCode%5D=&params%5BorderBy%5D=POP&params%5BsteadyYn%5D=N&po=pageObj&startIndex='+str(index))
    randp=round(random.random()*3,2)
    time.sleep(3.5+randp)
    html = browser.page_source
    
    data=[]
    melon_parse= BeautifulSoup(html, 'html.parser')
        
    tbody=melon_parse.select('tbody > tr')
    print(len(tbody))
    
    
    for i in range(len(tbody)):
        data.append([])
        data[i].append(tbody[i].find_all("span",{"class": "rank"})[0].get_text())
        data[i].append(tbody[i].find_all("div",{"class": "ellipsis rank01"})[0].get_text()[1:-1])
        data[i].append((tbody[i].find_all("div",{"class": "ellipsis rank02"})[0].get_text()[1:-1]))
        data[i].append(tbody[i].find_all("div",{"class": "ellipsis rank03"})[0].get_text()[1:-1])
        data[i].append(tbody[i].find_all("span",{"class": "cnt"})[0].get_text()[5:])
        singid=tbody[i].find_all("a",{"class": "btn button_icons type03 song_info"})[0]["href"].split('\'')[1]
        singurl='https://www.melon.com/song/detail.htm?songId='+singid
        browser.get(singurl)
        randp=round(random.random()*3,2)
        time.sleep(1.5+randp)
        singmelon_html = browser.page_source
        
        singmelon_parse= BeautifulSoup(singmelon_html, 'html.parser')

        try:
            #sing=singmelon_parse.find_all("div",{"id": "d_video_summary"})[0].get_text()

            sing_cont=singmelon_parse.find_all("div",{"id": "d_video_summary"})[0]
            
            for element in sing_cont(text=lambda text: isinstance(text, Comment)):
                element.extract()
            
            sing_cont = sing_cont.contents
            sing_cont[0] = sing_cont[0].replace('\n\t\t\t\t\t\t\t','')
            
            sing = ''
            for txt in sing_cont :
                if type(txt) != 'str' : 
                    sing += str(txt)
                else :
                    sing += txt.rstrip()
            
            print(sing)

        except:
            sing='가사가 없습니다'
        
        day=singmelon_parse.find_all("dl",{"class": "list"})[0]
        day2=day.find_all("dd")[1]
        data[i].append(day2)
        data[i].append(sing)
        a+=1
        
    index+=50    
    dataframe = pd.DataFrame(data)
    dataframe.to_csv("d:\\melon_data\\singdata"+str(index-50)+".csv", header=False, index=False)
