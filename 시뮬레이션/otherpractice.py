from xml.dom.minidom import parse,parseString
from xml.etree import ElementTree

import urllib.request
#수정기능은 딱히 필요없음, open APi이기때문에 매일 정보가 최신화됨
#서버에서받아오는거로 시뮬해야함
#검색기능 추가해야함 - 물건찾는 검색기능 추가완료, 장소 검색추가예정
#다양한통계 추가해야함...ex)가장 많이 읽어버리는 품목
#Gmail 기능추가해야함
#데이터베이스, 기능추가해야함
#c와 c++연동 해야함 
loopFlag=1
xmlFD=-1


Lostthings=None

    
def printMenu():#입력 매뉴얼 알려주는 함수
    print("\nWelcome! Lostthings Manager Program (xml version)") 
    print("========Menu==========")
    print("Load xml:  l")
    print("print Lost list: L")
    print("Search Lost things: s")
    print("Quit menu: q")
    print("==================")
def launcherFunction(menu):# 명령어 입력하여 실질적으로 수행처리하는 부분
    global Lostthings
    if menu ==  'l':
        Lostthings = LoadXMLFromFile()
    elif menu == 'L':
        PrintLostList(["fdPrdtNm",])
    elif menu == 's':
        keyword=str(input("input keyword to search"))
        SprintLostlist(SearchLost(keyword))
    elif menu == 'q':
        Quitprogram()
def LoadXMLFromFile():#파일 파싱하는 함수
    #key='qDDXL%2BLNCCmRozJ46Dxv%2FMprdc%2FeMiRN5XZpSCGAjBdGn5KC%2FnSSc3%2FhC8sFOWNQkC1ADJgG%2FRgdUEsF%2FdF6gg%3D%3D&cityCode=25&routeId=DJB30300101ND&numOfRows=999&pageSize=999&pageNo=1&startPage=1'
    url="http://openapi.lost112.go.kr/openapi/service/rest/LosfundInfoInqireService/getLosfundInfoAccToClAreaPd?PRDT_CL_CD_01=PRL000&PRDT_CL_CD_02=PRL100&ServiceKey=sea100UMmw23Xycs33F1EQnumONR%2F9ElxBLzkilU9Yr1oT4TrCot8Y2p0jyuJP72x9rG9D8CN5yuEs6AS2sAiw%3D%3D"

    data=urllib.request.urlopen(url).read()
    #filename=str(input("please input file name to load:"))
    filename="Lostthings.xml"
    f=open(filename,"wb")
    f.write(data)
    f.close()
    tree=parse(filename)
    return tree
def Quitprogram():#종료하는 함수
    global loopFlag
    loopFlag=0
    FreeLostthings()
    
def SearchLost(keyword):
    global Lostthings
    Lostlist =[]
    
    if not checkDocument():
         return None
    try:
       
        tree = ElementTree.fromstring(str(Lostthings.toxml()))
    except Exception:
        print ("Element Tree parsing Error: maybe the xml document is not correct")
        return None
    LostElements = tree.getiterator("item")
    for item in LostElements:
        LostTitle=item.find("fdPrdtNm")
        if(LostTitle.text.find(keyword) >= 0):
                           print(LostTitle)#여기에있는데 왜 값은 안나올
                           Lostlist.append((LostTitle.text))
    return Lostlist
def SprintLostlist(Llist):
    for Los in Llist:
        print(Los)
                           
def PrintLostList(tags):#전체정보 출력하는 부분
     global Lostthings
     if not checkDocument():
         return None
     Lostlist=Lostthings.childNodes
     print(Lostlist)
     Lost=Lostlist[0].childNodes
     print(Lost)
     for item in Lost:
         if item.nodeName=="body":
             subitems=item.childNodes#items 로넘어감
             for atom in subitems:# items에서 
                 if atom.nodeName=="items":
                        ssubitems=atom.childNodes
                        for last in  ssubitems:
                             if last.nodeName=="item":
                                 itl = last.childNodes#last = item 헤더부분
                                 for it in itl:
                                     print(it.firstChild.nodeValue)
                                 

                             
def FreeLostthings():#종료후에 실질적으로 메모리 해제하는함수
    if checkDocument():#xml문서 여부확인후에 
        Lostthings.unlink()#메모리 실질적으로 해제함
        
def checkDocument():#xml문서 로드를 안했다면 오류뜨게, 아니면 continue
    global Lostthings
    if Lostthings==None :
        print("Error: Document is empty")
        return False
    return True

while(loopFlag>0):#시작부분코드
    printMenu()
    menuKey=str(input('select menu:'))

    launcherFunction(menuKey)
else:
    print("thank you! bye")
