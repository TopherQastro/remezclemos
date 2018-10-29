
def vetoLine(qAnteLine, proxExpress):  #  Resets values in a line to
    print(lineno(), 'vetoLine() | qAnteLine:', qAnteLine)
    runLine = ([],[])
    for each in qAnteLine[0]:  #  Re-create any qAnteLinesuperPopList, qLine, qLineIndexList, proxDicIndexList as a mutable variable
        runLine[0].append(each)
    for each in qAnteLine[1]:  #  Re-create any qAnteLinesuperPopList, qLine, qLineIndexList, proxDicIndexList as a mutable variable
        runLine[1].append(each)
    global mList
    for mList in metaList:
        while len(mList) > 0:
            mList.pop()
    printGlobalData(([],[]))
    return ([],[]), runLine, False
          #qLine, qAnteLine, redButton

def removeWordL(superPopList, qLine):  #  Remove the leftmost word from line
    # do something
    return data


def removeWordR(empLine, qLine, runLine):  #  Remove the rightmost word from line
    print(lineno(), 'removeWordR-in', 'qLine:', qLine, 'runLine:', runLine)
    if len(qLine[0]) == 0 and len(runLine[0]) > 0:  #  Cut runLine
        print(lineno(), "rMR - if0")
        minusWordX = runLine[0].pop(0)  #  Since the previous line didn't yield any following line
        minusWordY = runLine[1].pop(0)  #  minusWordX just holds whatever is getting popped
    if len(qLine[0]) > 0:
        print(lineno(), "rMR - if1")
        minusWord0 = qLine[0].pop()  #  Remove word from first part of line
        minusWord1 = qLine[1].pop()  #  Until better method introduced, cut rLine here
        pWEmps = gF.empsLine(empLine, [minusWord0], emps, doubles, quantumList)
        pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)
        pLEmps = pLEmps[:-len(pWEmps)]  #  Cut emps from main line)
        superBlackList.pop()  #  If we leave blacklisted words further down the road, they may negate an otherwise compatible sentence
        print(lineno(), 'minusWord0:', minusWord0)
        superBlackList[-1].append(minusWord0)  #  Add to blackList at correct point
    else:
        pLEmps = []
    #if len(superPopList) > (len(qLine[1]) + 1):  #  If we've gone further than checking the list of next words
    print(lineno(), 'rMR - snipPopList')
    global mList
    for mList in metaList:
        if len(mList) > 0:
            mList.pop()
        elif len(qLine[1]) > 0:
            print(lineno(), qLine)
            printGlobalData(qLine)
    print(lineno(), 'removeWordR-out', qLine)
    printGlobalData(qLine)
    return pLEmps, qLine, runLine


def acceptWordL(qLine, nextWord, qLineIndexList, proxDicIndexList):  #  Add the rightmost word to line

##  INVERT THESE VALUES

    print('acceptWord:', qLine, '|', nextWord)
    pLine.append(nextWord)
    if len(proxNumList) > 0:
        proxNum = proxNumList[-1] + 1
    else:
        proxNum = 0
    proxNumList.append(proxNum)
    proxLineNum = proxLineNumList[0] + 1
    proxLineNumList.insert(0, proxLineNum)
    return qLineIndexList, proxDicIndexList, qLine


def acceptWordR(empLine, qLine, runLine, nextWord):  #  Add word to right side of line
    print('acceptWordR-in:', runLine, qLine, '|', nextWord)
    for each in nextWord[0]:
        qLine[0].append(each)
    for each in nextWord[1]:
        qLine[1].append(each)
    #proxDataBuilder(qLineIndexList, proxDicIndexList, qLine, len(qLine[1]))
    #if len(superBlackList) == len(qLine[1]):  #  We don't have any blackListed words that far ahead
    superBlackList.append([])
    qLineIndexList.append([])
    proxDicIndexList.append([])
    proxDataBuilder((runLine[0]+qLine[0], runLine[1]+qLine[1]), len(runLine[1]+qLine[1]))
    qLine, runLine = superPopListMaker(empLine, [], qLine, runLine)
    print('acceptWordR-out:', qLine, '|', nextWord, qLineIndexList, proxDicIndexList)
    return qLine


def lineGovernor(empLine, rhymeThisLine, rhymeList, qAnteLine):
    print(lineno(), 'lineGovernor start', rhymeThisLine)
    qLine, qAnteLine, redButton = vetoLine(qAnteLine, [])  #  Start with empty variables declared. This function is also a reset button if lines are to be scrapped.
    if rhymeThisLine == True:
        print(lineno(), 'len(rhymeList):', len(rhymeList))
        if (len(rhymeList) > 0):  #  This dictates whether stanzaGovernor sent a rhyming line. An empty line indicates metered-only, or else it would've been a nonzero population
            proxExpress = []
            for each in rhymeList:  #  Find words that come before rhymeWords, so you direct it towards that one
                try:
                    for all in proxMinusLista[:len(empLine)]:  #  Only go as far as the empLine, as if all words are one-syllable long
                        thisProxList = all[each]
                        for proxWord in thisProxList:
                            if proxWord not in proxExpress and proxWord not in quantumList:
                                proxExpress.append(proxWord)
                except KeyError:
                    continue
            print(lineno(), 'len(proxExpress):', len(proxExpress))
            qLine, redButton = rhymeLiner(empLine, proxExpress, rhymeList, qAnteLine)
        else:
            print(lineno(), 'no rhymes')
            return superBlackList, [], ([],[]), True  #  usedList, qLine, redButton
    elif metSwitch == True:  #  If metSwitch is off, then we wouldn't have either rhyme or meter
        print(lineno(), 'lineGov - meterLiner activate')
        qLine, redButton = meterLiner(empLine, [], qAnteLine)
    else:
        print(lineno(), 'lineGov - plainLiner activate')
        usedList, qLine, redButton = plainLinerLtoR(empLine, qAnteLine)
    if redButton == True:
        print(lineno(), 'lineGov - redButton')
        qLine, qAnteLine, redButton = vetoLine(qAnteLine, [])
        return qLine, True
    else:
        print(lineno(), 'lineGov - last else', qLine)
        return qLine, False  #  usedList, qLine, redButton