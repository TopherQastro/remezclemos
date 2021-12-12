
import globalFunctions as gF

def veto(firstWord):  #  Resets values in a line to
    print('lnF:', gF.lineno(), '| veto()', firstWord)
    listInt = int(0)
    #gF.superList = [[],[],[],[],[],[],[],[],[]]
    if (len(firstWord) > 0) and (firstWord not in gF.firstBlackList):
        gF.firstBlackList.append(firstWord)
    for lists in gF.superList:
        print('lnF:', gF.lineno(), listInt, lists)
        while len(lists) > 0:
            lists.pop()
        print('lnF:', gF.lineno(), listInt, lists)
        listInt+=1
    gF.soundsLine = [[],[],[],[]]
    gF.printGlobalData([[],[]])

    return ([],[])
          # qLine
          

def removeWordL(superPopList, qLine):  #  Remove the leftmost word from line
    # do something
    return data


def removeWordR(qLine, runLine):  #  Remove the rightmost word from line
    print('lnF:', gF.lineno(), '| removeWordR-in', 'qLine:', qLine, 'runLine:', runLine)
    if len(qLine[0]) == 0 and len(runLine[0]) > 0:  #  Cut runLine
        print('lnF:', gF.lineno(), "| rMR - if0")
        minusWordX = runLine[0].pop(0)  #  Since the previous line didn't yield any following line
        minusWordY = runLine[1].pop(0)  #  minusWordX just holds whatever is getting popped
    if len(qLine[0]) > 0:
        print('lnF:', gF.lineno(), "| rMR - if1")
        minusWord0 = qLine[0].pop()  #  Remove word from first part of line
        minusWord1 = qLine[1].pop()  #  Until better method introduced, cut rLine here
        gF.fonoFunk.subtractFonoLine((minusWord0, minusWord1))
        print('lnF:', gF.lineno(), '| minusWord0:', minusWord0)
        for lists in gF.superList:
            if len(lists) > 0:
                lists.pop()
            elif len(qLine[1]) > 0:
                print('lnF:', gF.lineno(), '| qLine:', qLine)
        if (len(qLine[0]) == 0) and (len(runLine) == 0):  #  If this was a line-starting word that doesn't fit
            gF.firstBlackList[gF.linesCount].append(minusWord0)
        gF.printGlobalData(qLine)
    else:
        gF.soundsLine = [], [], [], []
    #if len(gF.superList[1]) > (len(qLine[1]) + 1):  #  If we've gone further than checking the list of next words
    print('lnF:', gF.lineno(), '| removeWordR() out - qLine:', qLine)
    gF.printGlobalData(qLine)
    return qLine, runLine


def acceptWordL(qLine, nextWord):  #  Add the rightmost word to line

##  INVERT THESE VALUES

    print('lnF:', gF.lineno(), '| acceptWord:', qLine, '-', nextWord)
    qLine[0].append(nextWord)
    if len(gF.proxNumList) > 0:
        proxNum = gF.proxNumList[-1] + 1
    else:
        proxNum = 0
    gF.proxNumList.append(proxNum)
    proxLineNum = gF.proxLineNumList[0] + 1
    gF.proxLineNumList.insert(0, proxLineNum)
    return qLine


def acceptWordR(runLine, qLine, nextWord):  #  Add word to right side of line
    print('lnF:', gF.lineno(), '| acceptWordR-in:', qLine, '|', nextWord, 'runLine:', runLine)
    qLine[0].append(nextWord[0])
    qLine[1].append(nextWord[1])
    print('lnF:', gF.lineno(), qLine)
    print('lnF:', gF.lineno(), '| acceptWordR - adding superList items')
    gF.printGlobalData(qLine)
    for lists in gF.superList:
        lists.append([])
    gF.printGlobalData(qLine)
    print('lnF:', gF.lineno(), qLine, (runLine[0]+qLine[0], runLine[1]+qLine[1]))
    gF.proxFunk.proxDataBuilder((runLine[0]+qLine[0], runLine[1]+qLine[1]), len(runLine[1]+qLine[1]))
    print('lnF:', gF.lineno(), qLine)
    qLine, runLine, killSwitch = gF.popFunk.superPopListMaker([], qLine, runLine)
    print('lnF:', gF.lineno(), qLine)
    print('lnF:', gF.lineno(), '| acceptWordR-out:', qLine, '|', nextWord, gF.superList[6], gF.superList[7])
    return qLine, killSwitch


def lineStarter(qAnteLine, proxExpress):  #  Starts the values for the lineMakers
    print('lnF:', gF.lineno(), '| lineStarter() start')
    for lists in gF.superList:  
        lists.append([])        
    if (gF.linesCount == 0) or (len(qAnteLine) == 0):
        for all in gF.firstWords:
            if all not in gF.firstBlackList[gF.linesCount]:
                if all in proxExpress:
                    gF.superList[0][0].append(all)
                else:
                    gF.superList[1][0].append(all)
        qLine = ([],[])
    else:
        gF.proxFunk.proxDataBuilder(qAnteLine, len(qAnteLine[1]))
        qLine, runLine, killSwitch = gF.popFunk.superPopListMaker(proxExpress, ([],[]), qAnteLine)
    gF.printGlobalData(qLine)
    return qAnteLine, qLine


def gov(empsKeyLine, rhymeThisLine, rhymeList, qAnteLine, qAnteFonoLine):
    print('lnF:', gF.lineno(), '| gov() start', rhymeThisLine)
    qLine = veto(str())  #  Start with empty variables declared. This function is also a reset button if lines are to be scrapped.
    proxExpress = []
    if gF.metSwitch == True:
        print('lnF:', gF.lineno(), '| gov() - len(rhymeList):', len(rhymeList))
        for rhymes in rhymeList:
            if rhymes in gF.splitTextList:
                proxExpress.append(rhymes)
        print('lnF:', gF.lineno(), '| gov() - len(proxExpress):', len(proxExpress))
        qLine, killSwitch = gF.meterFunk.gov(empsKeyLine, rhymeThisLine, qLine, qAnteLine, qAnteFonoLine, proxExpress)
    else:
        print('lnF:', gF.lineno(), '| gov() - plainLiner activate')
        qLine, killSwitch = gF.plainFunk.plainLinerLtoR(qAnteLine)
    if killSwitch == True:
        print('lnF:', gF.lineno(), 'gov() - killSwitch')
        if len(qLine[0]) > 0:
            print('lnF:', gF.lineno(), 'kill0', qLine)
            qLine = veto(qLine[0][0])
        else:
            print('lnF:', gF.lineno(), 'kill1')
            qLine = veto(str())
        return qLine, True
    else:
        print('lnF:', gF.lineno(), '| gov() - last else', qLine)
        return qLine, False  #  usedList, qLine, killSwitch
