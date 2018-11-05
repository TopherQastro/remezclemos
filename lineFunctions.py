
import globalFunctions as gF

def veto():  #  Resets values in a line to
    print('liF:', gF.lineno(), 'veto()')
    for lists in gF.superList:
        lists = []
    #     while len(lists) > 0:
    #         mList.pop()
    gF.printGlobalData([[],[]])
    return ([],[]), []
          #qLine, pLEmps
          

def removeWordL(superPopList, qLine):  #  Remove the leftmost word from line
    # do something
    return data


def removeWordR(empLine, qLine, runLine):  #  Remove the rightmost word from line
    print('liF:', gF.lineno(), 'removeWordR-in', 'qLine:', qLine, 'runLine:', runLine)
    if len(qLine[0]) == 0 and len(runLine[0]) > 0:  #  Cut runLine
        print('liF:', gF.lineno(), "rMR - if0")
        minusWordX = runLine[0].pop(0)  #  Since the previous line didn't yield any following line
        minusWordY = runLine[1].pop(0)  #  minusWordX just holds whatever is getting popped
    if len(qLine[0]) > 0:
        print('liF:', gF.lineno(), "rMR - if1")
        minusWord0 = qLine[0].pop()  #  Remove word from first part of line
        minusWord1 = qLine[1].pop()  #  Until better method introduced, cut rLine here
        pWEmps = gF.pEmpsLine(empLine, [minusWord0])
        pLEmps = gF.pEmpsLine(empLine, qLine[0])
        print('liF:', gF.lineno(), qLine, pLEmps, pWEmps)
        pLEmps = pLEmps[:-len(pWEmps)]  #  Cut emps from main line)
        gF.superBlackList.pop()  #  If we leave blacklisted words further down the road, they may negate an otherwise compatible sentence
        print('liF:', gF.lineno(), 'minusWord0:', minusWord0)
        gF.superBlackList[-1].append(minusWord0)  #  Add to blackList at correct point
    else:
        pLEmps = []
    #if len(gF.superPopList) > (len(qLine[1]) + 1):  #  If we've gone further than checking the list of next words
    print('liF:', gF.lineno(), '| removeWordR() - snipPopList')
    for lists in (gF.superList[:-3] and gF.superList[-2:]):
        if len(lists) > 0:
            lists.pop()
        elif len(qLine[1]) > 0:
            print('liF:', gF.lineno(), '|', qLine)
            gF.printGlobalData(qLine)
    print('liF:', gF.lineno(), '| removeWordR() out - qLine:', qLine)
    gF.printGlobalData(qLine)
    return pLEmps, qLine, runLine


def acceptWordL(qLine, nextWord):  #  Add the rightmost word to line

##  INVERT THESE VALUES

    print('liF:', gF.lineno(), '| acceptWord:', qLine, '-', nextWord)
    pLine.append(nextWord)
    if len(proxNumList) > 0:
        proxNum = proxNumList[-1] + 1
    else:
        proxNum = 0
    proxNumList.append(proxNum)
    proxLineNum = proxLineNumList[0] + 1
    proxLineNumList.insert(0, proxLineNum)
    return qLine


def acceptWordR(empLine, runLine, qLine, nextWord):  #  Add word to right side of line
    print('liF:', gF.lineno(), '| acceptWordR-in:', qLine, '|', nextWord, 'runLine:', runLine)
    qLine[0].append(nextWord[0])
    qLine[1].append(nextWord[1])
    print('liF:', gF.lineno(), qLine)
    #gF.proxFunk.proxDataBuilder(gF.qLineIndexList, proxDicIndexList, qLine, len(qLine[1]))
    #if len(gF.superBlackList) == len(qLine[1]):  #  We don't have any blackListed words that far ahead
    print('liF:', gF.lineno(), '| acceptWordR - adding superList items')
    gF.printGlobalData(qLine)
    for lists in gF.superList:
        lists.append([])
    gF.printGlobalData(qLine)
    print('liF:', gF.lineno(), qLine, (runLine[0]+qLine[0], runLine[1]+qLine[1]))
    gF.proxFunk.proxDataBuilder((runLine[0]+qLine[0], runLine[1]+qLine[1]), len(runLine[1]+qLine[1]))
    print('liF:', gF.lineno(), qLine)
    qLine, runLine = gF.popFunk.superPopListMaker(empLine, [], qLine, runLine)
    print('liF:', gF.lineno(), qLine)
    print('liF:', gF.lineno(), '| acceptWordR-out:', qLine, '|', nextWord, gF.qLineIndexList, gF.proxDicIndexList)
    return qLine


