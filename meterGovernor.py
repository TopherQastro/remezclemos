
def meterLiner(empLine, proxExpress, qAnteLine):  #
    print(lineno(), 'meterLiner() | start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, qAnteLine)
    while (pLEmps != empLine) or (qLine[0][-1] in nonEnders):  #  Keep going until the line is finished or returns blank answer
        pLEmps, qLine, runLine, redButton = meterGovernor(empLine, proxExpress, pLEmps, qLine, runLine)
        if redButton == True:
            return qLine, redButton
        if pLEmps == empLine:
            print(lineno(), 'meterLiner() | pLEmps == empLine | superPopList:',
                  len(superPopList), len(superPopList[-1]))
            if qLine[1][-1] in nonEnders:  #  Words that don't sound good as the last word of a line, such as conjunctions without something else to connect
                pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
            else:
                for all in allPunx:
                    if all in superPopList[-1]:  #  If puncuation fits, place one on the end of a line (will give the next line an easier start, too)
                        qLine = acceptWordR(empLine, qLine, runLine, ([all], [all]))
                        break
        if redButton == True:
            return qLine, redButton
    print(lineno(), 'meterLiner() | out:', qLine, 'len(superPopList):', len(superPopList), 'redButton:', redButton)
    return qLine, redButton
          #qLine, redButton
            

def rhymeLiner(empLine, proxExpress, rhymeList, qAnteLine):
    print(lineno(), 'rhymeLiner() | start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, qAnteLine)
    if len(qLine[1]) == 0:
        return qLine, True
    while (qLine[0][-1] not in rhymeList) or (qLine[0][-1] in nonEnders) or (pLEmps != empLine):
        pLEmps, qLine, runLine, redButton = meterGovernor(empLine, proxExpress, pLEmps, qLine, runLine)
        if redButton == True:
            return qLine, redButton
        if pLEmps == empLine:
            print(lineno(), 'rhymeLiner() | pLEmps == empLine | qLine[0]:', qLine[0])
            if (qLine[0][-1] in allPunx):
                pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
            if (qLine[0][-1] in nonEnders) or (qLine[0][-1] not in rhymeList):  #  Words that don't sound good as the last word of a line, such as conjunctions without something else to connect
                pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
                pLEmps, qLine, runLine, redButton = meterGovernor(empLine, rhymeList, pLEmps, qLine, runLine)  #  Switch proxExpress to rhymeList to get them preferred
            else:
                for punc in allPunx:
                    if punc in superPopList[-1]:  #  If puncuation fits, place one on the end of a line (will give the next line an easier start, too)
                        qLine = acceptWordR(empLine, qLine, runLine, ([punc], [punc]))
                        return qLine, redButton
        if redButton == True:
            return qLine, redButton
    print(lineno(), 'rhymeLiner() | out:', qLine, 'len(superPopList):', len(superPopList), 'redButton:', redButton)
    if redButton == True:
        return qLine, redButton
    print(lineno(), 'rhymeLiner() | rhyHere1:', qLine)
    return qLine, redButton

    
def meterGovernor(empLine, proxExpress, pLEmps, qLine, runLine):
    print(lineno(), 'meterGovernor() | runLine:', runLine, '| qLine:', qLine)
    global startTime
    stopTime = time.time()
    if stopTime > (startTime + 300):
        qLine, runLine, redButton = vetoLine(runLine, [])
        startTime = time.time()
        print(lineno(), 'meterGovernor() | timeout restart |', str(time.ctime())[11:20])
        return pLEmps, qLine, runLine, True  
    while pLEmps != empLine:
        print(lineno(), 'meterGovernor() | metGov while start')
        if len(qLine[1]) == 0:  #  Check if we're starting with a completely empty line, load firstWords to superPopList if so
            print(lineno(), 'meterGovernor() | meterGov if0')
            pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, runLine) 
        elif len(qLine[1]) > 0:
            print(lineno(), 'meterGovernor() | meterGov if2 qLine:', qLine, 'len(superBlackList):', 
                  len(superBlackList), 'meterGovernor() | len(superPopList):', len(superPopList))
            if len(qLine[1]) == len(superPopList):
                qLine, runLine = superPopListMaker(empLine, proxExpress, qLine, runLine)                
            pLEmps, qLine, runLine = metPopDigester(empLine, proxExpress, qLine, runLine)
        elif len(runLine[0]) == 1 and runLine[-1] in endPunx:                
            print(lineno(), 'meterGovernor() |  if3', runLine)
            pLEmps, qLine, runLine = meterLinerStarter(empLine, proxExpress, ([], []))
        try:  
            if len(superPopList) == 0 and len(qLine[1]) == 0 and len(runLine[0]) == 0:
                print(lineno(), 'meterGovernor() | redButton == True')
                return pLEmps, qLine, runLine, True #  redButton event
        except IndexError:  #  Either the lists are empty, or they don't exist at all
            print(lineno(), 'meterGovernor() | iE:', qLine, runLine)
            printGlobalData(qLine)
            return pLEmps, qLine, runLine, True #  redButton event
        print(lineno(), 'meterGovernor() | end of meterGov ifchecks')
        while len(pLEmps) > len(empLine):  #  If somehow the line went over the numbered lists
            print(lineno(), 'meterGovernor() | meterGov over emps')
            pLEmps, qLine, runLine = removeWordR(empLine, qLine, runLine)
    return pLEmps, qLine, runLine, False    