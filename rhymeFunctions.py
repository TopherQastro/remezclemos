
#  This next section was organized as follows:
##  tVocs (or, 't') = 

import globalFunctions as gF

softRhySwitches = {'G':'K', 'D':'T', 'S':'TH', 'JH':'CH', 'F':'V'}  #  Voiced/unvoiced constantants (See: Korean language)
fCons = 'B', 'D', 'G', 'JH', 'L', 'N', 'P', 'S', 'T', 'V', 'ZH', 'CH', 'DH', 'F', 'HH', 'K', 'M', 'NG', 'R', 'SH', 'TH', 'W', 'Z'
fVocs = ['AA0', 'AH0', 'AW0', 'EH0', 'EY0', 'IH0', 'OW0', 'UH0', 'AE0', 'AO0', 'AY0', 'ER0', 'IY0', 'OY0', 'UW0', 'Y0',
         'AA1', 'AH1', 'AW1', 'EH1', 'EY1', 'IH1', 'OW1', 'UH1', 'AE1', 'AO1', 'AY1', 'ER1', 'IY1', 'OY1', 'UW1', 'Y1']
            

def rhySeeker(rhymeWord):
    #rhymeWord = input('Type word: ').upper()
    rhymeWord = rhymeWord.upper()  #  The file is in all caps
    rhymeList = []  #  Will contain lists of all suitable rhymes
    fonoFile = open('eng/data/USen/USen-primaryFono.txt', "r")
    for line in fonoFile:
        if rhymeWord+'  ' == line[0:len(rhymeWord)+2]:
            rhymeFono = line[len(rhymeWord)+2:].rstrip('\n')
            rhyListFono = rhymeFono.split(' ')
            break
    #print('ryF: |', rhymeWord, '=', rhyListFono)
    fonoFile = open('eng/data/USen/USen-primaryFono.txt', "r")  #  Need to reopen the file or it starts list from inputted rhymeWord
    for line in fonoFile:
        lineSplitSpot = line.index('  ')
        checkWord = line[:lineSplitSpot]
        checkFono = line[lineSplitSpot+2:].rstrip('\n')
        checkFono = checkFono.replace('2', '0')  #  Changes the secondary emphasis to easier matches
        listFono = checkFono.split(' ')
        rhyCheckFono = rhymeFono.split(' ')  #  This replenishes every loop for the word
        if gF.consMode == 'softRhy':  #  Consonant sounds that sound similar
            for key, val in softRhySwitches.items():
                listFono = listFono.replace(key, val)  #  Changes the cons to their matches, equalizing them
        elif gF.consMode == 'ignore':
            rCons = 0
            for cons in fCons:
                if cons in listFono:
                    listFono.remove(cons)
        #else:  It's 'fullList'
        #print('ryF: | listFono: ', checkWord, ':', listFono)
        theseSyls, theseCons = int(0), int(0)  #  Resets counts as every new word is processed
        while (len(rhyCheckFono) > 0) and (len(listFono) > 0):
            popCheckFono = listFono.pop()
            rhyPopCheckFono = rhyCheckFono.pop()
            #print('ryF: | ', popCheckFono, 'v.', rhyPopCheckFono)
            if popCheckFono == rhyPopCheckFono:
                if rhyPopCheckFono in fVocs:
                    #print('ryF: | sylsMatch')
                    theseSyls+=1
                    if theseSyls >= gF.rSyls:  #  If we find the number of syllables necessary
                        rhymeList.append(checkWord.lower())
                        #print('ryF: | rhyme found:', checkWord)
                        break
                else:
                    theseCons+=1
                    #print('ryF: | consMatch', theseCons, rCons)
            elif (popCheckFono in fCons) or (rhyPopCheckFono in fCons):
                if rCons > theseCons:  #  If we haven't surpassed the minimum consonant count, break without adding
                    #print('ryF: | consBreak')
                    break
                else:
                    try:
                        while popCheckFono in fCons:
                            popCheckFono = listFono.pop()
                        while rhyPopCheckFono in fCons:
                            rhyPopCheckFono = rhyCheckFono.pop()
                        #print('ryF: | newPops:', popCheckFono, rhyPopCheckFono)
                        if popCheckFono == rhyPopCheckFono:
                            #print('ryF: | sylsMatch')
                            theseSyls+=1
                            if theseSyls >= gF.rSyls:  #  If we find the number of syllables necessary
                                rhymeList.append(checkWord.lower())
                                #print('ryF: | rhyme found:', checkWord)
                                break
                    except IndexError:
                        #print('ryF: | ran out', rhyListFono, '-', listFono)
                        break
            else:
                #print('ryF: | mismatched, cancelled')
                break
    print('ryF: | rhymeList for', checkWord, '\n', rhymeList)
    return rhymeList
    

#rhySeeker(2)


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
