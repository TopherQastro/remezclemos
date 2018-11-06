
import globalFunctions as gF


def testMeterWord(empLine, qLine, qWord):  #  A subfunction of metPopDigester, which tests words given to it
    print('mLF:', gF.lineno(), '| testEmpLine:', empLine, qLine, qWord)
    testLine = []  #  HitSwitch is a boolean that tells whether a word has been found
    for pWords in qLine[0]:
        testLine.append(pWords)
    testLine.append(qWord[0])
    print('mLF:', gF.lineno(), '|\ntestLine:', testLine, '\nempLine:', empLine)
    testEmps = gF.pEmpsLine(empLine, testLine)
    #gF.superBlackList[len(qLine[1])].append(pWord)  #  Add to blackList at correct point
    print('mLF:', gF.lineno(), '| gF.superBlackListLen:', len(gF.superBlackList[len(qLine[1])]))
    print('mLF:', gF.lineno(), '|\ntestEmps:', testEmps, '\nempLine:', empLine)
    if len(testEmps) <= len(empLine):  #  This is to screen against an error
        print('mLF:', gF.lineno(), '| mPD testEmp0 |', qWord)
        if testEmps == empLine[:len(testEmps)]:  #  Check if the word is valid
            print('mLF:', gF.lineno(), '| mPD testEmp pass')
            return True
    return False
       

def gov(empLine, pLEmps, qLine, qAnteLine, proxExpress):
    print('mLF:', gF.lineno(), '| gov() | qAnteLine:', qAnteLine, '| qLine:', qLine)
    gF.stopTime = gF.time.time()
    if gF.stopTime > (gF.startTime + 300):
        qLine, runLine, pLEmps, killSwitch = gF.lineFunk.veto(qAnteLine, [])
        gF.startTime = gF.time.time()
        print('mLF:', gF.lineno(), '| gov() - timeout restart:', str(gF.time.ctime())[11:20])
        return qLine, True
    runLine = ([],[])
    while pLEmps != empLine:
        print('mLF:', gF.lineno(), '| gov() while0 start', qLine, pLEmps)
        pLEmps = gF.pEmpsLine(empLine, qLine[0])
        print('mLF:', gF.lineno(), '| gov() - pLEmps check:', pLEmps)
        result = False
        if len(gF.superPopList) == 0:  #  Check if we're starting with a completely empty line, load firstWords to gF.superPopList if so
            print('mLF:', gF.lineno(), '| gov() - meterGov if0')
            runLine, qLine = gF.lineFunk.lineStarter(qAnteLine, proxExpress)
        print('mLF:', gF.lineno(), '| runLine:', runLine)
        popWord = gF.popFunk.popWordPicker(qLine)
        print('mLF:', gF.lineno(), '| popWord:', popWord)
        if len(popWord[1]) > 0:
            result = testMeterWord(empLine, qLine, popWord)
        print('mLF:', gF.lineno(), '| runLine:', runLine)
        print('mLF:', gF.lineno(), '| qLine:', qLine)
        if result == True:
            print('mLF:', gF.lineno(), '| runLine:', runLine)
            print('mLF:', gF.lineno(), '| qLine:', qLine)
            qLine = gF.lineFunk.acceptWordR(empLine, runLine, qLine, popWord)
            print('mLF:', gF.lineno(), qLine)
        elif len(gF.superPopList[-1]+gF.expressList[-1]+gF.thesList[-1]+gF.contList[-1]+gF.punxList[-1]+gF.dynaList[-1]) == 0:
            if len(gF.qLineIndexList[-1]) > gF.proxMinDial:
                gF.proxFunk.snipProxData(empLine, pLEmps, qLine, runLine)
            else:
                pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
        if len(gF.superPopList) == 0:
            return ([],[]), True
        pLEmps = gF.pEmpsLine(empLine, qLine[0])
        print('mLF:', gF.lineno(), '| qLine:', qLine, pLEmps)
        if pLEmps == empLine and qLine[1][-1] in gF.nonEnders:
            print('mLF:', gF.lineno(), '| gov() - nonending word')
            pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
        print('mLF:', gF.lineno(), '| gov() - end of meterGov ifchecks', qLine, pLEmps)
        while len(pLEmps) > len(empLine):  #  If somehow the line went over the numbered lists
            print('mLF:', gF.lineno(), '| gov() - meterGov over emps')
            pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
        print('mLF:', gF.lineno(), '| pLEmps:', pLEmps, '- empLine:', empLine)
    return qLine, False    


            # elif len(runLine[0]) == 1 and runLine[-1] in gF.endPunx:                
            # print('mLF:', gF.lineno(), '| gov() |  if3', runLine)
            # pLEmps, qLine, runLine = gF.lineFunk.lineStarter(empLine, proxExpress, ([], []))

        # try:  
        #     if len(gF.superPopList) == 0 and len(qLine[1]) == 0 and len(runLine[0]) == 0:
        #         print('mLF:', gF.lineno(), '| gov() | killSwitch == True')
        #         return qLine, True #  killSwitch event
        # except IndexError:  #  Either the lists are empty, or they don't exist at all
        #     print('mLF:', gF.lineno(), '| gov() | iE:', qLine, runLine)
        #     gF.printGlobalData(qLine)
        #     return pLEmps, qLine, True #  killSwitch event