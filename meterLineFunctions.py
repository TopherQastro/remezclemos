
import globalFunctions as gF

def testEmpLine(empLine, qLine, runLine, qWord):  #  A subfunction of metPopDigester, which tests words given to it
    print('mLF:', gF.lineno(), ' | testEmpLine:', empLine, qLine, qWord)
    testLine = []  #  HitSwitch is a boolean that tells whether a word has been found
    for each in qLine[0]:
        testLine.append(each)
    for each in qWord[0]:
        testLine.append(each)   
    testEmps = gF.pEmpsLine(empLine, testLine)
    #gF.superBlackList[len(qLine[1])].append(pWord)  #  Add to blackList at correct point
    print('mLF:', gF.lineno(), ' | gF.superBlackListLen:', len(gF.superBlackList[len(qLine[1])]))
    if len(testEmps) <= len(empLine):  #  This is to screen against an error
        print('mLF:', gF.lineno(), ' | mPD testEmp0 |', qWord)
        if testEmps == empLine[:len(testEmps)]:  #  Check if the word is valid
            print('mLF:', gF.lineno(), ' | mPD testEmp pass')
            hitSwitch = True
            qLine = gF.lineFunk.acceptWordR(empLine, qLine, runLine, qWord)
            print('mLF:', gF.lineno(), ' | mPD acceptR', qLine, testEmps, gF.qLineIndexList, gF.proxDicIndexList)
            return testEmps, qLine, True
    return testEmps, qLine, False


def testExPopList(empLine, thisList, qLine, runLine):
    print('mLF:', gF.lineno(), ' | thisList:', len(thisList))
    testEmps = gF.pEmpsLine(empLine, qLine[0])
    while len(thisList) > 0:
        pWord = thisList.pop(gF.random.choice(range(0, len(thisList))))
        print('mLF:', gF.lineno(), ' | testExPop:', pWord)
        qWord = ([pWord], [pWord])  #  pWord is the same word unless the phonetic data doesn't match the 'real' data
        if (gF.contSwitch == True) and (pWord in gF.contractionList) and (pWord[:-2] != "'s") and (pWord[-1] != "'") and (pWord[:2] != ("o'" or "d'")):  #  This line will place contractions in a special list to be switched if nothing works
            gF.contList[-1].append(pWord)
        elif pWord in gF.allPunx:
            gF.punxList[-1].append(pWord)
        elif pWord not in gF.allPunx:  #  A zero-length emps value is an unrecognized word
            if (gF.thesSwitch == True) and (pWord not in gF.quantumList) and (pWord not in gF.thesList[-1]):
                gF.thesList[-1].append(pWord)
            gF.superBlackList[len(qLine[1])].append(pWord)  #  Make sure that it doesn't keep going thru the same words over and over
            print('mLF:', gF.lineno(), empLine, qLine, qWord)
            testEmps, qLine, hitSwitch = testEmpLine(empLine, qLine, runLine, qWord)
            if hitSwitch == True:
                return testEmps, qLine, runLine, True
    return testEmps, qLine, runLine, False


