
import globalFunctions as gF

def veto():  #  Resets values in a line to
    print('lnF:', gF.lineno(), '| veto()')
    listInt = int(0)
    for lists in gF.superList:
        #print('lnF:', gF.lineno(), listInt, lists)
        while len(lists) > 0:
            lists.pop()
        #print('lnF:', gF.lineno(), listInt, lists)
        listInt+=1
    gF.printGlobalData([[],[]])
    return ([],[]), []
          #qLine, pLEmps
          

def removeWordL(superPopList, qLine):  #  Remove the leftmost word from line
    # do something
    return data


def removeWordR(empLine, qLine, runLine):  #  Remove the rightmost word from line
    print('lnF:', gF.lineno(), '| removeWordR-in', 'qLine:', qLine, 'runLine:', runLine)
    if len(qLine[0]) == 0 and len(runLine[0]) > 0:  #  Cut runLine
        print('lnF:', gF.lineno(), "| rMR - if0")
        minusWordX = runLine[0].pop(0)  #  Since the previous line didn't yield any following line
        minusWordY = runLine[1].pop(0)  #  minusWordX just holds whatever is getting popped
    if len(qLine[0]) > 0:
        print('lnF:', gF.lineno(), "| rMR - if1")
        minusWord0 = qLine[0].pop()  #  Remove word from first part of line
        minusWord1 = qLine[1].pop()  #  Until better method introduced, cut rLine here
        pWEmps = gF.pEmpsLine(empLine, [minusWord0])
        pLEmps = gF.pEmpsLine(empLine, qLine[0])
        print('lnF:', gF.lineno(), qLine, pLEmps, pWEmps)
        pLEmps = pLEmps[:-len(pWEmps)]  #  Cut emps from main line)
        print('lnF:', gF.lineno(), '| len(superBlackList):', len(gF.superBlackList))
        print('lnF:', gF.lineno(), '| minusWord0:', minusWord0)
        gF.superBlackList.append([])  #  Add one to remove, because this was easiest in code
        for lists in gF.superList:
            if len(lists) > 0:
                lists.pop()
            elif len(qLine[1]) > 0:
                print('lnF:', gF.lineno(), '| qLine:', qLine)
        try:  #  This 'try' setup shouldn't be part of the program, just the next line
            if len(gF.superBlackList) > (len(gF.expressList) + 1):
                gF.superBlackList.pop()
            else:
                gF.superBlackList[-1].append(minusWord0)  #  Add to blackList at correct point
        except IndexError:  #  Investigate why an IndexError occurred. It's not supposed to.
            print('lnF:', gF.lineno(), '| superBlackList IndexError:\n', 
                  'len(superBlackList):', len(gF.superBlackList),
                  gF.superBlackList)
            input('paused...')
        gF.printGlobalData(qLine)
    else:
        pLEmps = []
    #if len(gF.superPopList) > (len(qLine[1]) + 1):  #  If we've gone further than checking the list of next words
    print('lnF:', gF.lineno(), '| removeWordR() out - qLine:', qLine)
    gF.printGlobalData(qLine)
    return pLEmps, qLine, runLine


def acceptWordL(qLine, nextWord):  #  Add the rightmost word to line

##  INVERT THESE VALUES

    print('lnF:', gF.lineno(), '| acceptWord:', qLine, '-', nextWord)
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
    print('lnF:', gF.lineno(), '| acceptWordR-in:', qLine, '|', nextWord, 'runLine:', runLine)
    qLine[0].append(nextWord[0])
    qLine[1].append(nextWord[1])
    print('lnF:', gF.lineno(), qLine)
    #gF.proxFunk.proxDataBuilder(gF.qLineIndexList, proxDicIndexList, qLine, len(qLine[1]))
    #if len(gF.superBlackList) == len(qLine[1]):  #  We don't have any blackListed words that far ahead
    print('lnF:', gF.lineno(), '| acceptWordR - adding superList items')
    gF.printGlobalData(qLine)
    for lists in gF.superList:
        lists.append([])
    gF.printGlobalData(qLine)
    print('lnF:', gF.lineno(), qLine, (runLine[0]+qLine[0], runLine[1]+qLine[1]))
    gF.proxFunk.proxDataBuilder((runLine[0]+qLine[0], runLine[1]+qLine[1]), len(runLine[1]+qLine[1]))
    print('lnF:', gF.lineno(), qLine)
    pLEmps = gF.pEmpsLine(empLine, qLine[0])
    qLine, runLine, killSwitch = gF.popFunk.superPopListMaker(empLine, pLEmps, [], qLine, runLine)
    print('lnF:', gF.lineno(), qLine)
    print('lnF:', gF.lineno(), '| acceptWordR-out:', qLine, '|', nextWord, gF.qLineIndexList, gF.proxDicIndexList)
    return qLine, killSwitch


