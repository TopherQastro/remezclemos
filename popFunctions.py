
import globalFunctions as gF


# Organizes expressList and superPopList words to cont, thes, punx
def popWordScanner(popWord):
    print('ppF:', gF.lineno(), ' | popWordScanner() thisList:', len(thisList))
    gF.printGlobalData(qLine)
    print('ppF:', gF.lineno(), ' | testExPop:', popWord)
    # popWord is the same word unless the phonetic data doesn't match the 'real' data
    qWord = ([popWord], [popWord])
    # This line will place contractions in a special list to be switched if nothing works
    if (gF.contSwitch == True) and (popWord in gF.contractionList) and (popWord[:-2] != "'s") and (popWord[-1] != "'") and (popWord[:2] != ("o'" or "d'")):
        gF.contList[-1].append(popWord)
    elif popWord in gF.allPunx:
        gF.superList[5][-1].append(popWord)
    elif popWord not in gF.allPunx:  # A zero-length emps value is an unrecognized word
        if (gF.thesSwitch == True) and (popWord not in gF.quantumList) and (popWord not in gF.thesList[-1]):
            gF.thesList[-1].append(popWord)
    print('ppF:', gF.lineno(), gF.soundLine[3], qLine, qWord)


def popWordPicker(qLine):  # Digests words that fit a particular meter
    print('ppF:', gF.lineno(), '| popWordPicker start')
    # $gF.printGlobalData(qLine)
    while len(gF.superList[1][-1]+gF.superList[0][-1]+gF.thesList[-1]+gF.contList[-1]) > 0:
        print('ppF:', gF.lineno(), '| whileLoop entered')
        if len(gF.superList[0]) > 0:
            # If the first expressList is out, move non-quantum to front
            if len(gF.superList[0][-1]) == 0:
                burnList = []
                for word in gF.superList[1][-1]:
                    if word not in gF.quantumList:
                        gF.superList[0][-1].append(word)
                        burnList.append(word)
                for word in burnList:
                    gF.superList[1][-1].pop(gF.superList[1][-1].index(word))
            if len(gF.superList[0][-1]) > 0:
                popWord = gF.superList[0][-1].pop(0)
                return (popWord, popWord)
            elif len(gF.superList[1][-1]) > 0:
                popWord = gF.superList[1][-1].pop(
                    gF.random.choice(range(0, len(gF.superList[1][-1]))))
                return (popWord, popWord)
        print('ppF:', gF.lineno(), ' | gF.contSwitch:', gF.contSwitch)
        # If any contractions were found in the gF.superList[1] we just tried
        if (gF.contSwitch == True) and (len(gF.contList[-1]) > 0):
            print('ppF:', gF.lineno(), ' | gF.contList[-1]:', gF.contList[-1])
            pWord = gF.contList[-1].pop(gF.random.choice(range(0,
                                        len(gF.contList[-1]))))
            contWord = gF.contractionDic[pWord]
            if len(contWord) == 0:  # If there's no contraction, it's just a word with an apostrophe
                contWord = pWord
            print('ppF:', gF.lineno(), ' | contWord:', contWord)
            # Appending two different words to the line
            qWord = (contWord, pWord)
            print('ppF:', gF.lineno(), ' | contraction attempt:', qWord)
            return qWord
        print('ppF:', gF.lineno(), ' | gF.thesSwitch:', gF.thesSwitch)
        if (gF.thesSwitch == True) and (len(gF.contList[-1]) > 0):
            if len(gF.dynaList[-1]) > 0:
                return gF.dynaList[-1].pop(gF.random.choice(range(0, len(gF.dynaList[-1]))))
            else:
                while len(gF.thesList[-1]) > 0:
                    print('ppF:', gF.lineno(
                    ), ' | thesCheck | len(gF.thesList[-1]):', len(gF.thesList[-1]))
                    thesWord = gF.thesList[-1].pop(
                        gF.random.choice(range(0, len(gF.thesList[-1]))))
                    try:
                        syns = thesDic[thesWord]
                    except KeyError:
                        syns = []
                        print('ppF:', gF.lineno(), ' | kE:thesWord', thesWord)
                        continue
                    print('ppF:', gF.lineno(), ' | syns:', syns)
                    while len(syns) > 0:
                        synonym = syns.pop(
                            gF.random.choice(range(0, len(syns))))
                        qWord = (synonym, thesWord)
                        print('ppF:', gF.lineno(), ' | thes qWord:', qWord)
                        gF.dynaList[-1].append[qWord]
    if len(qLine[1]) > 2:  # We want qLine to have more than 2 words before trying punctuation because it sounds better, although it isn't necessary for function. Also, make sure to exhaust all other possibilities first
        print('ppF:', gF.lineno(), ' | punxSearch',
              qLine[1][-(min(gF.punxDial, len(qLine[1]))):])
        punxCt = int(0)
        for punk in qLine[1][-(min(gF.punxDial, len(qLine[1]))):]:
            if punk in gF.allPunx:  # Will discriminate any puncuation within the designated length of gF.punxDial
                print('ppF:', gF.lineno(),
                      ' | found punk within gF.punxDial:', punk)
                punxCt += 1
        if (punxCt == 0) and (len(gF.superList[5][-1]) > 0) and (qLine[1][-1] not in gF.nonEnders):
            punxWord = gF.superList[5][-1].pop(
                gF.random.choice(range(0, len(gF.superList[5][-1]))))
            qWord = (punxWord, punxWord)
            return qWord
    print('ppF:', gF.lineno(), 'popWordPicker found nothing')
    return ([], [])