def metPopDigester(empLine, proxExpress, qLine, runLine):  #  Digests words that fit a particular meter
    print('mLF:', gF.lineno(), ' | mPD start | ', qLine, runLine)
    while len(gF.superPopList[-1]+gF.expressList[-1]+gF.thesList[-1]+gF.contList[-1]+gF.punxList[-1]) > 0:
        gF.printGlobalData(qLine)
        testEmps, qLine, runLine, passSwitch = testExPopList(empLine, proxExpress, qLine, runLine)
        if passSwitch == True:
            return testEmps, qLine, runLine
        for word in gF.superPopList[-1]:  #  If the first expressList is out, move non-quantum to front
            if word not in gF.quantumList:
                gF.expressList[-1].append(word)
        for word in gF.expressList[-1]:
            gF.superPopList[-1].pop(gF.superPopList[-1].index(word))
        testEmps, qLine, runLine, passSwitch = testExPopList(empLine, gF.superPopList[-1], qLine, runLine)
        if passSwitch == True:
            return testEmps, qLine, runLine
        print('mLF:', gF.lineno(), ' | gF.contSwitch:', gF.contSwitch)
        if (gF.contSwitch == True) and (len(gF.contList[-1]) > 0):  #  If any contractions were found in the gF.superPopList we just tried
            print('mLF:', gF.lineno(), ' |  |gF.contList[-1]:', gF.contList[-1])
            while len(gF.contList[-1]) > 0:
                pWord = gF.contList[-1].pop(gF.random.choice(range(0, len(gF.contList[-1]))))
                contWord = contractionDic[pWord]
                if len(contWord) == 0:  #  If there's no contraction, it's just a word with an apostrophe
                    contWord = pWord
                print('mLF:', gF.lineno(), ' |  |contWord:', contWord)
                qWord = (contWord, [pWord])  #  Appending two different words to the line
                print('mLF:', gF.lineno(), ' |  |contraction attempt:', qWord)
                testEmps, qLine, hitSwitch = testEmpLine(empLine, qLine, runLine, qWord)
                if hitSwitch == True:
                    return testEmps, qLine, runLine
        print('mLF:', gF.lineno(), ' |  |gF.thesSwitch:', gF.thesSwitch)
        if gF.thesSwitch == True:
            while len(gF.thesList[-1]) > 0:
                print('mLF:', gF.lineno(), ' |  |thesCheck | len(gF.thesList[-1]):', len(gF.thesList[-1]))
                thesWord = gF.thesList[-1].pop(gF.random.choice(range(0, len(gF.thesList[-1]))))
                try:
                    syns = thesDic[thesWord]
                except KeyError:
                    syns = []
                    print('mLF:', gF.lineno(), ' |  | kE:synWord')
                    continue
                print('mLF:', gF.lineno(), ' |  | syns:', syns)
                while len(syns) > 0:
                    synonym = syns.pop(gF.random.choice(range(0, len(syns))))
                    qWord = ([synonym], [thesWord])
                    print('mLF:', gF.lineno(), ' | thes qWord:', qWord)
                    testEmps, qLine, hitSwitch = testEmpLine(empLine, qLine, runLine, qWord)
                    if hitSwitch == True:
                        return testEmps, qLine, runLine
        if (len(qLine[1]) > 2):  #  We want qLine to have more than 2 words before trying punctuation because it sounds better, although it isn't necessary for function. Also, make sure to exhaust all other possibilities first
            print('mLF:', gF.lineno(), ' | punxSearch', qLine[1][-(min(gF.punxDial, len(qLine[1]))):])
            punxCt = int(0)
            for all in qLine[1][-(min(gF.punxDial, len(qLine[1]))):]:
                if all in gF.allPunx:  #  Will discriminate any puncuation within the designated length of gF.punxDial
                    print('mLF:', gF.lineno(), ' | found punk within gF.punxDial:', all)
                    punxCt+=1
            if (punxCt == 0) and (len(gF.punxList[-1]) > 0) and (qLine[1][-1] not in nonEnders):
                punxWord = gF.punxList[-1].pop(gF.random.choice(range(0, len(gF.punxList[-1]))))
                qWord = ([punxWord], [punxWord])
                qLine = gF.lineFunk.acceptWordR(empLine, qLine, runLine, qWord)
                print('mLF:', gF.lineno(), ' | punxD acceptR', qLine)
                testEmps = gF.pEmpsLine(empLine, qLine[0])                
                return testEmps, qLine, runLine
            else:
                while len(gF.punxList[-1]) > 0:  #  Clear punx
                    gF.punxList[-1].pop()
        else:
            while len(gF.punxList[-1]) > 0:  #  Clear punx
                gF.punxList[-1].pop()
        if len(qLine[1]) > 0:
            if (len(gF.qLineIndexList[-1]) > gF.proxMinDial) and (len(runLine[1]+qLine[1]) > gF.proxMinDial):
                print('mLF:', gF.lineno(), ' | snip qLineIndex in:', gF.qLineIndexList, 
                      gF.proxDicIndexList, runLine[1], qLine[1])
                gF.qLineIndexList[-1].pop()
                gF.proxDicIndexList[-1].pop()
                print('mLF:', gF.lineno(), ' | snip qLineIndex out:', 
                      gF.qLineIndexList, gF.proxDicIndexList)
                for eachList in gF.superList[:-2]:
                    eachList.pop()
                qLine, runLine = gF.popFunk.superPopListMaker(empLine, proxExpress, qLine, runLine)
            else: #and len(qLine[1]) > gF.proxMinDial:  #  If we have enough words, then we can remove rightmost element and metadata, then try again
                print('mLF:', gF.lineno(), ' | snipLine', qLine, '|', runLine, len(gF.superPopList))
                pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
    if (len(gF.superPopList[-1]+gF.expressList[-1]+gF.thesList[-1]+gF.contList[-1]+gF.punxList[-1]) == 0):
        pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
    pLEmps = gF.pEmpsLine(empLine, qLine[0])
    print('mLF:', gF.lineno(), ' | mPD end whilemain | pLEmps:', pLEmps, qLine)
    return pLEmps, qLine, runLine
              #pLEmps, qLine, qAnteLine    

