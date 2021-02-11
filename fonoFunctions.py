
import globalFunctions as gF

#  Place the code that scrapes and builds rawData from languages
def fonoBuild_USen():
    fonoList = "fono", "vocs", "cons", "empsFull", "empsEven", "empsUnik"
    fono, vocs, cons, empsFull, empsEven, empsUnik = gF.dd(list), gF.dd(list), gF.dd(list), gF.dd(list), gF.dd(list), gF.dd(list)
    fonoDics =  fono, vocs, cons, empsFull, empsEven, empsUnik
    fonoDicsInt = int(0)
    fullList = []
    for fonoBits in fonoList:
        thisDict = fonoDics[fonoDicsInt]
        dataFile = gF.csv.reader(open('eng/data/USen/USen-'+fonoBits+'.csv', 'r'))
        for line in dataFile:
            print('fnF | word:', line[0], line[1])
            thisDict[line[0]] = line[1]
            if line[0] not in fullList:
                fullList.append(line[0])
        fonoDicsInt += 1
    return fonoDics, fullList

def fonoBuild_UKen():
    fono, vocs, cons, empsFull, empsEven, empsUnik
    return fono, vocs, cons, empsFull, empsEven, empsUnik

def fonoBuild_ESes():
    fono, vocs, cons, empsFull, empsEven, empsUnik
    return fono, vocs, cons, empsFull, empsEven, empsUnik


def fonoBuild_SQLmain(fonoDics, fullList):

    print('fnF:', gF.lineno(), ' | begin fonoSQLBuild()')

    fono, vocs, cons, empsFull, empsEven, empsUnik = fonoDics
    for letter in gF.upperAlphabet:  #  Creating SQL database grouped by initial letter
        gF.fonoCursor.execute('''CREATE TABLE mastFono'''+letter+'''(word TEXT,
        fono TEXT, vocs TEXT, cons TEXT, empsFull TEXT, empsEven TEXT, empsUnik TEXT)''')


    for word in fullList:
        if len(word) > 0:
            print('pxF:', gF.lineno(), word)
            entry = word
            if entry[0].upper() in gF.upperAlphabet:
                tableKey = entry[0].upper()
            else:
                tableKey = 'Q'
            
            try:        
                gF.fonoCursor.execute('''INSERT INTO mastProx'''+tableKey+''' (word,
                fono TEXT, vocs TEXT, cons TEXT, empsFull TEXT, empsEven TEXT, empsUnik TEXT)
                VALUES(?,?,?,?,?,?,?,?,?)''', (word, fono[entry], vocs[entry], cons[entry], 
                empsFull[entry], empsEven[entry], empsUnik[entry]))

            except KeyError:
                print('pxF:', gF.lineno(), ' | fuckery:', entry)
                continue

    gF.fonoConn.commit()
    input('paused...')



def gpDataWriter(lang, allDics, strBit, textFile):
    pFile = csv.writer(open(lang+'/data/textLibrary/textData/'+textFile+'-'+strBit+'.csv', 'w+'))
    print('building: data/textLibrary/textData/'+textFile+'-'+strBit+'.csv')
    gpDic = {}
    gpEntr = str()
    #$print('gF:', lineno(), '| len(allDics):', len(allDics))
    #print(allDics[0])
    for dicIndex in range(0, 19):
        if dicIndex == 0:
            for key, val in allDics[0].items():
                for each in val:
                    gpEntr=gpEntr+each+'^'
                gpDic[key] = gpEntr[:-1]+'~'
                #$print('gF:', lineno(), '|', gpEntr)
        else:
            try:
                for each in allDics[dicIndex]:
                    for key, val in each.items():
                        gpEntr = str()
                        for each in val:
                            gpEntr=gpEntr+each+'^'
                            #$print('gF:', lineno(), '| gpEntr:', len(gpEntr))
                        gpDic[key] = gpDic[key]+gpEntr[:-1]+'~'
            except KeyError:
                print('kE datawriter:', pWord)
                continue
    for key, val in gpDic:
        pFile.writerow([pWord, gpEntr])

   
def dataWriter(lang, lista, libInt, strBit, textFile):
    print(lista, libInt, strBit, textFile)
    pFile = csv.writer(open(lang+'/data/textLibrary/textData/'+textFile+'-'+strBit+str(libInt+1)+'.csv', 'w+'))
    yaWrote = []
    for key, val in lista[libInt].items():
        svVal = str()
        for each in val:
            totChk = val.count(each)
            if (totChk >= 2) and (each not in yaWrote):
                svVal+=(each+'^')
                yaWrote.append(each)
        pFile.writerow([key, svVal[:-1]])