# Creates a list-of-lists to pull from
def superPopListMaker(proxExpress, qLine, runLine):
    print('ppF:', gF.lineno(), 'sPLM init | len(gF.superList[1])',
          len(gF.superList[1]))
    print('ppF:', gF.lineno(), 'qLine:', qLine)
    gF.printGlobalData(qLine)
    keepList = []  # Will return empty set upon failure
    testLine = ([], [])
    killSwitch = False
    if len(runLine[0]) > 0:  # If there's a previous line, add it into testLine
        for each in runLine[0]:
            testLine[0].append(each)
        for each in runLine[1]:
            testLine[1].append(each)
    for each in qLine[0]:
        testLine[0].append(each)
    for each in qLine[1]:
        testLine[1].append(each)
    print('ppF:', gF.lineno(), '| superPopListMaker() - start', len(gF.superList[1]), testLine,
          'proxData:', gF.qLineIndexList, gF.superList[7])
    print('ppF:', gF.lineno(), '| superPopListMaker() - len(testLine) >= 1',
          gF.qLineIndexList, gF.superList[7])
    if len(testLine) == 0:
        for firstWords in gF.firstWords:
            gF.superList[1][-1].append(firstWords)  
            return qLine, runLine, False
    print('ppF:', gF.lineno(), '| qLine:', qLine)
    try:
        print('ppF:', gF.lineno(), '| superPopListMaker() -', qLine, testLine)
        if len(gF.qLineIndexList[-1]) > len(gF.proxPlusLista):
            qLine, runLine = gF.proxFunk.snipProxData(proxExpress, qLine, runLine)
        while len(gF.qLineIndexList[-1]) > 0:
            print('ppF:', gF.lineno(), '| superPopListMaker() - main while', testLine)
            proxP1grab = gF.proxFunk.proxGrabber(testLine[1][-1], 0)
            for all in proxP1grab:
                if (all != testLine[1][-1]):
                    # Practically an 'else' clause, because the 'if' above returns an answer
                    keepList.append(all)
            print('ppF:', gF.lineno(), '| proxP1 keepList:', len(keepList))
            # Only keep going if we need more than 2 words analyzed
            if len(gF.qLineIndexList[-1]) > 1:
                print('ppF:', gF.lineno(), '| superPopListMaker() - testLine:', testLine, gF.qLineIndexList)
                # Skip first indexNum, we already found it
                for proxDicIndexes in gF.superList[7][-1][1:]:
                    print('ppF:', gF.lineno(), '| superPopListMaker() - testLine:', testLine, '\n', testLine[1], [gF.qLineIndexList[-1][proxDicIndexes]], proxDicIndexes)
                    testList = gF.proxFunk.proxGrabber(testLine[1][gF.qLineIndexList[-1][proxDicIndexes]], proxDicIndexes)
                    # testList = gF.proxPlusLista[each][testLine[1][gF.qLineIndexList[-1][each]]]  #  Scans approximate words with indexes
                    burnList = []  # burnList holds words that don't match with mutual proxLists
                    for all in keepList:
                        # or (testString not in rawText):  #  Add blackList screening later
                        if (all not in testList):
                            # Screen it with a burnList so we don't delete as we iterate thru list
                            burnList.append(all)
                    print('ppF:', gF.lineno(), '| superPopListMaker() - len(keepList):', len(keepList), 'len(burnList):', len(burnList))
                    if len(keepList) > 0:
                        print('ppF:', gF.lineno(), '| trimming keeplist')
                        for all in burnList:
                            keepList.remove(all)
                    else:  # If we run out prematurely, stop iterating over the list
                        print('ppF:', gF.lineno(), '| superPopListMaker() - keepList out')
                        break
            print('ppF:', gF.lineno(), '| final keepList:', len(keepList))
            if len(keepList) == 0:
                print('ppF:', gF.lineno(), '| keepList empty', qLine, testLine)
                if len(qLine[0]) > 1:
                    print('ppF:', gF.lineno(), '|', len(gF.qLineIndexList), '>=', gF.proxMinDial, "?")
                    if len(gF.qLineIndexList) >= gF.proxMinDial:
                        # superListCt = int(0)
                        # for lists in gF.superList:
                        #     superListCt+=len(lists[-1])
                        # if superListCt == 0:
                        qLine, runLine = gF.proxFunk.snipProxData(proxExpress, qLine, runLine)
                        print('ppF:', gF.lineno(), '|', len(gF.qLineIndexList))
                    else:
                        print('ppF:', gF.lineno(), '| proxdata too short')
                        input('paused...')
                        qLine, runLine = gF.lineFunk.removeWordR(empsKeyLine, qLine, runLine)
                else:
                    print('ppF:', gF.lineno(), '| superPopList lost line')
                    killSwitch = True
                    break
            else:
                print('ppF:', gF.lineno(), '| superPopListMaker() - grown', len(gF.superList[1]), '|', testLine, 'proxData:', gF.qLineIndexList, gF.superList[7])
                if len(gF.superList[1]) == 0:
                    for lists in gF.superList[:-3]:
                        lists.append([])
                for keepWords in keepList:
                    if keepWords in gF.allPunx:
                        gF.superList[5][-1].append(keepWords)
                    elif (keepWords in proxExpress) and (keepWords not in gF.superList[0][-1]) and (keepWords not in gF.quantumList):
                        gF.superList[0][-1].append(keepWords)
                    elif all not in gF.superList[1][-1]:
                        gF.superList[1][-1].append(keepWords)
                break
        print('ppF:', gF.lineno(), 'qLine:', qLine)
        gF.printGlobalData(qLine)
        return qLine, runLine, killSwitch
    except KeyError:
        print('ppF:', gF.lineno(), 'kE:', testLine,
              'len(gF.superList[1]):', len(gF.superList[1]))
        input('paused...')
        unknownWords.write(qLine[1][-1])
        pLEmps, qLine, runLine = gF.lineFunk.removeWordR(empLine, qLine, runLine)
        #gF.proxFunk.proxDataBuilder(qLine, len(qLine[0]))
        return qLine, runLine
    print('ppF:', gF.lineno(), 'sPM lastfinish', qLine)
    gF.printGlobalData(qLine)
    return qLine, runLine, killSwitch