def lineStarter(qAnteLine, proxExpress):  #  Starts the values for the lineMakers
    print('lnF:', gF.lineno(), '| lineStarter() | start')
    runLine = ([],[])
    for anteWords in qAnteLine[0]:  #  qAnteLine gets appended to runLine because this function will be cutting from it when it doesn't yield results
        runLine[0].append(anteWords)
    for anteWords in qAnteLine[1]:
        runLine[1].append(anteWords)
    for lists in gF.superList[:-2]:  #  All the global lists except for 
        lists.append([])             #  qLineIndexList, proxDataIndexList
    print('lnF:', gF.lineno(), '| lineStarter() |', runLine)
    gF.proxFunk.proxDataBuilder(runLine, len(runLine[1]))
    print('lnF:', gF.lineno(), '| lineStarter() | firstWordgF.superPopList start')
    for all in gF.firstWords:
        if all not in gF.superBlackList[0]:
            if all in proxExpress:
                gF.expressList[0].append(all)
            else:
                gF.superPopList[0].append(all)
    print('lnF:', gF.lineno(), '| len(superPopList[0]):', len(gF.superPopList[0]), 'len(expressList[0]):', len(gF.expressList[0]))
    return runLine, ([],[])
          #runLine, qLine

def gov(empLine, rhymeThisLine, rhymeList, qAnteLine):
    print('liF:', gF.lineno(), '| gov() start', rhymeThisLine)
    qLine, pLEmps = veto()  #  Start with empty variables declared. This function is also a reset button if lines are to be scrapped.
    proxExpress = []
    if rhymeThisLine == True:
        print('liF:', gF.lineno(), '| gov() - len(rhymeList):', len(rhymeList))
        if (len(rhymeList) > 0):  #  This dictates whether stanzaGovernor sent a rhyming line. An empty line indicates metered-only, or else it would've been a nonzero population
            proxExpress = []
            for rhymers in rhymeList:  #  Find words that come before rhymeWords, so you direct it towards that one
                try:
                    for words in gF.proxMinusLista[:len(empLine)]:  #  Only go as far as the empLine, as if all words are one-syllable long
                        thisProxList = words[rhymers]
                        for proxWord in thisProxList:
                            if (proxWord not in proxExpress) and (proxWord not in quantumList):
                                proxExpress.append(proxWord)
                except KeyError:
                    continue
            print('liF:', gF.lineno(), '| gov() - len(proxExpress):', len(proxExpress))
            qLine, killSwitch = gF.rhymeFunk.gov(empLine, proxExpress, rhymeList, qAnteLine)
        else:
            print('liF:', gF.lineno(), '| gov() - no rhymes')
            return ([],[]), True  #  qLine, killSwitch
    elif gF.metSwitch == True:  #  If metSwitch is off, then we wouldn't have either rhyme or meter
        print('liF:', gF.lineno(), '| gov() - gF.meterFunk.gov activate')
        qLine, killSwitch = gF.meterFunk.gov(empLine, [], ([], []), qAnteLine, proxExpress)
                                              #  empLine, qLine, pLEmps, runLine, proxExpress
    else:
        print('liF:', gF.lineno(), '| gov() - plainLiner activate')
        qLine, killSwitch = plainLinerLtoR(empLine, qAnteLine)
    if killSwitch == True:
        print('liF:', gF.lineno(), 'gov() - killSwitch')
        qLine, pLEmps = veto()
        return qLine, True
    else:
        print('liF:', gF.lineno(), '| gov() - last else', qLine)
        return qLine, False  #  usedList, qLine, killSwitch