def meterLinerStarter(empLine, proxExpress, qAnteLine):  #  Starts the values for the lineMakers
    print('mLF:', gF.lineno(), ' | meterLinerStarter() | start')
    qLine, qAnteLine, pLEmps, killSwitch = gF.lineFunk.veto(qAnteLine, [])
    runLine = ([], [])
    for each in qAnteLine[0]:  #  qAnteLine gets appended to runLine because this function will be cutting from it when it doesn't yield results
        runLine[0].append(each)
    for each in qAnteLine[1]:
        runLine[1].append(each)
    for someLists in gF.superList[:-2]:  #  All the global lists except for 
                                         #  superBlackList, qLineIndexList, proxDataIndexList
        someLists.append([])
    if len(runLine[1]) > 0:  #  Checks before trying to manipulate runLine just below, also loops it so it subtracts from anteLine first
        print('mLF:', gF.lineno(), ' | meterLinerStarter() | firstWordMet if')
        gF.qLineIndexList.append([])
        gF.proxDicIndexList.append([])
        gF.proxFunk.proxDataBuilder(runLine, len(runLine[1]))
        qLine, runLine = gF.popFunk.superPopListMaker(empLine, proxExpress, qLine, runLine)
    else:
        print('mLF:', gF.lineno(), ' | meterLinerStarter() | firstWordgF.superPopList start')
        for all in gF.firstWords:
            if all not in gF.superBlackList[0]:
                if all in proxExpress:
                    gF.expressList[0].append(all)
                else:
                    gF.superPopList[0].append(all)
    pLEmps, qLine, runLine = metPopDigester(empLine, proxExpress, qLine, runLine)    
    return pLEmps, qLine, runLine

