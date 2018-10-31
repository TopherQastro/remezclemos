
def rhymeLiner(qLine, proxExpress, rhymeList):
    print('mLF:', gF.lineno(), '| rhymeLiner() | start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    while len(qLine[0] == 0) or (qLine[0][-1] not in rhymeList):
    if metSwitch == True:
        qLine, killSwitch = gF.meterLineFunk.gov(empLine, proxExpress, pLEmps, qLine, runLine)
    else:
        qLine, killSwitch = plainGovernor(empLine, proxExpress, pLEmps, qLine, runLine)

    if killSwitch == True:
       return qLine, killSwitch
    else:
        if qLine[0][-1] in gF.allPunx:
            if qLine[0][-2] not in rhymeList):
	        pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
		pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
            else:
                retun qLine, killSwitch
        elif (qLine[0][-1] not in rhymeList):  #  Words that don't sound good as the last word of a line, such as conjunctions without something else to connect
            pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
    qLine, killSwitch = meterGovernor(empLine, rhymeList, pLEmps, qLine, runLine)  #  Switch proxExpress to rhymeList to get them preferred

    print('mLF:', gF.lineno(), '| rhymeLiner() | out:', qLine, 'len(gF.superPopList):', len(gF.superPopList), 'killSwitch:', killSwitch)

    return qLine, killSwitch

    