
import globalFunctions as gF

def veto():  #  Resets values in a line to
    print('lnF:', gF.lineno(), '| veto()')
    listInt = int(0)
    #gF.superList = [[],[],[],[],[],[],[],[],[]]
    for lists in gF.superList:
        print('lnF:', gF.lineno(), listInt, lists)
        while len(lists) > 0:
            lists.pop()
        print('lnF:', gF.lineno(), listInt, lists)
        listInt+=1
    gF.soundsLine = [[],[],[],[]]
    gF.printGlobalData()


def makeYLine(quantumLine0, quantumLine1):
    print('lnF:', gF.lineno(), 'makeYLine begin:', quantumLine0, quantumLine1)
    yLine = ([],[])
    for pWords in quantumLine0[0]+quantumLine1[0]:
        yLine[0].append(pWords)
    for rWords in quantumLine0[1]+quantumLine1[1]:
        yLine[1].append(rWords)
    print('lnF:', gF.lineno(), 'makeYLine ended:', yLine)
    return yLine
      

def removeWordL(superPopList):  #  Remove the leftmost word from line
    # do something
    return data

def compareLastWords(qLineA, qLineB):
    lastInt = int(-1)
    while qLineA[0][lastInt] in gF.allPunx:
        lastInt-=1
    checkWordA = qLineA[0][lastInt]
    lastInt = int(-1)    
    while qLineB[0][lastInt] in gF.allPunx:
        lastInt-=1
    checkWordB = qLineB[0][lastInt]
    if checkWordA == checkWordB:
        return True
    else:
        return False

def removeWordR(runLine):  #  Remove the rightmost word from line
    print('lnF:', gF.lineno(), '| removeWordR-in', 'gF.qLine:', gF.qLine, 'runLine:', runLine)
    if len(gF.qLine[0]) == 0 and len(runLine[0]) > 0:  #  Cut runLine
        print('lnF:', gF.lineno(), "| rMR - if0")
        minusWordX = runLine[0].pop(0)  #  Since the previous line didn't yield any following line
        minusWordY = runLine[1].pop(0)  #  minusWordX just holds whatever is getting popped
    if len(gF.qLine[0]) > 0:
        print('lnF:', gF.lineno(), "| rMR - if1")
        minusWord0 = gF.qLine[0].pop()  #  Remove word from first part of line
        minusWord1 = gF.qLine[1].pop()  #  Until better method introduced, cut rLine here
        gF.superBlackList[len(gF.qLine[0])].append(minusWord1)
        gF.fonoFunk.subtractFonoLine((minusWord0, minusWord1))
        print('lnF:', gF.lineno(), '| minusWord0:', minusWord0)
        for lists in gF.superList:
            if len(lists) > 0:
                lists.pop()
            elif len(gF.qLine[1]) > 0:
                print('lnF:', gF.lineno(), '| gF.qLine:', gF.qLine)
        if (len(gF.qLine[0]) == 0) and (len(runLine) == 0):  #  If this was a line-starting word that doesn't fit
            gF.firstBlackList[gF.linesCount].append(minusWord0)
        gF.printGlobalData()
    else:
        gF.soundsLine = [], [], [], []
    #if len(gF.superList[1]) > (len(gF.qLine[1]) + 1):  #  If we've gone further than checking the list of next words
    print('lnF:', gF.lineno(), '| removeWordR() out - gF.qLine:', gF.qLine)
    gF.printGlobalData()
    return runLine


def acceptWordL(nextWord):  #  Add the rightmost word to line

##  INVERT THESE VALUES

    print('lnF:', gF.lineno(), '| acceptWord:', gF.qLine, '-', nextWord)
    gF.qLine[0].append(nextWord)
    if len(gF.proxNumList) > 0:
        proxNum = gF.proxNumList[-1] + 1
    else:
        proxNum = 0
    gF.proxNumList.append(proxNum)
    proxLineNum = gF.proxLineNumList[0] + 1
    gF.proxLineNumList.insert(0, proxLineNum)