def meterLiner(empLine, proxExpress, qAnteLine):  #
    print('mLF:', gF.lineno(), ' | meterLiner() | start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, qAnteLine)
    while (pLEmps != empLine) or (qLine[0][-1] in nonEnders):  #  Keep going until the line is finished or returns blank answer
        qLine, killSwitch = meterGovernor(empLine, proxExpress, pLEmps, qLine, runLine)
        if killSwitch == True:
            return qLine, killSwitch
        if pLEmps == empLine:
            print('mLF:', gF.lineno(), ' | meterLiner() | pLEmps == empLine | gF.superPopList:',
                  len(gF.superPopList), len(gF.superPopList[-1]))
            if qLine[1][-1] in nonEnders:  #  Words that don't sound good as the last word of a line, such as conjunctions without something else to connect
                pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
            else:
                for all in gF.allPunx:
                    if all in gF.superPopList[-1]:  #  If puncuation fits, place one on the end of a line (will give the next line an easier start, too)
                        qLine = gF.lineFunk.acceptWordR(empLine, qLine, runLine, ([all], [all]))
                        break
        if killSwitch == True:
            return qLine, killSwitch
    print('mLF:', gF.lineno(), ' | meterLiner() | out:', qLine, 'len(gF.superPopList):', len(gF.superPopList), 'killSwitch:', killSwitch)
    return qLine, killSwitch
          #qLine, killSwitch
            

def rhymeLiner(empLine, proxExpress, rhymeList, qAnteLine):
    print('mLF:', gF.lineno(), ' | rhymeLiner() | start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, qAnteLine)
    if len(qLine[1]) == 0:
        return qLine, True
    while (qLine[0][-1] not in rhymeList) or (qLine[0][-1] in nonEnders) or (pLEmps != empLine):
        qLine, killSwitch = meterGovernor(empLine, proxExpress, pLEmps, qLine, runLine)
        if killSwitch == True:
            return qLine, killSwitch
        if pLEmps == empLine:
            print('mLF:', gF.lineno(), ' | rhymeLiner() | pLEmps == empLine | qLine[0]:', qLine[0])
            if (qLine[0][-1] in gF.allPunx):
                pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
            if (qLine[0][-1] in nonEnders) or (qLine[0][-1] not in rhymeList):  #  Words that don't sound good as the last word of a line, such as conjunctions without something else to connect
                pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
                qLine, killSwitch = meterGovernor(empLine, rhymeList, pLEmps, qLine, runLine)  #  Switch proxExpress to rhymeList to get them preferred
            else:
                for punc in gF.allPunx:
                    if punc in gF.superPopList[-1]:  #  If puncuation fits, place one on the end of a line (will give the next line an easier start, too)
                        qLine = gF.lineFunk.acceptWordR(empLine, qLine, runLine, ([punc], [punc]))
                        return qLine, killSwitch
        if killSwitch == True:
            return qLine, killSwitch
    print('mLF:', gF.lineno(), ' | rhymeLiner() | out:', qLine, 'len(gF.superPopList):', len(gF.superPopList), 'killSwitch:', killSwitch)
    if killSwitch == True:
        return qLine, killSwitch
    print('mLF:', gF.lineno(), ' | rhymeLiner() | rhyHere1:', qLine)
    return qLine, killSwitch

    
def gov(empLine, qLine, pLEmps, runLine, proxExpress):
    print('mLF:', gF.lineno(), ' | meterGovernor() | runLine:', runLine, '| qLine:', qLine)
    gF.stopTime = gF.time.time()
    if gF.stopTime > (gF.startTime + 300):
        qLine, runLine, pLEmps, killSwitch = gF.lineFunk.veto(runLine, [])
        gF.startTime = gF.time.time()
        print('mLF:', gF.lineno(), ' | meterGovernor() | timeout restart |', str(gF.time.ctime())[11:20])
        return qLine, True  
    while pLEmps != empLine:
        print('mLF:', gF.lineno(), ' | meterGovernor() | metGov while start')
        if len(qLine[1]) == 0:  #  Check if we're starting with a completely empty line, load firstWords to gF.superPopList if so
            print('mLF:', gF.lineno(), ' | meterGovernor() | meterGov if0')
            pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, runLine) 
        elif len(qLine[1]) > 0:
            print('mLF:', gF.lineno(), ' | meterGovernor() | meterGov if2 qLine:', qLine, 'len(gF.superBlackList):', 
                  len(gF.superBlackList), 'meterGovernor() | len(gF.superPopList):', len(gF.superPopList))
            if len(qLine[1]) == len(gF.superPopList):
                qLine, runLine = gF.popListFunk.gF.popFunk.superPopListMaker(empLine, proxExpress, qLine, runLine)                
            pLEmps, qLine, runLine = metPopDigester(empLine, proxExpress, qLine, runLine)
        elif len(runLine[0]) == 1 and runLine[-1] in gF.endPunx:                
            print('mLF:', gF.lineno(), ' | meterGovernor() |  if3', runLine)
            pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, ([], []))
        try:  
            if len(gF.superPopList) == 0 and len(qLine[1]) == 0 and len(runLine[0]) == 0:
                print('mLF:', gF.lineno(), ' | meterGovernor() | killSwitch == True')
                return qLine, True #  killSwitch event
        except IndexError:  #  Either the lists are empty, or they don't exist at all
            print('mLF:', gF.lineno(), ' | meterGovernor() | iE:', qLine, runLine)
            gF.printGlobalData(qLine)
            return pLEmps, qLine, True #  killSwitch event
        print('mLF:', gF.lineno(), ' | meterGovernor() | end of meterGov ifchecks')
        while len(pLEmps) > len(empLine):  #  If somehow the line went over the numbered lists
            print('mLF:', gF.lineno(), ' | meterGovernor() | meterGov over emps')
            pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
    return qLine, False    