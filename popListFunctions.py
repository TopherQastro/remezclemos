
import globalFunctions as gF

def superPopListMaker(empLine, proxExpress, qLine, runLine): #  Creates a list-of-lists to pull from
    print(gF.lineno(), 'sPLM init | len(gF.superPopList)', len(gF.superPopList))
    gF.printGlobalData(qLine)
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
    for mList in gF.superList[:-3]:  #  Everything except proxData, superBlackLIst
        mList.append([])
    print(gF.lineno(), 'superPopListMaker() | start', len(gF.superPopList), testLine, 
          'proxData:', gF.qLineIndexList, gF.proxDicIndexList)
    testLineLen = len(testLine[1])
    if testLineLen == 0:  #  If we've received a totally empty line, populate it with firstWords, but not directly or corrupt global bank
        print(gF.lineno(), 'superPopListMaker() | zeroLine')
        pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, qAnteLine)
        return qLine, runLine
              #gF.superPopList, etc
    print(gF.lineno(), 'superPopListMaker() | len(testLine) >= 1', gF.qLineIndexList, gF.proxDicIndexList)
    try:
        print(gF.lineno(), 'superPopListMaker() | this blackList:', qLine, len(gF.superBlackList))#[len(qLine[1])])
        pLEmps = gF.pEmpsLine(empLine, qLine[0])
        while len(gF.qLineIndexList[-1]) > 0:
            for all in gF.proxP1[testLine[1][-1]]:
                if (all not in gF.superBlackList[-1]) and (all != testLine[1][-1]):  #  Screen against the initial gF.superBlackList
                    keepList.append(all)  #  Practically an 'else' clause, because the 'if' above returns an answer
            #print(gF.lineno(), 'sPM - this keepList:', keepList)
            if len(gF.qLineIndexList[-1]) > 1:  #  Only keep going if we need more than 2 words analyzed
                for each in gF.proxDicIndexList[-1][1:]:  #  Skip first indexNum, we already found it
                    testList = gF.proxMinusLista[each][testLine[1][gF.qLineIndexList[-1][each]]]  #  Scans approximate words with indexes
                    burnList = []  #  burnList holds words that don't match with mutual proxLists
                    for all in keepList:
                        if (all not in testList) or (all in gF.superBlackList[-1]): #or (testString not in rawText):  #  Add blackList screening later
                            burnList.append(all)  #  Screen it with a burnList so we don't delete as we iterate thru list
                    print(gF.lineno(), 'superPopListMaker() | len(keepList):', len(keepList), 
                          'len(burnList):', len(burnList))
                    if len(keepList) > 0:
                        for all in burnList:
                            keepList.remove(all)
                    else:  #  If we run out prematurely, stop iterating over the list
                        print(gF.lineno(), 'superPopListMaker() | keepList out')
                        break
            if len(keepList) == 0:
                gF.qLineIndexList[-1].pop()
                gF.proxDicIndexList[-1].pop()
                print(gF.lineno(), 'superPopListMaker() | snipping proxData', 
                      gF.qLineIndexList[-1], gF.proxDicIndexList[-1])
                if len(gF.qLineIndexList[-1]) > 0:  #  Ensure that the line has something to check
                    if (len(gF.qLineIndexList[-1]) <= gF.proxMinDial):  #  This keeps the chain longer than a minimum length
                        pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
                        print(gF.lineno(), 'sPM out', gF.qLineIndexList[-1], 
                              gF.proxDicIndexList[-1])
                        break
            else:
                print(gF.lineno(), 'superPopListMaker() | grown', len(gF.superPopList), '|', testLine, 'proxData:', gF.qLineIndexList, gF.proxDicIndexList)
                for keepWords in keepList:
                    if keepWords in proxExpress and keepWords not in gF.expressList[-1] and keepWords not in quantumList:
                        gF.expressList[-1].append(keepWords)
                    elif all not in gF.superPopList[-1]:
                        gF.superPopList[-1].append(keepWords)
                break
        gF.printGlobalData(qLine)
        return qLine, runLine
    except KeyError:
        print(gF.lineno(), 'kE:', testLine, 'len(gF.superPopList):', len(gF.superPopList))
        unknownWords.write(qLine[1][-1])
        pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
        #gF.proxFunk.proxDataBuilder(qLine, len(qLine[0]))
        return qLine, runLine
    print(gF.lineno(), 'sPM lastfinish')
    gF.printGlobalData(qLine)
    return qLine, runLine


def plainPopDigester():  #  Digests words from list without regard to their syllables or meter
    return doo, doo


def empPopDigester():  #  Digests words based on the length of their syllables
    return doo, doo


