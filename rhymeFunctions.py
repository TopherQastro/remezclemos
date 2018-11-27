
import globalFunctions as gF


def rhyDictator(lang, pWord, maxTotalVs, maxRSyls): # Find rhymes of a particular word
    print('ryF:', gF.lineno(), '| entering rhyDictator() w/', pWord)
    print('ryF:', gF.lineno(), '| len(gF.splitText):', len(gF.splitText))
    #$input('paused...')
    matchBox, finalRhys = [], []
    totalVs, rSyls = int(1), int(1)
    while totalVs < maxTotalVs:
        while (rSyls <= totalVs):
            tName, rName = str(totalVs), str(rSyls)
            #$print('ryF:', gF.lineno(), '| rhy:', pWord, str(totalVs), str(rSyls))
            if totalVs < 10:
                tName = '0'+tName
            if rSyls < 10:
                rName = '0'+rName
            try:
                #$print('ryF:', gF.lineno(), '| tName, rName:', tName, rName)
                dicFile = gF.csv.reader(open(lang+'/data/USen/rhymes/rhymeLib-t'+tName+"r"+rName+".csv", "r"))
                for line in dicFile:
                    strikeList = []
                    keyChain = line[0].split('^')
                    valChain = line[1].split('^')
                    #$if len(keyChain) > 0:
                        #$print('ryF:', gF.lineno(), '| keyChain:', keyChain)
                    #$if len(valChain) > 0:
                        #$print('ryF:', gF.lineno(), '| valChain:', valChain)
                    if (pWord in keyChain) or (pWord in valChain):
                        if pWord in valChain:
                            valChain.remove(pWord)
                        matchBox = valChain
                        #$print('ryF:', gF.lineno(), '| matchBox:', matchBox)
                        for matches in matchBox:
                            if '(' in matches:
                                newWord = matches[:-3]
                                matchBox.append(newWord)
                                strikeList.append(matches)
                            if matches not in gF.splitText:
                                #$print('ryF:', gF.lineno(), '| striking:', matches)
                                strikeList.append(matches)
                            #$else:
                                #$print('ryF:', gF.lineno(), '| keeping:', matches)
                        for strikes in strikeList:
                            if strikes in matchBox:
                                matchBox.remove(strikes)
                        strikeList = []                        
                    for finalMatches in matchBox:
                        if finalMatches not in finalRhys:
                            finalRhys.append(finalMatches)
                    #$print('ryF:', gF.lineno(), 'len(finalRhys):', len(finalRhys))
            except IOError:
                return []
            rSyls+=1
        totalVs+=1
        rSyls = int(1)
    finalRhys.sort()
    print('ryF:', gF.lineno(), '| finalRhys:', len(finalRhys))
    #$input('paused...')
    return finalRhys


def rhymeLiner(empLine, proxExpress, qAnteLine, rhymeList):
    print('ryF:', gF.lineno(), '| rhymeLiner() - start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    qLine = [[], []]
    pLEmps = []
    while (len(qLine[0]) == 0) or (qLine[0][-1] not in rhymeList):
        if gF.metSwitch == True:
            qLine, killSwitch = gF.meterFunk.gov(empLine, pLEmps, qLine, qAnteLine, proxExpress)
        else:
            qLine, killSwitch = gF.plainFunk.gov(empLine, pLEmps, qLine, qAnteLine, proxExpress)
        if killSwitch == True:
            return qLine, killSwitch
        else:
            if qLine[0][-1] in gF.allPunx:
                if qLine[0][-2] not in rhymeList:
                    pLEmps, qLine, qAnteLine = gF.lineFunk.removeWordR(empLine, qLine, qAnteLine)
                    pLEmps, qLine, qAnteLine = gF.lineFunk.removeWordR(empLine, qLine, qAnteLine)
                else:
                    return qLine, killSwitch
            elif qLine[0][-1] not in rhymeList:  #  Words that don't sound good as the last word of a line, such as conjunctions without something else to connect
                pLEmps, qLine, qAnteLine = gF.lineFunk.removeWordR(empLine, qLine, qAnteLine)
    print('ryF:', gF.lineno(), '| rhymeLiner() - out:', qLine, 'len(gF.superPopList):', len(gF.superPopList), 'killSwitch:', killSwitch)
    return qLine, killSwitch
