
import globalFunctions as gF

def testEmpLine(empLine, qLine, runLine, qWord):  #  A subfunction of metPopDigester, which tests words given to it
    print(gF.lineno(), 'testEmpLine:', empLine, qLine, qWord)
    testLine = []  #  HitSwitch is a boolean that tells whether a word has been found
    for each in qLine[0]:
        testLine.append(each)
    for each in qWord[0]:
        testLine.append(each)   
    testEmps = gF.empsLine(empLine, testLine, emps, doubles)
    #superBlackList[len(qLine[1])].append(pWord)  #  Add to blackList at correct point
    print(gF.lineno(), 'superBlackListLen:', len(superBlackList[len(qLine[1])]))
    if len(testEmps) <= len(empLine):  #  This is to screen against an error
        print(gF.lineno(), 'mPD testEmp0 |', qWord)
        if testEmps == empLine[:len(testEmps)]:  #  Check if the word is valid
            print(gF.lineno(), 'mPD testEmp pass')
            hitSwitch = True
            qLine = acceptWordR(empLine, qLine, runLine, qWord)
            print(gF.lineno(), 'mPD acceptR', qLine, testEmps, qLineIndexList, proxDicIndexList)
            return testEmps, qLine, True
    return testEmps, qLine, False


def testExPopList(empLine, thisList, qLine, runLine):
    print(gF.lineno(), 'thisList:', len(thisList))
    testEmps = gF.empsLine(empLine, qLine[0], emps)
    while len(thisList) > 0:
        pWord = thisList.pop(random.choice(range(0, len(thisList))))
        print(gF.lineno(), 'testExPop:', pWord)
        qWord = ([pWord], [pWord])  #  pWord is the same word unless the phonetic data doesn't match the 'real' data
        if (contSwitch == True) and (pWord in contractionList) and (pWord[:-2] != "'s") and (pWord[-1] != "'") and (pWord[:2] != ("o'" or "d'")):  #  This line will place contractions in a special list to be switched if nothing works
            contList[-1].append(pWord)
        elif pWord in allPunx:
            punxList[-1].append(pWord)
        elif pWord not in allPunx:  #  A zero-length emps value is an unrecognized word
            if (thesSwitch == True) and (pWord not in quantumList) and (pWord not in thesList[-1]):
                thesList[-1].append(pWord)
            superBlackList[len(qLine[1])].append(pWord)  #  Make sure that it doesn't keep going thru the same words over and over
            print(gF.lineno(), empLine, qLine, qWord)
            testEmps, qLine, hitSwitch = testEmpLine(empLine, qLine, runLine, qWord)
            if hitSwitch == True:
                return testEmps, qLine, runLine, True
    return testEmps, qLine, runLine, False


