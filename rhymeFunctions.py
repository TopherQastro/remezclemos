
import globalFunctions as gF

def rhymeMainSQLBuild():

    print('fnF:', gF.lineno(), ' | begin rhymeSQLBuild()')

    for letter in gF.upperAlphabet:  #  Creating SQL database grouped by initial letter
        gF.rhymeCursor.execute('''CREATE TABLE mastRhyme'''+letter+'''(word TEXT,
        t01r01 TEXT, t02r01 TEXT, t03r01 TEXT, t04r01 TEXT, t05r01 TEXT, t06r01 TEXT, 
        t07r01 TEXT, t08r01 TEXT, t09r01 TEXT, t10r01 TEXT, 
        t02r02 TEXT, t03r02 TEXT, t04r02 TEXT, t05r02 TEXT, t06r02 TEXT, t07r02 TEXT, 
        t08r02 TEXT, t09r02 TEXT, t10r02 TEXT, 
        t03r03 TEXT, t04r03 TEXT, t05r03 TEXT, t06r03 TEXT, t07r03 TEXT, t08r03 TEXT, 
        t09r03 TEXT, t10r03 TEXT, 
        t04r04 TEXT, t05r04 TEXT, t06r04 TEXT, t07r04 TEXT, t08r04 TEXT, t09r04 TEXT, 
        t10r04 TEXT, 
        t05r05 TEXT, t06r05 TEXT, t01r01 TEXT, t01r01 TEXT, t01r01 TEXT, t01r01 TEXT, 
        t06r06 TEXT, t07r06 TEXT, t08r06 TEXT, t09r06 TEXT, t10r06 TEXT, 
        t07r07 TEXT, t08r07 TEXT, t09r07 TEXT, t10r07 TEXT, 
        t08r08 TEXT, t09r08 TEXT, t10r08 TEXT, 
        t09r09 TEXT, t10r09 TEXT, 
        t10r10 TEXT)''')

    #  Open exhaustive list of words
    fullList = []

    for word in fullList:
        if len(word) > 0:
            print('pxF:', gF.lineno(), word)
            entry = word
            if entry[0].upper() in gF.upperAlphabet:
                tableKey = entry[0].upper()
            else:
                tableKey = 'Q'
            
            try:        
                gF.fonoCursor.execute('''INSERT INTO mastProx'''+tableKey+''' (word TEXT,
                fono TEXT, emps TEXT, vocs TEXT, cons TEXT)
                VALUES(?,?,?,?,?)''', (word, fono, emps, vocs, cons))

            except KeyError:
                print('pxF:', gF.lineno(), ' | fuckery:', entry)
                continue

    gF.fonoConn.commit()
    input('paused...')


def rhyBuild_USen():

    rhyDic0 = defaultdict(list)
    rhyDic1 = defaultdict(list)

    #  In this emp data, the '1' signifies the dominant stress, which may be confusing
    #  since '2' is numerically greater but emphasized quieter, and the '0' remains
    #  lesser in both cases...

    fCons = 'B', 'D', 'G', 'JH', 'L', 'N', 'P', 'S', 'T', 'V', 'ZH', 'CH', 'DH', 'F', 'HH', 'K', 'M', 'NG', 'R', 'SH', 'TH', 'W', 'Z'
    fVocs = ['AA0', 'AH0', 'AW0', 'EH0', 'EY0', 'IH0', 'OW0', 'UH0', 'AE0', 'AO0', 'AY0', 'ER0', 'IY0', 'OY0', 'UW0', 'Y0',
            'AA1', 'AH1', 'AW1', 'EH1', 'EY1', 'IH1', 'OW1', 'UH1', 'AE1', 'AO1', 'AY1', 'ER1', 'IY1', 'OY1', 'UW1', 'Y1']
            

    phonoFile = open('data/USen/phonoLib-USen.txt', "r")


    print('rhyDic start')
    for line in phonoFile:
        dicData = line[:-1].split(' ')
        theseVocs = []
        for each in dicData[2:]:
            if '2' in each:
                thisVoc = each.replace('2', '1')
            else:
                thisVoc = each
            theseVocs.append(thisVoc)
        #print(dicData[0].lower(), theseVocs)
        rhyDic0[dicData[0].lower()] = theseVocs
        rhyDic1[dicData[0].lower()] = theseVocs
    print('rhyDic complete')


    totalVs = int(1)


