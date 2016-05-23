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

loopFlag=1
xmlFD=-1
BusDoc=None
conn = None
regKey = 'PWIFTthzdz6Il8%2FAJ%2FASVFqKDtEAYoXdpKP6%2Bvq%2FLINz9URHz6rA4OQ64EOSgFEHDx%2F7WboeJ%2F9Z90wSP0wOPQ%3D%3D' 

# 네이버 OpenAPI 접속 정보 information
server = "openapi.tago.go.kr"

def printMenu():#입력 매뉴얼 알려주는 함수
    print("\nWelcome! BusLine Manager Program (xml version)") 
    print("========Menu==========")
    print("search Bus num: s")
    print("Quit menu: q")
    print("Erase File context:E")
    print("==================")
    
def launcherFunction(menu):# 명령어 입력하여 실질적으로 수행처리하는 부분
    global Bus
    if menu == 's':
        busnumber=str(input("input BusNumber to search for Information "))
        routeid = SearchBus(busnumber)
        try:        
            routedic = printroute(routeid["routeID"])
            print(str(routedic["전자디자인고"]))
            nowbusdic = nowbus(routeid["routeID"])
            position = int(routedic["송강중학교"])
            print(position)
            maxpos = 0 # 내가 있는 정류장보다 앞에있는 버스중에 제일 가까이 있는 버스           
            for now in nowbusdic: 
                if maxpos == 0: #버스정류장이 0이면 제일 먼저거 넣음
                    maxpos = int(nowbusdic[now])
                if int(nowbusdic[now]) < position and int(nowbusdic[now]) > maxpos: #버스가 정류장보다 앞에있고 maxpos보다 더 큰지
                    maxpos = int(nowbusdic[now]) 
            print(str(position-maxpos) + "정류장 남았습니다.") #현재위치 - 버스위치 = 남은 정류장 수
        except Exception: # 예외처리 : 버스번호 자체가 없거나 현재 움직이는 버스가 없다.
            print("No Bus!")
    elif menu == 'q':
        Quitprogram()
    elif menu == 'E':
        Key=str(input("file내용을 삭제 하시겠습니까? 이전에 봤던 모든기록이 지워집니다.(y,n)"))
        if(Key=='y' or Key=='Y'):
            EraseFilecontext()
        elif(Key=='n' or Key=='N'):
            printMenu()
            menuKey=str(input('select menu:'))
            launcherFunction(menuKey)
        else:
            print("다시누르세요 y or n")

def printroute(routeid): #전체 노선같고옴
    if conn == None :
        connectOpenAPIServer()
    uri = userURIBuilder(server,"BusRouteInfoInqireService/getRouteAcctoThrghSttnList", ServiceKey=regKey,routeId=routeid,cityCode="25",pageSize="999",pageNo="1",startPage="1")    
    #print(uri)    
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
        
def nowbus(routeid): #현재 움직이는 버스 위치
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

def userURIBuilder(server,service,**user):
    str = "https://" + server + "/openapi/service/" + service + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def SearchBus(busnumber): #버스번호로 검색
    if conn == None :
        connectOpenAPIServer()
    uri = userURIBuilder(server, "BusRouteInfoInqireService/getRouteNoList",ServiceKey=regKey, cityCode="25",routeNo=busnumber,pageSize="999",pageNo="1",startPage="1")    
    conn.request("GET", uri)
    
    req = conn.getresponse()
    print (req.status)
    if int(req.status) == 200 :
        print("Bus data downloading complete!")
        return extractRouteidData(req.read()) #버스번호 사전화
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None

def extractRouteidData(strXml): #버스의 routeID를 얻어옴
    tree = ElementTree.fromstring(strXml)
    #print (strXml)
    # Book 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("item")  # return list type
    #print(itemElements)
    for item in itemElements:
        routeID = item.find("routeid")
        print (routeID.text)
        if len(routeID.text) > 0 :
           return {"routeID":routeID.text}

def extractRouteData(strXml): # 버스의 정류장이름(nodenm)과 순서(nodeord)를 얻어옴
    tree = ElementTree.fromstring(strXml)
    #print (strXml)
    # Book 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("item")  # return list type
    nodedic = {}
    #print(itemElements)
    for item in itemElements:
        global nodedic
        nodenm = item.find("nodenm")
        nodeord = item.find("nodeord")        
        if len(nodenm.text) > 0 :            
            nodedic[nodenm.text] = nodeord.text
            nodedic[nodenm.text]
    return nodedic

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)


while(loopFlag>0):#시작부분코드
    printMenu()
    menuKey=str(input('select menu:'))

    launcherFunction(menuKey)
else:
    print("thank you! bye")

            