def metPopDigester(empLine, proxExpress, qLine, runLine):  #  Digests words that fit a particular meter
    print(gF.lineno(), 'mPD start | ', qLine, runLine)
    global metaList, qLineIndexList, proxDicIndexList
    while len(superPopList[-1]+expressList[-1]+thesList[-1]+contList[-1]+punxList[-1]) > 0:
        printGlobalData(qLine)
        testEmps, qLine, runLine, passSwitch = testExPopList(empLine, expressList[-1], qLine, runLine)
        if passSwitch == True:
            return testEmps, qLine, runLine
        for word in superPopList[-1]:  #  If the first expressList is out, move non-quantum to front
            if word not in quantumList:
                expressList[-1].append(word)
        for word in expressList[-1]:
            superPopList[-1].pop(superPopList[-1].index(word))
        testEmps, qLine, runLine, passSwitch = testExPopList(empLine, superPopList[-1], qLine, runLine)
        if passSwitch == True:
            return testEmps, qLine, runLine
        print(gF.lineno(), 'contSwitch:', contSwitch)
        if (contSwitch == True) and (len(contList[-1]) > 0):  #  If any contractions were found in the superPopList we just tried
            print(gF.lineno(), 'contList[-1]:', contList[-1])
            while len(contList[-1]) > 0:
                pWord = contList[-1].pop(random.choice(range(0, len(contList[-1]))))
                contWord = contractionDic[pWord]
                if len(contWord) == 0:  #  If there's no contraction, it's just a word with an apostrophe
                    contWord = pWord
                print(gF.lineno(), 'contWord:', contWord)
                qWord = (contWord, [pWord])  #  Appending two different words to the line
                print(gF.lineno(), 'contraction attempt:', qWord)
                testEmps, qLine, hitSwitch = testEmpLine(empLine, qLine, runLine, qWord)
                if hitSwitch == True:
                    return testEmps, qLine, runLine
        print(gF.lineno(), 'thesSwitch:', thesSwitch)
        if thesSwitch == True:
            while len(thesList[-1]) > 0:
                print(gF.lineno(), 'thesCheck | len(thesList[-1]):', len(thesList[-1]))
                thesWord = thesList[-1].pop(random.choice(range(0, len(thesList[-1]))))
                try:
                    syns = thesDic[thesWord]
                except KeyError:
                    syns = []
                    print(gF.lineno(), 'kE:synWord')
                    continue
                print(gF.lineno(), 'syns:', syns)
                while len(syns) > 0:
                    synonym = syns.pop(random.choice(range(0, len(syns))))
                    qWord = ([synonym], [thesWord])
                    print(gF.lineno(), 'thes qWord:', qWord)
                    testEmps, qLine, hitSwitch = testEmpLine(empLine, qLine, runLine, qWord)
                    if hitSwitch == True:
                        return testEmps, qLine, runLine
        if (len(qLine[1]) > 2):  #  We want qLine to have more than 2 words before trying punctuation because it sounds better, although it isn't necessary for function. Also, make sure to exhaust all other possibilities first
            print(gF.lineno(), 'punxSearch', qLine[1][-(min(punxProxNum, len(qLine[1]))):])
            punxCt = int(0)
            for all in qLine[1][-(min(punxProxNum, len(qLine[1]))):]:
                if all in allPunx:  #  Will discriminate any puncuation within the designated length of punxProxNum
                    print(gF.lineno(), 'found punk within punxProxNum:', all)
                    punxCt+=1
            if (punxCt == 0) and (len(punxList[-1]) > 0) and (qLine[1][-1] not in nonEnders):
                punxWord = punxList[-1].pop(random.choice(range(0, len(punxList[-1]))))
                qWord = ([punxWord], [punxWord])
                qLine = acceptWordR(empLine, qLine, runLine, qWord)
                print(gF.lineno(), 'punxD acceptR', qLine)
                testEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)                
                return testEmps, qLine, runLine
            else:
                while len(punxList[-1]) > 0:  #  Clear punx
                    punxList[-1].pop()
        else:
            while len(punxList[-1]) > 0:  #  Clear punx
                punxList[-1].pop()
        if len(qLine[1]) > 0:
            if (len(qLineIndexList[-1]) > proxMinDial) and (len(runLine[1]+qLine[1]) > proxMinDial):
                print(gF.lineno(), 'snip qLineIndex in:', qLineIndexList, proxDicIndexList, runLine[1], qLine[1])
                qLineIndexList[-1].pop()
                proxDicIndexList[-1].pop()
                print(gF.lineno(), 'snip qLineIndex out:', qLineIndexList, proxDicIndexList)
                global eachList
                for eachList in metaList[:-2]:
                    eachList.pop()
                qLine, runLine = superPopListMaker(empLine, proxExpress, qLine, runLine)
            else: #and len(qLine[1]) > proxMinDial:  #  If we have enough words, then we can remove rightmost element and metadata, then try again
                print(gF.lineno(), 'snipLine', qLine, '|', runLine, len(superPopList))
                pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
    if (len(superPopList[-1]+expressList[-1]+thesList[-1]+contList[-1]+punxList[-1]) == 0):
        pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
    pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)
    print(gF.lineno(), 'mPD end whilemain | pLEmps:', pLEmps, qLine)
    return pLEmps, qLine, runLine
              #pLEmps, qLine, qAnteLine    

def meterLinerStarter(empLine, proxExpress, qAnteLine):  #  Starts the values for the lineMakers
    print(gF.lineno(), 'meterLinerStarter() | start')
    qLine, qAnteLine, killSwitch = vetoLine(qAnteLine, [])
    runLine = ([], [])
    for each in qAnteLine[0]:  #  qAnteLine gets appended to runLine because this function will be cutting from it when it doesn't yield results
        runLine[0].append(each)
    for each in qAnteLine[1]:
        runLine[1].append(each)
    global mList
    for mList in metaList[:-2]:  #  All the global lists except for qLineIndexList, proxDataIndexList
        mList.append([])
    global qLineIndexList, proxDataBuilder
    if len(runLine[1]) > 0:  #  Checks before trying to manipulate runLine just below, also loops it so it subtracts from anteLine first
        print(gF.lineno(), 'meterLinerStarter() | firstWordMet if')
        qLineIndexList.append([])
        proxDicIndexList.append([])
        proxDataBuilder(runLine, len(runLine[1]))
        qLine, runLine = superPopListMaker(empLine, proxExpress, qLine, runLine)
    else:
        print(gF.lineno(), 'meterLinerStarter() | firstWordSuperPopList start')
        for all in firstWords:
            if all not in superBlackList[0]:
                if all in proxExpress:
                    expressList[0].append(all)
                else:
                    superPopList[0].append(all)
    pLEmps, qLine, runLine = metPopDigester(empLine, proxExpress, qLine, runLine)    
    return pLEmps, qLine, runLine