def acceptWordR(runLine, nextWord):  #  Add word to right side of line
    print('lnF:', gF.lineno(), '| acceptWordR-in:', gF.qLine, '|', nextWord, 'runLine:', runLine)
    gF.qLine = makeYLine(gF.qLine, nextWord)
    while len(gF.superBlackList) < (len(gF.qLine[0])+1):
        gF.superBlackList.append([])
    print('lnF:', gF.lineno(), gF.qLine)
    print('lnF:', gF.lineno(), '| acceptWordR - adding superList items')
    gF.printGlobalData()
    for lists in gF.superList:
        lists.append([])
    gF.printGlobalData()
    print('lnF:', gF.lineno(), '| runline:', runLine)
    print('lnF:', gF.lineno(), gF.qLine)
    gF.proxFunk.proxDataBuilder([runLine, gF.qLine])
    print('lnF:', gF.lineno(), gF.qLine)
    runLine, killSwitch = gF.popFunk.superPopListMaker([], makeYLine(runLine, gF.qLine), runLine)
    print('lnF:', gF.lineno(), gF.qLine)
    print('lnF:', gF.lineno(), '| acceptWordR-out:', gF.qLine, '|', nextWord, gF.superList[6], gF.superList[7])
    return killSwitch


def lineStarter(proxExpress):  #  Starts the values for the lineMakers
    print('lnF:', gF.lineno(), '| lineStarter() start')
    for lists in gF.superList:  
        lists.append([])        
    if (gF.linesCount == 0) or (len(gF.qAnteLine[1]) == 0):
        for all in gF.firstWords:
            if all not in gF.firstBlackList[gF.linesCount]:
                if all in proxExpress:
                    gF.superList[0][0].append(all)
                else:
                    gF.superList[1][0].append(all)
        gF.qLine, runLine = ([],[]), ([],[])
        killSwitch = False
    elif len(gF.qAnteLine[1]) > 0:
        runLine = makeYLine(gF.qAnteLine, ([],[]))
        gF.proxFunk.proxDataBuilder(runLine)
        runLine, killSwitch = gF.popFunk.superPopListMaker(proxExpress, runLine, runLine)
    else:
        gF.proxFunk.proxDataBuilder(([],[]))
        runLine, killSwitch = gF.popFunk.superPopListMaker(proxExpress, gF.qLine, ([],[]))
    gF.printGlobalData()
    return runLine, killSwitch


def gov(rhymeSwitch, rhymeList):
    print('lnF:', gF.lineno(), '| gov() start', rhymeSwitch)
    #if rhymeList
    veto()  #  Start with empty variables declared. This function is also a reset button if lines are to be scrapped.
    proxExpress = []
    if gF.metSwitch == True:
        print('lnF:', gF.lineno(), '| gov() - len(rhymeList):', len(rhymeList))
        for rhymes in rhymeList:
            if rhymes in gF.splitTextList:
                proxExpress.append(rhymes)
        print('lnF:', gF.lineno(), '| gov() - len(proxExpress):', len(proxExpress))
        killSwitch = gF.meterFunk.gov(rhymeSwitch, proxExpress)
    else:
        print('lnF:', gF.lineno(), '| gov() - plainLiner activate')
        killSwitch = gF.plainFunk.plainLinerLtoR(gF.qAnteLine)
    if killSwitch == True:
        print('lnF:', gF.lineno(), 'gov() - killSwitch')
        if len(gF.qLine[0]) > 0:
            print('lnF:', gF.lineno(), 'kill0', gF.qLine)
            veto()
        elif len(gF.qAnteLine) > 0:  #  If the previous sentence was almost there, go back and continue with the last word removed
            print('lnF:', gF.lineno(), 'kill1')
            gF.qLine = ([],[])
            gF.qAnteLine = removeWordR(gF.qAnteLine)
            for anteWords0 in gF.qAnteLine[0]:
                gF.qLine[0].append(anteWords0)
            for anteWords1 in gF.qAnteLine[1]:
                gF.qLine[1].append(anteWords1)
            if len(gF.stanza) > 0:
                for anteEmps in gF.empMap[len(gF.stanza)-1]:
                    gF.soundsLine[3].append(anteEmps)
                gF.stanza.pop()
            gF.qAnteFonoLine = []
            return False
        else:
            print('lnF:', gF.lineno(), 'kill2')
            veto()
        return True
    else:
        print('lnF:', gF.lineno(), '| gov() - last else', gF.qLine)
        return False  #  usedList, killSwitch
