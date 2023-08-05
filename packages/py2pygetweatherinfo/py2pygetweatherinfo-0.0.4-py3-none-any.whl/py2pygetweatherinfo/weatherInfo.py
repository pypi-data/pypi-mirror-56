import sys,time,datetime
from bs4 import BeautifulSoup
import requests
def fetchCode(s):
    page = requests.get("https://weather.codes/india/")
    soup=BeautifulSoup(page.content,"lxml")
    d={}
    dlitem = soup.find("dl")
    l=[]
    for i in dlitem.find_all('dd'):
        l.append(i.text[:-1])
    c=0
    for i in dlitem.find_all('dt'):
        if c==9000:
            break
        d[l[c].casefold()]=i.text
        c=c+1
    try:
        return d[s]
    except KeyError:
        print("place is not found !!!")
        exit()
def main():
    
    if __name__ =="__main__" :
        if(len(sys.argv[1:])==1):
            place=sys.argv[1]
            day = str(datetime.datetime.now())
            currenttime=day[11:16]
            forecasttype="today"
            
        if(len(sys.argv[1:])==2):
            place=sys.argv[1]
            day = str(sys.argv[2])
            if(day[0:7]!=str(datetime.datetime.now())[0:7]):
                print('Please Enter Current month date Only !!')
                exit()
            date=str(day[8:11])
            forecasttype="monthly"
            
        if(len(sys.argv[1:])==3):
            place=sys.argv[1]
            day = str(sys.argv[2])
            if(day[0:7]!=str(datetime.datetime.now())[0:7]):
                print('Please Enter Current month date Only !!')
                exit()
            date=str(day[8:11])
            forecasttype=str(sys.argv[3]).lower()
            if(forecasttype=="hourbyhour" or forecasttype=="hourly" and (str(datetime.datetime.now())[0:10])!=str(sys.argv[2])):
                print('Please Enter Today Date Only For "Hourly" Weather type !!')
                exit()

            if(forecasttype=="today" or forecasttype=="daily" and (str(datetime.datetime.now())[0:10])!=str(sys.argv[2])):
                print('Please Enter Today Date Only For "Daily" Weather type !!')
                exit()
            if(forecasttype=="monthly" or forecasttype=="5day" or forecasttype=="tenday"):
                forecasttype="monthly"
        WeatherCode=fetchCode(place)
        page = requests.get("https://weather.com/en-IN/weather/"+forecasttype+"/l/"+WeatherCode+":1:IN")
        soup=BeautifulSoup(page.content,"lxml")

        print('weatherType : ')
        weatherTypes=soup.find("ul",{"class":"styles__root__1ftiD styles__overflowNav__lGuSb"}).find_all('li')
        for weatherType in weatherTypes[:-1]:
            print(weatherType.text)
        print()
        print('Place : ',place)
        print()
        
        if(forecasttype=="today" or forecasttype=="daily"):
            CurrentTime=soup.find("p",{"class":"today_nowcard-timestamp"}).text
            temp=soup.find("div",{"class":"today_nowcard-temp"}).text
            details=soup.find("div",{"class":"today_nowcard-sidecar component panel"})
            table=soup.find_all("table")
            print('CurrentTime : '+CurrentTime+'\nTemp : '+temp)
            for items in table:
                 for i in items.find_all("tr"):
                        print(str(i.find("th").text)+' - '+str(i.find("td").text))
                        
        if(forecasttype=="hourbyhour" or forecasttype=="hourly"):
            table=soup.find_all("table",{"class":"twc-table"})
            records={}
            currenttime=str(datetime.datetime.now())[11:16]
            minut=int(currenttime[3:6].strip())
            if minut%15!=0:
                if(minut+(15-minut%15))==60:
                    if int(currenttime[0:2])==12:
                        currenttime='01:00'
                    else:
                        hr=int(currenttime[0:2])+1
                        if hr<10:
                            currenttime='0'+str(hr)+':00'
                              
                        currenttime=str(hr)+':00'
                else:
                    currenttime=currenttime[0:2]+':'+str(minut+(15-minut%15))
                
            for items in table:
                 for thead in items.find_all("thead")[0].find_all('tr')[0].find_all("th"):
                        records[str(thead.text).upper()]=''
                 
                 for tr in items.find_all("tbody")[0].find_all('tr'):
                     if str(tr.find_all('td')[1].find_all('span')[0].text)==currenttime:
                         records['TIME']=tr.find_all('td')[1].find_all('span')[0].text
                         records['DESCRIPTION']=tr.find_all('td')[2].find_all('span')[0].text
                         records['TEMP']=tr.find_all('td')[3].find_all('span')[0].text
                         records['FEELS']=tr.find_all('td')[4].find_all('span')[0].text
                         records['PRECIP']=tr.find_all('td')[5].find_all('span')[1].text
                         records['HUMIDITY']=tr.find_all('td')[6].find_all('span')[0].text
                         records['WIND']=tr.find_all('td')[7].find_all('span')[0].text
                         break

            for item in records:
                print(item,' : ',records[item])
        if(forecasttype=="monthly" or forecasttype=="5day" or forecasttype=="tenday"):
            
            table2=soup.find_all("div",{"class":"dayCell"})
            table3=soup.find_all("div",{"class":"futureDayCell"})
            l=[]
            for i in table2:
                d={}
                d["date"]=i.find_all("div",{"class":"date"})[0].text
                d["hitemp"]=i.find_all("div",{"class":"temp hi"})[0].text
                d["lowtemp"]=i.find_all("div",{"class":"temp low"})[0].text
                l.append(d)
            for i in table3:
                d={}
                d["date"]=i.find_all("div",{"class":"date"})[0].text
                d["hitemp"]=i.find_all("div",{"class":"hi"})[0].text
                d["lowtemp"]=i.find_all("div",{"class":"low"})[0].text
                l.append(d)
            
            rl=l[::-1]
            for i in rl:
                if(i['date']==date):
                    indx=int(l.index(i))
                    if(str(sys.argv[3]).lower()=="monthly"):
                        print('Date : {}\nHigh-Temp : {}\nLow-Temp : {}\n'.format(i['date'],i['hitemp'],i['lowtemp']))
                        break
                    if(str(sys.argv[3]).lower()=="5day"):
                        for j in l[indx:(indx+5)]:
                            print('Date : {}\nHigh-Temp : {}\nLow-Temp : {}\n'.format(j['date'],j['hitemp'],j['lowtemp']))
                        break
                    if(str(sys.argv[3]).lower()=="tenday"):
                        for k in l[indx:(indx+10)]:
                            print('Date : {}\nHigh-Temp : {}\nLow-Temp : {}\n'.format(k['date'],k['hitemp'],k['lowtemp']))
                        break
            
                              
