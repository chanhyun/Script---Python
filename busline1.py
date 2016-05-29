# -*- coding: utf-8 -*-
"""
Created on Mon May 23 12:09:50 2016

@author: chanhyun
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 19 16:23:30 2016

@author: Administrator
"""

from xml.dom.minidom import parse,parseString
from xml.etree import ElementTree

import urllib.request

from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
import smtplib
loopFlag=1
xmlFD=-1
BusDoc=None
conn = None
host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"
regKey = 'PWIFTthzdz6Il8%2FAJ%2FASVFqKDtEAYoXdpKP6%2Bvq%2FLINz9URHz6rA4OQ64EOSgFEHDx%2F7WboeJ%2F9Z90wSP0wOPQ%3D%3D' 
uri=None
WantStation=None#목적지 정류장 입력변수
StartStation=None #자신이 있는 정류장 입력변수


# 네이버 OpenAPI 접속 정보 information
server = "openapi.tago.go.kr"

def printMenu():#입력 매뉴얼 알려주는 함수
    print("\nWelcome! BusLine Manager Program (xml version)") 
    print("========Menu==========")
    print("search Bus num: s")
    print("Quit menu: q")
    print("Send Mail: M")
    print("Erase File context:E")
    print("==================")

def ect(routeid):
    try:        
        routedic = Printroute(routeid["routeID"])#routeid = DJB3030004ND,5번의 전체노선 코드번호
        NowBusdic = NowBus(routeid["routeID"])
        position = int(routedic["송강중학교"])
        print(position)
        maxpos = 0 # 내가 있는 정류장보다 앞에있는 버스중에 제일 가까이 있는 버스           
        for now in NowBusdic: 
            if maxpos == 0: #버스정류장이 0이면 제일 먼저거 넣음
                maxpos = int(NowBusdic[now])
            if (int(NowBusdic[now]) < position) and (int(NowBusdic[now]) > maxpos): #버스가 정류장보다 앞에있고 maxpos보다 더 큰지
                maxpos = int(NowBusdic[now]) 
        if position-maxpos > 0:
            result = (str(position-maxpos) + "정류장 남았습니다.")
        else:
            result = "다시 검색해주세요"
        return result #현재위치 - 버스위치 = 남은 정류장 수
    except Exception: # 예외처리 : 버스번호 자체가 없거나 현재 움직이는 버스가 없다.
        return False

    
    
def launcherFunction(menu):# 명령어 입력하여 실질적으로 수행처리하는 부분
    if menu == 's' or menu == 'S':
        busnumber=str(input("input BusNumber to search for Information "))#원하는 버스 번호 얻어오고
        routeid = SearchBus(busnumber)#Search함수에 5번 넣고
        print (ect(routeid))
    elif menu == 'q' or menu == 'Q':
        Quitprogram()
    elif menu == 'M' or menu == 'm':
        SendMail()
    elif menu == 'E':
        Key=str(input("file내용을 삭제 하시겠습니까? 이전에 봤던 모든기록이 지워집니다.(y,n)"))
        if(Key=='y' or Key=='Y'):
            pass
            #EraseFilecontext()
        elif(Key=='n' or Key=='N'):
            printMenu()
            menuKey=str(input('select menu:'))
            launcherFunction(menuKey)
        else:
            print("다시누르세요 y or n")
def SearchBus(busnumber): #버스번호로 검색
    if conn == None :
        connectOpenAPIServer()
    uri = userURIBuilder(server, "BusRouteInfoInqireService/getRouteNoList",ServiceKey=regKey, cityCode="25",routeNo=busnumber,pageSize="999",pageNo="1",startPage="1")#server=server
    #service=BusRoute~NoList
    #**user= Servicekey,cityCode,routeno,pagesize,pageno,startpage (key) and = user[key](==value?)
    conn.request("GET", uri)
    
    req = conn.getresponse()#응답시키
    print (req.status)
    if int(req.status) == 200 :
        print("Bus data downloading complete!")
        return extractRouteidData(req.read()) #버스번호 사전화 ,request가 현재 url에있는 정보들 다 뽑아옴.
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None
    