def globalOpen(name, mode):

    lib = {}

    libFile = csv.reader(open(name, 'r+', encoding='utf-8'))
    
    for line in libFile:
        if line != []:
            if mode == 'lista':
                lib[line[0]] = list(line[1])
            elif mode == 'string':
                lib[line[0]] = str(line[1])
    doubSame = int(0)
    doubDiff = int(0)
    yaFound = []
    newAdds = {}  #  This section will find words with multiple pronounciations and create an entry to avoid KeyErrors later
    for key, val in lib.items():
        if '(' in key and key[:-3] not in yaFound:
            diffInt = int(0)
            diffEmps = []
            try:
                while diffInt < 5:
                    diffEmps.append(lib[key[:-3]+'('+str(diffInt)+')'])
                    diffInt+=1
            except KeyError:
                try:
                    diffInt = len(diffEmps)
                    while diffInt > 0:
                        diffInt-=1
                        if lib[key[:-3]+'('+str(diffInt)+')'] != lib[key[:-3]+'(0)']:
                            #print('differnt:', lib[key[:-3]+'('+str(diffInt)+')'], lib[key[:-3]+'(0)'])
                            doubDiff+=1
                            yaFound.append(key[:-3])
                            break
                    if diffInt == 0:
                        #print('nodiff:', key[:-3])
                        newAdds[key[:-3]] = lib[key[:-3]+'(0)']
                        doubSame+=1
                        yaFound.append(key[:-3])
                    continue
                except KeyError:
                    #print('failed:', key)
                    continue
    for key, val in newAdds.items():
        lib[key] = val

    #$print('\nresults:\ndoubsame:', doubSame, '\ndoubDiff:', doubDiff)
    #input('continue...')
                
        
    return lib

def globalClose(lib, name):

    libFile = csv.writer(open("__global/__data/" + name + "File.csv", "w+", encoding='latin-1'))

    for key, val in lib.items():
        ## REMOVE NEXT LINE'S CONDITION FOR CONSBUILD ##
        if val != []:
            svData = str()
            for each in lib[key]:
                svData = svData + each
            val = svData
            libFile.writerow([key, val])


def getLineData(pLine, vocs, emps, cons, phos): # pulls all the phonetic info at once

    #  Make this into SQL calls

    # pLVocs, pLEmps, pLFono, pLCons = [], [], [], []
    # pLVocs = dataLine(pWord, vocs)
    # pLEmps = dataLine(pWord, emps)
    # pLFono = dataLine(pWord, phos)
    # pLCons = dataLine(pWord, cons)

    return fono, emps, vocs, cons


def dataLine(pLine, dic):
    pData = []
    for each in pLine:
        if each in doubList:
            print('figure out')
        if (each not in silentPunx) and (len(each) > 0):
            pData.extend(dic[each])
    return pData


def pEmpsLine(empKey, pLine):
    print('gF:', lineno(), '| pLine:', pLine)
    empLine = []
##    for all in allPunx:
##        if all in pLine:
##            pLine.remove(all)
    #empHost = pLine.split(' ')
    for eachWord in pLine:
        if '_' in eachWord:
            splitWords = eachWord.split('_')
##            for sWord in splitWords:
            theseEmps = empsLine(empKey, splitWords, emps, doubles, quantumList)
            for eachEmp in theseEmps:
                empLine.append(eachEmp)
        else:
            eWord = eachWord.lower()
            if eWord in doubles:
                try:
                    if eWord in quantumList:
                        #$print('gF:', lineno(), qW:', eWord, empLine, empKey)
                        empLine.append(empKey[len(empLine)])  #  Could be either 1 or 0, so just match empKey
                    else:
                        for each in emps[eWord]:
                            empLine.append(each)
                except KeyError:
                    try:
                        doubInt = int(0)  #  This only tries one pronounciation of a word, for the sake of ease
                        eWord = eWord+'('+str(doubInt)+')'
                        if eWord in quantumList:
                            #$print('gF:', lineno(), qW:', eWord, empLine, empKey)
                            empLine.append(empKey[len(empLine)])  #  Could be either 1 or 0, so just match empKey
                        else:
                            for each in emps[eWord]:
                                empLine.append(each)
                    except:
                        #$print('gF:', lineno(), gotfukt')
                        this = 'that'
                except IndexError:
                    #$print('gF:', lineno(), iE0', eWord)
                    try:
                        for each in emps[eWord]:
                            empLine.append(each)
                    except KeyError:
                        for each in emps[eWord+'(0)']:
                            empLine.append(each)
            elif (eachWord not in allPunx) and (len(eachWord) > 0):
                try:
                    if eWord in quantumList:
                        #$print('gF:', lineno(), qW:', eWord, empLine, empKey)
                        empLine.append(empKey[len(empLine)])  #  Could be either 1 or 0, so just match empKey
                    else:
                        for each in emps[eWord]:
                            empLine.append(each)
                except KeyError:
                    try:
                        eWord = eWord[0].upper()+eWord[1:]
                        if eWord in quantumList:  #  quantum words could be either emp
                            #$print('gF:', lineno(), qW:', eWord, empLine, empKey)
                            empLine.append(empKey[len(empLine)])  #  Just match empKey
                        else:
                            for each in emps[eWord]:
                                empLine.append(each)
                        #$print('empLine0')
                    except KeyError:
                        empLine.append('2')
                        #$print('kE empLine:', eachWord)
                        continue
                    except IndexError:
                        #$print('wut?', eWord)
                        continue
                except IndexError:
                    #$print('gF:', lineno(), iE1', eWord)
                    try:
                        for each in emps[eWord]:
                            empLine.append(each)
                    except KeyError:
                        for each in emps[eWord+'(0)']:  #  Defaults to first emps of word
                            empLine.append(each)        #  with multiple pronuciations
                            
    #$print('gF:', lineno(), gotHere', empLine)
    return empLine


fonoBuild_SQLmain(fonoBuild_USen())