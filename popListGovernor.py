
def superPopListMaker(empLine, proxExpress, qLine, runLine): #  Creates a list-of-lists to pull from
    print(lineno(), 'sPLM init | len(superPopList)', len(superPopList))
    global qLineIndexList, proxDicIndexList
    printGlobalData(qLine)
    keepList = []  #  Will return empty set upon failure
    testLine = ([],[])
    if len(runLine[0]) > 0:  #  If there's a previous line, add it into testLine
        for each in runLine[0]:
            testLine[0].append(each)
        for each in runLine[1]:
            testLine[1].append(each)
    for each in qLine[0]:
        testLine[0].append(each)
    for each in qLine[1]:
        testLine[1].append(each)
    global mList
    for mList in metaList[:-2]:  #  Everything except proxData
        mList.append([])
    print(lineno(), 'superPopListMaker() | start', len(superPopList), testLine, 
          'proxData:', qLineIndexList, proxDicIndexList)
    testLineLen = len(testLine[1])
    if testLineLen == 0:  #  If we've received a totally empty line, populate it with firstWords, but not directly or corrupt global bank
        print(lineno(), 'superPopListMaker() | zeroLine')
        pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, qAnteLine)
        return qLine, runLine
              #superPopList, etc
    print(lineno(), 'superPopListMaker() | len(testLine) >= 1', qLineIndexList, proxDicIndexList)
    try:
        print(lineno(), 'superPopListMaker() | this blackList:', qLine, len(superBlackList))#[len(qLine[1])])
        pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)
        while len(qLineIndexList[-1]) > 0:
            for all in proxP1[testLine[1][-1]]:
                if (all not in superBlackList[-1]) and (all != testLine[1][-1]):  #  Screen against the initial superBlackList
                    keepList.append(all)  #  Practically an 'else' clause, because the 'if' above returns an answer
            #print(lineno(), 'sPM - this keepList:', keepList)
            if len(qLineIndexList[-1]) > 1:  #  Only keep going if we need more than 2 words analyzed
                for each in proxDicIndexList[-1][1:]:  #  Skip first indexNum, we already found it
                    testList = proxPlusLista[each][testLine[1][qLineIndexList[-1][each]]]  #  Scans approximate words with indexes
                    burnList = []  #  burnList holds words that don't match with mutual proxLists
                    for all in keepList:
                        if (all not in testList) or (all in superBlackList[-1]): #or (testString not in rawText):  #  Add blackList screening later
                            burnList.append(all)  #  Screen it with a burnList so we don't delete as we iterate thru list
                    print(lineno(), 'superPopListMaker() | len(keepList):', len(keepList), 
                          'len(burnList):', len(burnList))
                    if len(keepList) > 0:
                        for all in burnList:
                            keepList.remove(all)
                    else:  #  If we run out prematurely, stop iterating over the list
                        print(lineno(), 'superPopListMaker() | keepList out')
                        break
            if len(keepList) == 0:
                qLineIndexList[-1].pop()
                proxDicIndexList[-1].pop()
                print(lineno(), 'superPopListMaker() | snipping proxData', 
                      qLineIndexList[-1], proxDicIndexList[-1])
                if len(qLineIndexList[-1]) > 0:  #  Ensure that the line has something to check
                    if (len(qLineIndexList[-1]) <= proxMinDial):  #  This keeps the chain longer than a minimum length
                        pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
                        print(lineno(), 'sPM out', qLineIndexList[-1], 
                              proxDicIndexList[-1])
                        break
            else:
                print(lineno(), 'superPopListMaker() | grown', len(superPopList), '|', testLine, 'proxData:', qLineIndexList, proxDicIndexList)
                for keepWords in keepList:
                    if keepWords in proxExpress and keepWords not in expressList[-1] and keepWords not in quantumList:
                        expressList[-1].append(keepWords)
                    elif all not in superPopList[-1]:
                        superPopList[-1].append(keepWords)
                break
        printGlobalData(qLine)
        return qLine, runLine
    except KeyError:
        print(lineno(), 'kE:', testLine, 'len(superPopList):', len(superPopList))
        unknownWords.write(qLine[1][-1])
        pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
        #proxDataBuilder(qLine, len(qLine[0]))
        return qLine, runLine
    print(lineno(), 'sPM lastfinish')
    printGlobalData(qLine)
    return qLine, runLine


def plainPopDigester():  #  Digests words from list without regard to their syllables or meter
    return doo, doo


def empPopDigester():  #  Digests words based on the length of their syllables
    return doo, doo