def meterLiner(empLine, proxExpress, qAnteLine):  #
    print(gF.lineno(), 'meterLiner() | start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, qAnteLine)
    while (pLEmps != empLine) or (qLine[0][-1] in nonEnders):  #  Keep going until the line is finished or returns blank answer
        pLEmps, qLine, runLine, killSwitch = meterGovernor(empLine, proxExpress, pLEmps, qLine, runLine)
        if killSwitch == True:
            return qLine, killSwitch
        if pLEmps == empLine:
            print(gF.lineno(), 'meterLiner() | pLEmps == empLine | superPopList:',
                  len(superPopList), len(superPopList[-1]))
            if qLine[1][-1] in nonEnders:  #  Words that don't sound good as the last word of a line, such as conjunctions without something else to connect
                pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
            else:
                for all in allPunx:
                    if all in superPopList[-1]:  #  If puncuation fits, place one on the end of a line (will give the next line an easier start, too)
                        qLine = acceptWordR(empLine, qLine, runLine, ([all], [all]))
                        break
        if killSwitch == True:
            return qLine, killSwitch
    print(gF.lineno(), 'meterLiner() | out:', qLine, 'len(superPopList):', len(superPopList), 'killSwitch:', killSwitch)
    return qLine, killSwitch
          #qLine, killSwitch
            

def rhymeLiner(empLine, proxExpress, rhymeList, qAnteLine):
    print(gF.lineno(), 'rhymeLiner() | start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, qAnteLine)
    if len(qLine[1]) == 0:
        return qLine, True
    while (qLine[0][-1] not in rhymeList) or (qLine[0][-1] in nonEnders) or (pLEmps != empLine):
        pLEmps, qLine, runLine, killSwitch = meterGovernor(empLine, proxExpress, pLEmps, qLine, runLine)
        if killSwitch == True:
            return qLine, killSwitch
        if pLEmps == empLine:
            print(gF.lineno(), 'rhymeLiner() | pLEmps == empLine | qLine[0]:', qLine[0])
            if (qLine[0][-1] in allPunx):
                pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
            if (qLine[0][-1] in nonEnders) or (qLine[0][-1] not in rhymeList):  #  Words that don't sound good as the last word of a line, such as conjunctions without something else to connect
                pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
                pLEmps, qLine, runLine, killSwitch = meterGovernor(empLine, rhymeList, pLEmps, qLine, runLine)  #  Switch proxExpress to rhymeList to get them preferred
            else:
                for punc in allPunx:
                    if punc in superPopList[-1]:  #  If puncuation fits, place one on the end of a line (will give the next line an easier start, too)
                        qLine = acceptWordR(empLine, qLine, runLine, ([punc], [punc]))
                        return qLine, killSwitch
        if killSwitch == True:
            return qLine, killSwitch
    print(gF.lineno(), 'rhymeLiner() | out:', qLine, 'len(superPopList):', len(superPopList), 'killSwitch:', killSwitch)
    if killSwitch == True:
        return qLine, killSwitch
    print(gF.lineno(), 'rhymeLiner() | rhyHere1:', qLine)
    return qLine, killSwitch

    
def gov(empLine, proxExpress, pLEmps, qLine, runLine):
    print(gF.lineno(), 'meterGovernor() | runLine:', runLine, '| qLine:', qLine)
    stopTime = time.time()
    if stopTime > (startTime + 300):
        qLine, runLine, killSwitch = sBG.lineFunk.veto(runLine, [])
        startTime = time.time()
        print(gF.lineno(), 'meterGovernor() | timeout restart |', str(time.ctime())[11:20])
        return pLEmps, qLine, runLine, True  
    while pLEmps != empLine:
        print(gF.lineno(), 'meterGovernor() | metGov while start')
        if len(qLine[1]) == 0:  #  Check if we're starting with a completely empty line, load firstWords to superPopList if so
            print(gF.lineno(), 'meterGovernor() | meterGov if0')
            pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, runLine) 
        elif len(qLine[1]) > 0:
            print(gF.lineno(), 'meterGovernor() | meterGov if2 qLine:', qLine, 'len(superBlackList):', 
                  len(superBlackList), 'meterGovernor() | len(superPopList):', len(superPopList))
            if len(qLine[1]) == len(superPopList):
                qLine, runLine = sBG.popListFunksuperPopListMaker(empLine, proxExpress, qLine, runLine)                
            pLEmps, qLine, runLine = metPopDigester(empLine, proxExpress, qLine, runLine)
        elif len(runLine[0]) == 1 and runLine[-1] in endPunx:                
            print(gF.lineno(), 'meterGovernor() |  if3', runLine)
            pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, ([], []))
        try:  
            if len(superPopList) == 0 and len(qLine[1]) == 0 and len(runLine[0]) == 0:
                print(gF.lineno(), 'meterGovernor() | killSwitch == True')
                return pLEmps, qLine, runLine, True #  killSwitch event
        except IndexError:  #  Either the lists are empty, or they don't exist at all
            print(gF.lineno(), 'meterGovernor() | iE:', qLine, runLine)
            printGlobalData(qLine)
            return pLEmps, qLine, runLine, True #  killSwitch event
        print(gF.lineno(), 'meterGovernor() | end of meterGov ifchecks')
        while len(pLEmps) > len(empLine):  #  If somehow the line went over the numbered lists
            print(gF.lineno(), 'meterGovernor() | meterGov over emps')
            pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
    return pLEmps, qLine, runLine, False    