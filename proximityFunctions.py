
import globalFunctions as gF


def loadmakeData():
    try:
        filepath = (gF.lang+'/data/textLibrary/textData/'+gF.textFile+'-firstFile.txt')
        print('pxF:', gF.lineno(), ' | begin fwFile load', filepath) 
        firstFile = open(filepath, 'r')
        for line in firstFile:
            gF.firstWords.append(line[:-1])
            gF.firstPopList.append(line[:-1])
        print('pxF:', gF.lineno(), ' | firstFile load complete')       
    except FileNotFoundError:  #  Triggered if files don't exist, so we make new ones
        proxNewBuild()


def proxNewBuild():
    print('pxF:', gF.lineno(), '| initializing empty proxSQL...')
    for letter in gF.upperAlphabet:
        gF.proxCursor.execute('''CREATE TABLE mastProx'''+letter+'''(word TEXT,
        proxP1 TEXT, proxP2 TEXT, proxP3 TEXT, proxP4 TEXT, proxP5 TEXT, proxP6 TEXT,
        proxP7 TEXT, proxP8 TEXT, proxP9 TEXT, proxP10 TEXT, proxP11 TEXT, proxP12 TEXT,
        proxP13 TEXT, proxP14 TEXT, proxP15 TEXT, proxP16 TEXT, proxP17 TEXT, proxP18 TEXT,
        proxP19 TEXT, proxP20 TEXT, proxP21 TEXT, proxP22 TEXT, proxP23 TEXT, proxP24 TEXT,
        proxM1 TEXT, proxM2 TEXT, proxM3 TEXT, proxM4 TEXT, proxM5 TEXT, proxM6 TEXT,
        proxM7 TEXT, proxM8 TEXT, proxM9 TEXT, proxM10 TEXT, proxM11 TEXT, proxM12 TEXT,
        proxM13 TEXT, proxM14 TEXT, proxM15 TEXT, proxM16 TEXT, proxM17 TEXT, proxM18 TEXT,
        proxM19 TEXT, proxM20 TEXT, proxM21 TEXT, proxM22 TEXT, proxM23 TEXT, proxM24 TEXT)''')

    print('pxF:', gF.lineno(), ' | building firstfile...')
    firstFile = open(gF.lang+'/data/textLibrary/textData/'+gF.textFile+'-firstFile.txt', 'w+')
    print('pxF:', gF.lineno(), ' | begin loadmakeProxLibs()')
    #  Prox and gramprox store Markov chains and build in -Liner() functions
    #  Libs declared here, made into lists of dics of lists, and called using indices on     
    #  The maximum length of theseslists are truncated based on the user's initial input
    print('pxF:', gF.lineno(), ' | builing proxLibs...')
    fullList = []
    newSplitText = []
    splitLineIndex = int(0)
    fonoLine, vocsLine, consLine, empsLine = gF.soundsLine
    for words in gF.splitText:
        #print('pxF:', gF.lineno(), '| checking:', words)
        if words in gF.doubles:
            words+='(0)'
            #print('pxF:', gF.lineno(), '| doubled:', words)
        dicCheck = gF.fonoFunk.addFonoLine([], (words, words))
        #print('pxF:', gF.lineno(), '| result:', dicCheck, '-', words)
        if dicCheck == 'gotIt' or words in gF.allPunx:
            if '(0)' in words:
                #print('pxF:', gF.lineno(), '| trimming:', words)
                words = words[:-3]
                #print('pxF:', gF.lineno(), '| fixed:', words)
            if words not in fullList:
                fullList.append(words)
            newSplitText.append(words)
            #print('pxF:', gF.lineno(), '| adding:', words, '| len(newSplitText):', len(newSplitText))
        else:
            newSplitText.append('nullWord')  #  skip words that don't exist
            #print('pxF:', gF.lineno(), '| rejecting:', words)
        splitLineIndex+=1
        empsLine = []  #  Continuously erase empsLine, as we're only checking if words exist in dics
        gF.soundsLine = fonoLine, vocsLine, consLine, empsLine
    for all in range(0, (len(gF.proxMinusLista))):  #  Now that we've got an exhaustive list of real words,
        for each in fullList:                       #  we'll create empty lists for all of them
            gF.proxMinusLista[all][each] = []
            gF.proxMinusLista[all][each] = []
    splitTLen = len(newSplitText)
    splitTIndex = int(0)
    for words in newSplitText:  #  
        #print('pxF:', gF.lineno(), ' | working here:', splitTIndex, gF.splitText[splitTIndex:splitTIndex+15])
        if words != 'nullWord' and len(words) > 0 and words not in gF.deadPunx:
            try:
                tablekey = words[0].upper()
                if tablekey not in gF.upperAlphabet:
                    tablekey = 'Q'
                proxNumerator, proxDicCounter, proxMax = int(1), int(0), len(gF.proxMinusLista)
                if words in gF.endPunx:
                    #print('pxF:', gF.lineno(), ' | firstWord:', newSplitText[splitTIndex+1]) 
                    firstWord = newSplitText[splitTIndex+1]
                    if firstWord not in gF.firstWords:
                        gF.firstWords.append(firstWord)
                        firstFile.write(firstWord+'\n')
                while proxDicCounter < proxMax and splitTIndex+proxNumerator < splitTLen:
                    try:
                        proxWord = gF.splitText[splitTIndex+proxNumerator]
                        if len(proxWord) > 0 and proxWord != 'nullWord':
                            if proxWord not in gF.proxPlusLista[proxDicCounter][words]:
                                #print('pxF:', gF.lineno(), ' | plusadd = proxP:', proxWord, 'words:', words, proxDicCounter, proxNumerator)
                                gF.proxPlusLista[proxDicCounter][words].append(proxWord)
                            if words not in gF.proxMinusLista[proxDicCounter][proxWord]:
                                #print('pxF:', gF.lineno(), ' | minusadd = proxM:', proxWord, 'words:', words, proxDicCounter, proxNumerator)
                                gF.proxMinusLista[proxDicCounter][proxWord].append(words)
                    except TypeError:
                        print('pxF:', gF.lineno(), ' | prox tE:', proxWord)
                        proxDicCounter += 1
                        proxNumerator += 1
                        continue
                    except IndexError:  #  If the list is over
                        break
                    proxDicCounter += 1
                    proxNumerator += 1
            except TypeError:
                splitTIndex+=1
                #print('pxF:', gF.lineno(), splitTIndex)
                #print('pxF:', gF.lineno(), ' | p tE:', words)
                continue
            splitTIndex+=1
            if splitTIndex%1000==0:
                print('pxF:', gF.lineno(), ' | prox', splitTIndex, 'of', len(gF.splitText))       
        else:
            splitTIndex+=1

    for word in fullList:
        if len(word) > 0:
            #print('pxF:', gF.lineno(), word)
            entry = word
            if entry[0].upper() in gF.upperAlphabet:
                tableKey = entry[0].upper()
            else:
                tableKey = 'Q'

            superProxEntry = []
            for proxPDics in gF.proxPlusLista:
                proxEntry = str()
                for proxKeys in proxPDics[word]:
                    proxEntry+=(proxKeys+'^')
                superProxEntry.append(proxEntry[:-1])
            for proxMDics in gF.proxMinusLista:
                proxEntry = str()
                for proxKeys in proxMDics[word]:
                    proxEntry+=(proxKeys+'^')
                superProxEntry.append(proxEntry[:-1])

            #print('pxF:', gF.lineno(), superProxEntry)
            
            try:        
                gF.proxCursor.execute('''INSERT INTO mastProx'''+tableKey+''' (word,
                proxP1, proxP2, proxP3, proxP4, proxP5, proxP6,
                proxP7, proxP8, proxP9, proxP10, proxP11, proxP12,
                proxP13, proxP14, proxP15, proxP16, proxP17, proxP18,
                proxP19, proxP20, proxP21, proxP22, proxP23, proxP24,
                proxM1, proxM2, proxM3, proxM4, proxM5, proxM6,
                proxM7, proxM8, proxM9, proxM10, proxM11, proxM12,
                proxM13, proxM14, proxM15, proxM16, proxM17, proxM18,
                proxM19, proxM20, proxM21, proxM22, proxM23, proxM24)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                       ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (word, 
                       superProxEntry[0], superProxEntry[1], superProxEntry[2], superProxEntry[3],
                       superProxEntry[4], superProxEntry[5], superProxEntry[6], superProxEntry[7],
                       superProxEntry[8], superProxEntry[9], superProxEntry[10], superProxEntry[11],
                       superProxEntry[12], superProxEntry[13], superProxEntry[14], superProxEntry[15],
                       superProxEntry[16], superProxEntry[17], superProxEntry[18], superProxEntry[19],
                       superProxEntry[20], superProxEntry[21], superProxEntry[22], superProxEntry[23],
                       superProxEntry[24], superProxEntry[25], superProxEntry[26], superProxEntry[27],
                       superProxEntry[28], superProxEntry[29], superProxEntry[30], superProxEntry[31],
                       superProxEntry[32], superProxEntry[33], superProxEntry[34], superProxEntry[35],
                       superProxEntry[36], superProxEntry[37], superProxEntry[38], superProxEntry[39],
                       superProxEntry[40], superProxEntry[41], superProxEntry[42], superProxEntry[43],
                       superProxEntry[44], superProxEntry[45], superProxEntry[46], superProxEntry[47]))
            except KeyError:
                print('pxF:', gF.lineno(), ' | fuckery:', entry)
                continue

    gF.proxConn.commit()
    #input('paused...')

def proxDataBuilder(qLine, limitNum):  #  Takes the qLine and builds proxData up to a certain length
    print('pxF:', gF.lineno(), '| proxDataBuilder() - qLine:', qLine) # , qLineIndexList, proxDicIndexList)
    qLineLen = len(qLine[1])
    proxInt = int(0)  #  Starts the proxData
    print('pxF:', gF.lineno(), '| proxDataBuilder() - proxData:', gF.qLineIndexList, gF.proxDicIndexList)
    if len(qLine[1]) > 0:
        # gF.qLineIndexList.append([0])
        # gF.proxDicIndexList.append([0])
        while proxInt < qLineLen:  #  Creates a list of indexes and the reverse list to index proxDics
            gF.proxDicIndexList[-1].append(proxInt)
            gF.qLineIndexList[-1].insert(0, proxInt)
            proxInt+=1
    print('pxF:', gF.lineno(), '| proxDataBuilder() - qLine:', qLine, 
                               '- proxData:', gF.qLineIndexList, gF.proxDicIndexList)


def snipProxData(proxExpress, qLine, runLine):
    print('pxF:', gF.lineno(), '| snipProxData() start', qLine)
    if len(qLine[1]) > 0:
        print('pxF:', gF.lineno(), '| len(qLine[1]) > 0')
        if (len(gF.qLineIndexList[-1]) > gF.proxMinDial) and (len(runLine[1]+qLine[1]) > gF.proxMinDial):
            print('pxF:', gF.lineno(), '| snip qLineIndex in:', gF.qLineIndexList, 
                    gF.proxDicIndexList, runLine[1], qLine[1])
            gF.qLineIndexList[-1].pop()
            gF.proxDicIndexList[-1].pop()
            print('pxF:', gF.lineno(), '| snip qLineIndex out:', 
                    gF.qLineIndexList, gF.proxDicIndexList)
            # for eachList in gF.superList[:-2]:
            #     if len(eachList) > 0:
            #         eachList.pop()
            # gF.printGlobalData(qLine)
            # if len(gF.superBlackList) > (len(gF.superPopList) + 1):
            #     print('pxF:', gF.lineno(), '| superBlackPop')
            #     gF.superBlackList.pop()
            # qLine, runLine, killSwitch = gF.popFunk.superPopListMaker(empLine, pLEmps, proxExpress, qLine, runLine)
        else: #and len(qLine[1]) > gF.proxMinDial:  #  If we have enough words, then we can remove rightmost element and metadata, then try again
            print('pxF:', gF.lineno(), '| snipLine', qLine, '|', runLine, len(gF.superPopList))
            qLine, runLine = gF.lineFunk.removeWordR(qLine, runLine)
    return qLine, runLine


def proxGrabber(thisWord, proxIndex):
    print('pxF:', gF.lineno(), '| proxGrabbing:', thisWord, gF.proxPlusStrings[proxIndex])
    print('pxF:', gF.lineno(), '| pulling from SQL database', gF.proxPlusLista[proxIndex][thisWord])
    tablekey = thisWord[0].upper()
    if tablekey not in gF.upperAlphabet:
        if gF.lang == 'eng':
            tablekey = 'Q'
        elif gF.lang == 'esp':
            tablekey = 'K'
    gF.proxCursor.execute('''SELECT '''+gF.proxPlusStrings[proxIndex]+''' FROM mastProx'''+tablekey+''' WHERE word=?''', (thisWord,))
    proxInfo = gF.proxCursor.fetchone()
    print('pxF:', gF.lineno(), '| proxInfo:', proxInfo)
    if proxInfo == None:
        proxList = []
        print('pxF:', gF.lineno(), '| proxList not found')
    else:
        proxList = proxInfo[0].split('^')
    print('pxF:', gF.lineno(), '| proxList:', proxList)
    #input('paused')
    gF.proxPlusLista[proxIndex][thisWord] = proxList
    return proxList