def extractRouteidData(strXml): #버스의 routeID를 얻어옴,단순 특정버스 전체 노선출력
    tree = ElementTree.fromstring(strXml)
    #print (strXml)
    itemElements = tree.getiterator("item")  # return list type
    #print(itemElements)
    for item in itemElements:
        routeID = item.find("routeid")
        #print(10000000)
        print (routeID.text)
        if len(routeID.text) > 0 :
           return {"routeID":routeID.text}

def extractRouteData(strXml): # 버스의 정류장이름(nodenm)과 순서(nodeord)를 얻어옴
    tree = ElementTree.fromstring(strXml)
    #print (strXml)
    itemElements = tree.getiterator("item")  # return list type
    nodedic = {}
    #print(itemElements)
    for item in itemElements:
        global nodedic
        nodenm = item.find("nodenm")
        nodeord = item.find("nodeord")        
        if len(nodenm.text) > 0 :            
            nodedic[nodenm.text] = nodeord.text#여기해석이 안되네
    return nodedic
            
def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)#http://www.(data.go.kr) ()는 "openapi.tago.go.kr"

def userURIBuilder(server,service,**user):
    str = "https://" + server + "/openapi/service/" + service + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str            
def Quitprogram():
    global loopFlag
    loopFlag = 0
    FreeBus()
def FreeBus():#종료후에 실질적으로 메모리 해제하는함수
        exit
def Printroute(routeid): #전체 노선갖고옴
    if conn == None :
        connectOpenAPIServer()
    uri = userURIBuilder(server,"BusRouteInfoInqireService/getRouteAcctoThrghSttnList", ServiceKey=regKey,routeId=routeid,cityCode="25",pageSize="999",pageNo="1",startPage="1")    
    #print(uri)
    #노선버스 위치별 목록조회.gps딸려있음
    conn.request("GET", uri)
    
    req = conn.getresponse()
    #print (req.status)
    if int(req.status) == 200 :
        print("BusNode data downloading complete!")
        routedic = extractRouteData(req.read())#노선 사전화
        return routedic
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None
        
def NowBus(routeid): #현재 움직이는 버스 위치
    if conn == None :
        connectOpenAPIServer()
    uri = userURIBuilder(server,"BusLcInfoInqireService/getRouteAcctoBusLcList", ServiceKey=regKey,cityCode="25", routeId=routeid, pageSize="999", pageNo="1",startPage="1")    
    #print(uri)    
    conn.request("GET", uri)
    
    req = conn.getresponse()
    #print (req.status)
    if int(req.status) == 200 :
        print("reflash data downloading complete!")
        routedic = extractRouteData(req.read()) #노선 사전화
        return routedic
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None


def MakeHtmlDoc(Buslinelist):
    from xml.dom.minidom import getDOMImplementation
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None,"html",None)
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)
    body = newdoc.createElement('body')

    
    b = newdoc.createElement('b')
    bustext=newdoc.createTextNode("Wait Bus!")
    b.appendChild(bustext)
    body.appendChild(b)
        
    p=newdoc.createElement('p')
    titleText=newdoc.createTextNode(Buslinelist)
    p.appendChild(titleText)
    body.appendChild(p)
    
    top_element.appendChild(body)
    return newdoc.toxml()    
  
    


def SendMail():
    global host, port
    html = ""
    title = str(input ('Title :'))
    senderAddr= "stephano2037@gmail.com"
    passwd= "dntrlwlak3"
    recipientAddr = str(input ('recipient email address :'))
   # writemsg=str(input(' write something:'))
    while(1):
        msgtext = str(input ('Do you want to include Bus data (y/n) '))    
        if msgtext == 'y' or msgtext == 'Y':
            keyword = str(input ('input keyword to search:'))
            busid = {}        
            busid = SearchBus(keyword)
            html = MakeHtmlDoc(ect(busid))
            break
        elif msgtext == 'n' or msgtext == 'N':
            return
    
        
    
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    #msgPart = MIMEText(writemsg)
    BusPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # 메세지에 생성한 MIME 문서를 첨부합니다.
    #msg.attach(msgPart)
    msg.attach(BusPart)
    
    print ("connect smtp server ... ")
    s = smtplib.SMTP(host,port)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)    # 로긴을 합니다. 
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()
    
    print ("Mail sending complete!!!")

while(loopFlag>0):#시작부분코드
    printMenu()
    menuKey=str(input('select menu:'))

    launcherFunction(menuKey)
else:
    print("thank you! bye")

            
