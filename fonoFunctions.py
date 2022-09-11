import globalFunctions as gF

def loadFonoWordData(newWord, checkInitial):
    fonoLine, vocsLine, consLine, empsLine = gF.soundsLine
    print('fnF:', gF.lineno(), empsLine)
    try:
        if gF.fonoSwitch == True:
            fonoLine+=gF.fonoDics[gF.soundDicsIndex[checkInitial]][newWord]
        if gF.vocsSwitch == True:    
            vocsLine+=gF.vocsDics[gF.soundDicsIndex[checkInitial]][newWord]
        if gF.consSwitch == True:
            consLine+=gF.consDics[gF.soundDicsIndex[checkInitial]][newWord]
        if gF.empsSwitch == True:
            presentEmpsLen = len(empsLine)
            if '(' in newWord:
                quantumCheck = newWord[:-3]
            else:
                quantumCheck = newWord
            if quantumCheck in gF.quantumList:
                print('fnF:', gF.lineno(), 'quantumFono')
                presentEmpsLen = len(gF.soundsLine[3])
                empsLine+=gF.empsKeyLine[presentEmpsLen:presentEmpsLen+len(gF.empsDics[gF.soundDicsIndex[checkInitial]][newWord])]
                return 'gotIt'
            else:
                print('fnF:', gF.lineno(), 'not quantum')
                try:
                    empsLine+=gF.empsKeyLine[presentEmpsLen:presentEmpsLen+len(gF.empsDics[gF.soundDicsIndex[checkInitial]][newWord+'(0)'])]
                    print('fnF:', gF.lineno(), '| dupeTagged:', newWord)
                    return 'gotIt'
                except KeyError:
                    print('fnF:', gF.lineno(), 'unique sounds:', newWord)
                    empsLine+=gF.empsDics[gF.soundDicsIndex[checkInitial]][newWord]
                    return 'gotIt'
    except KeyError:
        print('fnF:', gF.lineno(), '| loadFono() - keyError - fono not found')
        print('fnF:', gF.lineno(), '| loadFono() -', newWord, empsLine)
        return 'noInfo'


def addFonoLine(pWord):
    newWord = pWord[0]
    print('fnF:', gF.lineno(), newWord, gF.soundsLine[3])
    if len(newWord) > 0:
        if newWord[0].upper() in gF.upperAlphabet:
            checkInitial = newWord[0].upper()
        else:
            checkInitial = 'Q'
        print('fnF:', gF.lineno(), '| addFonoLine() - loading fonoInfo')
        fonoLoad = loadFonoWordData(newWord, checkInitial)
    else:
        return 'noInfo'
    if fonoLoad == 'noInfo':
        gF.soundCursor.execute("SELECT * FROM mastFono"+checkInitial+" WHERE word=?", (newWord,))
        print('fnF:', gF.lineno(), '| addFonoLine()', gF.soundsLine[3])
        soundInfo = gF.soundCursor.fetchone()
        print('fnF:', gF.lineno(), soundInfo)
        if soundInfo is not None:
            if gF.fonoSwitch == True:
                gF.fonoDics[gF.soundDicsIndex[checkInitial]][newWord] = soundInfo[1].split('^')
            if gF.vocsSwitch == True:
                gF.vocsDics[gF.soundDicsIndex[checkInitial]][newWord] = soundInfo[2].split('^')
            if gF.consSwitch == True:
                gF.consDics[gF.soundDicsIndex[checkInitial]][newWord] = soundInfo[3].split('^')
            if gF.empsSwitch == True:
                boolEmps = []
                if gF.empMode == 'empsFull':
                    thisEmps = soundInfo[4]
                elif gF.empMode == 'empsEven':
                    thisEmps = soundInfo[5]
                else:
                    thisEmps = soundInfo[6]
                for each in thisEmps:  #  Stored as ints because could be numbers up to 2. Change to bools
                    if each == '1':
                        boolEmps.append(bool(True))
                    else:
                        boolEmps.append(bool(False))
                gF.empsDics[gF.soundDicsIndex[checkInitial]][newWord] = boolEmps
            fonoLoad = loadFonoWordData(newWord, checkInitial)
            print('fnF:', gF.lineno(), '| found:', newWord, gF.soundsLine[3])
            return 'gotIt'
        else:    
            print('fnF:', gF.lineno(), '| noInfo:', newWord, gF.soundsLine[3])
            return 'noInfo'
    else:
        return 'gotIt'
    