def rhyMaker(totalVs, rSyls):
    tName = str(totalVs)
    rName = str(rSyls)
    if totalVs < 10:
        tName = '0'+tName
    if rSyls < 10:
        rName = '0'+rName
    try:
        libFile = gF.csv.reader(open('eng/data/USen/rhymes/rhymeLib-t'+tName+"r"+rName+".csv", "r"))
        print('rhymeLib-t'+tName+"r"+rName+" already exists")
    except IOError:
        dicFile = gF.csv.writer(open('eng/data/USen/rhymes/rhymeLib-t'+tName+"r"+rName+".csv", 'w+', encoding='latin-1'))
        print('rhymeLib-t'+tName+"r"+rName+" beginning....")
        yaFound = []
        thisRhyDic = {}
        for key, val in rhyDic0.items():
            keyList, valList = [], []
            keyString, valString = str(), str()
            if key not in yaFound:
                #print('finding:', key, val)
                vocCount  = int(0)
                presentVocs = []
                for all in fVocs:
                    if all in val:
                        #print('voc:', all)
                        presentVocs.append(all)
                        vocCount+=val.count(all)
                        #if val.count(all) > 1:
                            #print('FLAG THIS')
                #print('vocCount=', vocCount)
                if vocCount >= totalVs:
                    if vocCount == totalVs:
                        valList.append(key)
                    else:
                        keyList.append(key)
                    vocList = []
                    for all in presentVocs:
                        #print('trying:', all)
                        vocIndexer, vocTarget = int(0), int(0)
                        try:
                            while vocIndexer < totalVs:
                                #print(vocTarget, vocIndexer)
                                vocTarget=val[vocIndexer:].index(all)
                                vocList.append(vocTarget+vocIndexer)
                                vocIndexer+=(vocTarget+1)
                        except IndexError:
                            #print('iE')
                            vocIndexer = totalVs
                            continue
                        except ValueError:
                            #print('vE')
                            continue
                    vocList.sort()
                    #print('vocSpots:', key, val, vocList)
                    try:
                        rCutter = val[vocList[-rSyls]:]
                        #print('rCutter:', rCutter)
                        yaFound.append(key)
                        for key, val in rhyDic1.items():
                            try:
                                #print('tester:', key, val[-len(rCutter):])
                                if val[-len(rCutter):] == rCutter:
                                    #print('match found:', key)
                                    yaFound.append(key)
                                    vocCount = int(0)
                                    for all in fVocs:
                                        if all in val:
                                            vocCount+=val.count(all)
                                    #print('vocCount:', vocCount, totalVs, rSyls)
                                    if vocCount >= totalVs:
                                        if vocCount == totalVs:
                                            valList.append(key)
                                            # print('addVal')
                                        else:
                                            keyList.append(key)
                                        #print('addKey')
                            except IndexError:
                                continue
                        #print('foundthese', len(keyList), len(valList))
                    except IndexError:
                        continue
                #print('writing to file:', len(keyList), len(valList))
                if len(valList) > 0:
                    for all in keyList:
                        keyString+=(all+'^')
                    for all in valList:
                        valString+=(all+'^')
                    #print(keyString, valString)
                    dicFile.writerow([keyString[:-1], valString[:-1]])
        print('rhyDic complete')


for totalVs in range(1, 11):
    for rSyls in range(1, 11):
        if rSyls <= totalVs:
            rhyMaker(totalVs, rSyls)



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