def lineStarter(qAnteLine, proxExpress):  #  Starts the values for the lineMakers
    print('lnF:', gF.lineno(), '| lineStarter() start')
    runLine = ([],[])
    for anteWords in qAnteLine[0]:  #  qAnteLine gets appended to runLine because this function will be cutting from it when it doesn't yield results
        runLine[0].append(anteWords)
    for anteWords in qAnteLine[1]:
        runLine[1].append(anteWords)
    gF.printGlobalData(([],[]))
    print('lnF:', gF.lineno(), '| superList:', gF.superList,
                                 '\nlen(thesList):', len(gF.thesList),
                                 '\nlen(contList):', len(gF.contList),
                                 '\nlen(superBlackList):', len(gF.superBlackList), 
                                 '\nlen(qLineIndexList):', len(gF.qLineIndexList), 
                                 '\nlen(proxDicIndexList):', len(gF.proxDicIndexList))
    for lists in gF.superList:  #  All the global lists except for 
        lists.append([])             #  qLineIndexList, proxDataIndexList
    gF.printGlobalData(([],[]))
    print('lnF:', gF.lineno(), '| superList:', gF.superList,
                                 '\nlen(thesList):', len(gF.thesList),
                                 '\nlen(contList):', len(gF.contList),
                                 '\nlen(superBlackList):', len(gF.superBlackList), 
                                 '\nlen(qLineIndexList):', len(gF.qLineIndexList), 
                                 '\nlen(proxDicIndexList):', len(gF.proxDicIndexList))
    print('lnF:', gF.lineno(), '| lineStarter() - runLine:', runLine)
    gF.superBlackList.append([])
    print(len(gF.superBlackList))
    gF.proxFunk.proxDataBuilder(runLine, len(runLine[1]))
    print('lnF:', gF.lineno(), '| lineStarter() - firstWord start')
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
    print('lnF:', gF.lineno(), '| gov() start', rhymeThisLine)
    qLine, pLEmps = veto()  #  Start with empty variables declared. This function is also a reset button if lines are to be scrapped.
    proxExpress = []
    if rhymeThisLine == True:
        print('lnF:', gF.lineno(), '| gov() - len(rhymeList):', len(rhymeList))
        if (len(rhymeList) > 0):  #  This dictates whether stanzaGovernor sent a rhyming line. An empty line indicates metered-only, or else it would've been a nonzero population
            proxExpress = []
            for rhymers in rhymeList:  #  Find words that come before rhymeWords, so you direct it towards that one
                try:
                    for words in gF.proxMinusLista[:len(empLine)]:  #  Only go as far as the empLine, as if all words are one-syllable long
                        thisProxList = words[rhymers]
                        for proxWord in thisProxList:
                            if (proxWord not in proxExpress) and (proxWord not in gF.quantumList):
                                proxExpress.append(proxWord)
                except KeyError:
                    continue
            print('lnF:', gF.lineno(), '| gov() - len(proxExpress):', len(proxExpress))
            qLine, killSwitch = gF.rhyFunk.rhymeLiner(empLine, proxExpress, qAnteLine, rhymeList)
        else:
            print('lnF:', gF.lineno(), '| gov() - no rhymes')
            return ([],[]), True  #  qLine, killSwitch
    elif gF.metSwitch == True:  #  If metSwitch is off, then we wouldn't have either rhyme or meter
        print('lnF:', gF.lineno(), '| gov() - gF.meterFunk.gov activate')
        qLine, killSwitch = gF.meterFunk.gov(empLine, [], ([], []), qAnteLine, proxExpress)
                                              #  empLine, qLine, pLEmps, runLine, proxExpress
    else:
        print('lnF:', gF.lineno(), '| gov() - plainLiner activate')
        qLine, killSwitch = plainLinerLtoR(empLine, qAnteLine)
    if killSwitch == True:
        print('lnF:', gF.lineno(), 'gov() - killSwitch')
        qLine, pLEmps = veto()
        return qLine, True
    else:
        print('lnF:', gF.lineno(), '| gov() - last else', qLine)
        return qLine, False  #  usedList, qLine, killSwitch
