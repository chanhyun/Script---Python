from xml.dom.minidom import parse,parseString
from xml.etree import ElementTree

loopFlag=1
xmlFD=-1

Lostthings=None
def printMenu():
    print("\nWelcome! Lostthings Manager Program (xml version)") 
    print("========Menu==========")
    print("Load xml:  l")
    print("print Lost list: L")
    print("==================")
def launcherFunction(menu):
    global Lostthings
    if menu ==  'l':
        Lostthings = LoadXMLFromFile()
    elif menu == 'L':
        PrintLostList(["fdPrdtNm",])
def LoadXMLFromFile():
    filename=str(input("please input file name to load:"))
    global xmlFD

    try:
        xmlFD=open(filename,"rb")
    except IOError:
        print("invalid file name or path")
        return None
    else:
        try:
            dom=parse(xmlFD)
        except Exception:
            print("loading fail")
        else:
            print("XML Document loading complete")
            return dom
    return None
def PrintLostList(tags):
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
                                 itl = last.childNodes
                                 for it in itl:
                                     print(it.firstChild.nodeValue)
                                 

                             
def FreeLostthings():
    if checkDocument():
        Lostthings.unlink()
def checkDocument():
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
