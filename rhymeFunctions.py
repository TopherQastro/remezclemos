
import globalFunctions as gF


def rhyDictator(lang, superTokens, pWord, maxTotalVs, maxRSyls): # Find rhymes of a particular word
    matchBox, finalRhys = [], []
    totalVs, rSyls = int(1), int(1)
    while totalVs < maxTotalVs:
        while (rSyls <= totalVs):
            tName, rName = str(totalVs), str(rSyls)
           #$ print('gF:', lineno(),.rhy:', pWord, str(totalVs), str(rSyls))
            if totalVs < 10:
                tName = '0'+tName
            if rSyls < 10:
                rName = '0'+rName
            try:
                dicFile = csv.reader(open(lang+'/data/USen/rhymes/rhymeLib-t'+tName+"r"+rName+".csv", "r"))
                for line in dicFile:
                    strikeList = []
                    keyChain = line[0].split('^')
                    if pWord in keyChain:
                        matchBox = line[1].split('^')
                        if pWord in matchBox:
                            matchBox.remove(pWord)
                        for all in matchBox:
                            if '(' in all:
                                newWord = all[:-3]
                                matchBox.append(newWord)
                                strikeList.append(all)
                            if all not in superTokens:
                                strikeList.append(all)
                        for all in strikeList:
                            if all in matchBox:
                                matchBox.remove(all)
                        strikeList = []                        
                        for all in matchBox:
                            if all not in finalRhys:
                                finalRhys.append(all)
                for all in matchBox:
                    if all not in finalRhys:
                        finalRhys.append(all)
            except IOError:
                return []
            rSyls+=1
        totalVs+=1
        rSyls = int(1)
    finalRhys.sort()
   #$ print('gF:', lineno(),.rhys:', len(finalRhys))
    return finalRhys


def rhymeLiner(qLine, proxExpress, rhymeList):
    print('mLF:', gF.lineno(), '| rhymeLiner() | start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    while (len(qLine[0] == 0) or (qLine[0][-1] not in rhymeList):
        if metSwitch == True:
            qLine, killSwitch = gF.meterLineFunk.gov(empLine, proxExpress, pLEmps, qLine, runLine)
        else:
            qLine, killSwitch = gF.plainLineFunk.gov(empLine, proxExpress, pLEmps, qLine, runLine)
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
    print('mLF:', gF.lineno(), '| rhymeLiner() | out:', qLine, 'len(gF.superPopList):', len(gF.superPopList), 'killSwitch:', killSwitch)
    return qLine, killSwitch

    