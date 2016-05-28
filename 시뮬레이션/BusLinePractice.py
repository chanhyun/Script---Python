from xml.dom.minidom import parse,parseString
from xml.etree import ElementTree

import urllib.request

#서버에서받아오는거로 시뮬해야함(해결)
#5.17일 대전버스 5번 정보(막차시간,출발시간,출발지,종착지등)검색구현함

#검색기능 추가해야함 - 버스정류장장소 검색추가예정(1)
#(1)번에서 노선만 나오게하려면? 코드번호까지나오는건 비효율적


#Gmail 기능추가해야함
#데이터베이스, 기능추가해야함
#c와 c++연동 해야함

loopFlag=1
xmlFD=-1
Logtext=-1
####현재 대전 버스5번만 되어있음########
Bus=None

    
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
        SearchBus(busnumber)
        #SprintBuslist(SearchBus(busnumber))
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
def EraseFilecontext():#파일내용삭제 함수
    global Logtext
    Logtext="log.txt"#음.. 기존의 파일로 시작하기위해선 이리해야되나.
    L=open(Logtext,"w")
    L.write("you Erased the previous records")
    L.close()
    printMenu()
    menuKey=str(input('select menu:'))
    launcherFunction(menuKey)
    
    
    
def Quitprogram():#종료하는 함수
    global loopFlag
    loopFlag=0
    FreeBus()
 #
def SearchBus(busnumber):
    global Bus
    global Logtext
    #BusdataList=[None]*10
    Bus_data={ "startnodenm":"출발지","endnodenm":"종착지","startvehicletime":"시작시간","endvehicletime":"막차시간" \
               ,"intervalsattime":"interval","intervalsuntime":"intervalsuntime","intervaltime":"intervaltime","routeid":"routeid"\
               , "routeno":"routeno","routetp":"routetp"}
    if busnumber=='5':
        BusInformUrl="http://openapi.tago.go.kr/openapi/service/BusRouteInfoInqireService/getRouteInfoIem?ServiceKey=qDDXL%2BLNCCmRozJ46Dxv%2FMprdc%2FeMiRN5XZpSCGAjBdGn5KC%2FnSSc3%2FhC8sFOWNQkC1ADJgG%2FRgdUEsF%2FdF6gg%3D%3D&cityCode=25&routeId=DJB30300004ND&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
        data=urllib.request.urlopen(BusInformUrl).read()#5번버스의 정보출력
        BusLineUrl="http://openapi.tago.go.kr/openapi/service/BusRouteInfoInqireService/getRouteAcctoThrghSttnList?ServiceKey=qDDXL%2BLNCCmRozJ46Dxv%2FMprdc%2FeMiRN5XZpSCGAjBdGn5KC%2FnSSc3%2FhC8sFOWNQkC1ADJgG%2FRgdUEsF%2FdF6gg%3D%3D&routeId=DJB30300004ND&cityCode=25&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
        BusLine=urllib.request.urlopen(BusLineUrl).read()#5번버스의경로노선,BusLine은 공통 변수로 사용가능
    
    #공통부분
    Logtext="log.txt"
    filename="Bus.xml"
    f=open(filename,"wb")#xml file 
    L=open(Logtext,"ab")#데이터저장하는 파일
    f.write(data)
    L.write(data)#url은변수내용  바뀌기만 하면됨, 변수이름은 버스정보바뀌어도 그대로 사용가능함
    
    f.close()
    L.close()
    tree=parse(filename)
    Bus=tree
    FindBus=Bus.childNodes
    Busnum=FindBus[0].childNodes
    for item in Busnum:
        if item.nodeName=="body":
            subitems=item.childNodes#items 로넘어감
            for atom in subitems:# items에서 
                if atom.nodeName=="items":
                    ssubitems=atom.childNodes
                        #print(atom)
                    for last in  ssubitems:
                            if last.nodeName=="item":
                                 #print(last)
                                itl = last.childNodes#last = item 헤더부분
                                 #print(itl)#10가지헤더부분
                                for it in itl:
                                    print(it.nodeName)
                                    for v in Bus_data.keys():#얘까지돈다.
                                        if(it.nodeName==v):
                                            print(it.firstChild.nodeValue)
                                            print(end="")
                                            
    YN=str(input("이 버스의 경로를 찾으시겠습니까?(y,n)"))
    if(YN=='y' or YN=='Y'):
        f=open(filename,"wb")
        f.write(BusLine)
        L=open(Logtext,"ab")#a는 add의 약자로 파일 내용 기존에있던거에서 내용추가해서 덧붙임
        L.write(BusLine)
        f.close()
        Stree=parse(filename)#second tree
        Bus=Stree
        FindBus=Bus.childNodes
        Busnum=FindBus[0].childNodes
        for item in Busnum:
            if item.nodeName=="body":
                subitems=item.childNodes
                for atom in subitems:
                    if atom.nodeName=="items":
                        ssubitems=atom.childNodes
                        for last in  ssubitems:
                                if last.nodeName=="item":
                                    itl = last.childNodes#last = item 헤더부분
                                    for it in itl:
                                        print(it.nodeName," ",end=' ')
                                        print(it.firstChild.nodeValue)
    elif(YN=='n' or YN=='N'):
        L.close()
        print("MENU 선택화면으로 돌아갑니다.")
        printMenu()
        menuKey=str(input('select menu:'))
        launcherFunction(menuKey)
    else:
        print("y or n 만 선택해주세요")
                    
                                    
                                        
        #return None
def SprintBuslist(Buslist):
    for BusInform in Buslist:
        print(BusInform)
def FreeBus():#종료후에 실질적으로 메모리 해제하는함수
    if checkDocument():#xml문서 여부확인후에 
        Bus.unlink()#메모리 실질적으로 해제함
        
def checkDocument():#xml문서 로드를 안했다면 오류뜨게, 아니면 continue
    global Bus
    if Bus==None :
        print("Error: Document is empty")
        return False
    return True

while(loopFlag>0):#시작부분코드
    printMenu()
    menuKey=str(input('select menu:'))

    launcherFunction(menuKey)
else:
    print("thank you! bye")