def subtractFonoLine(pWord):
    newWord = pWord[0]
    print('fnF:', gF.lineno(), '| ', pWord, newWord)
    if newWord[0].upper() in gF.upperAlphabet:
        checkInitial = newWord[0].upper()
    else:
        checkInitial = "Q"
    fonoLine, vocsLine, consLine, empsLine = gF.soundsLine
    if gF.fonoSwitch == True:
        fonoLine = fonoLine[:-len(gF.fonoDics[gF.soundDicsIndex[checkInitial]][newWord])]
    if gF.vocsSwitch == True:    
        vocsLine = vocsLine[:-len(gF.vocsDics[gF.soundDicsIndex[checkInitial]][newWord])]
    if gF.consSwitch == True:
        consLine = consLine[:-len(gF.consDics[gF.soundDicsIndex[checkInitial]][newWord])]
    if gF.empsSwitch == True:
        print('fnF:', gF.lineno(), '| ', len(gF.empsDics), checkInitial, len(gF.empsDics[gF.soundDicsIndex[checkInitial]]), newWord)
        empsLine = empsLine[:-len(gF.empsDics[gF.soundDicsIndex[checkInitial]][newWord])]
    gF.soundsLine = fonoLine, vocsLine, consLine, empsLine

def testEmps():
    #print('mLF:', gF.lineno(), '| testing emps\n', gF.empsKeyLine+' & '+gF.soundsLine[3])
    if gF.soundsLine[3] <= len(gF.empsKeyLine):  #  This is to screen against an error
        if testEmps == gF.soundsLine[3][:len(testEmps)]:  #  Check if the word is valid
            #print('mLF:', gF.lineno(), '| mPD testEmp pass')
            return True
    #print('mLF:', gF.lineno(), '| mPD emps rejected')
    return False

def fonoBuild_USen():
    fonoList = "fono", "vocs", "cons", "empsFull", "empsEven", "empsUnik"
    fono, vocs, cons, empsFull, empsEven, empsUnik = gF.dd(list), gF.dd(list), gF.dd(list), gF.dd(list), gF.dd(list), gF.dd(list)
    fonoDics =  fono, vocs, cons, empsFull, empsEven, empsUnik
    fonoDicsInt = int(0)
    fullList = []
    for fonoBits in fonoList:
        print('building dic:', fonoBits)
        dataFile = gF.csv.reader(open('eng/data/USen/USen-'+fonoBits+'.csv', 'r'))
        for line in dataFile:
            #print('fnF',  gF.lineno(), '| word:', line[0], line[1])
            fonoDics[fonoDicsInt][line[0]] = line[1]
            if line[0] not in fullList:
                fullList.append(line[0])
        fonoDicsInt+=1
    print('len(vocs):', len(vocs), 'len(fono):', len(fono), 'len(fullList):', len(fullList))
    for words in fullList:
        if len(fono[words]) == 0:
            print('no fono for', words, '\n', cons[words], vocs[words])

    return fonoDics, fullList


def fonoLiner(qLine):
    fonoLine = []
    for qWords in qLine[0]:
        fonoFile = open('eng/data/USen/USen-primaryFono.txt', "r")
        fonoInt = int(1)  #  Use this to check for words with >1 pronunciations
        if '(0)' in qWords:  #  info should exist for '(1)' and above
            qWords = qWords[:-3]
        qWords = qWords.upper()  #  The file is in all caps
        fonoString = str()
        for line in fonoFile:
            if qWords+'  ' == line[0:len(qWords)+2]:
                fonoString = line[len(qWords)+2:].rstrip('\n')
                break
        fonoListFono = fonoString.split(' ')
        for fonoBits in fonoListFono:
            fonoLine.append(fonoBits)
    print('fnF:', gF.lineno(), '| fonoLine =', fonoLine)
    #input('paused')
    return fonoLine


def fonoBuild_UKen():
    fono, vocs, cons, empsFull, empsEven, empsUnik
    return fono, vocs, cons, empsFull, empsEven, empsUnik

def fonoBuild_ESes():
    fono, vocs, cons, empsFull, empsEven, empsUnik
    return fono, vocs, cons, empsFull, empsEven, empsUnik


def fonoBuild_SQLmain(fonoDics, fullList):

    print('fnF: | begin fonoSQLBuild()')

    fono, vocs, cons, empsFull, empsEven, empsUnik = fonoDics
    for letter in gF.upperAlphabet:  #  Creating SQL database grouped by initial letter
        gF.soundCursor.execute('''CREATE TABLE mastFono'''+letter+'''(word TEXT,
        fono TEXT, vocs TEXT, cons TEXT, empsFull TEXT, empsEven TEXT, empsUnik TEXT)''')

    wordCt = int(0)
    for word in fullList:
        if len(word) > 0:
            entry = word
            wordCt+=1
            print('fnF:', wordCt, word, fono[entry], vocs[entry], cons[entry], empsFull[entry], empsEven[entry], empsUnik[entry])
            if entry[0].upper() in gF.upperAlphabet:
                tableKey = entry[0].upper()
            else:
                tableKey = 'Q'
            
            try:        
                gF.soundCursor.execute('''INSERT INTO mastFono'''+tableKey+''' VALUES(?,?,?,?,?,?,?)''', 
                (word, fono[entry], vocs[entry], cons[entry], empsFull[entry], empsEven[entry], empsUnik[entry]))

            except KeyError:
                print('fnF: | fuckery:', entry)
                continue

    gF.soundConn.commit()
    #input('paused...')