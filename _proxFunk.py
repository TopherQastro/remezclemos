import sqlite3
import inspect
from collections import defaultdict

fono_file = 'eng/data/USen/USen_fonoDB.sqlite'    # name of the sqlite database file
fonoConn = sqlite3.connect(fono_file)
fonoCursor = fonoConn.cursor()


allPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '"', "''", '-', '\\', '+',
           '=', '/', '<', '>', '(', ')']  #  Doesn't include apostrophe, because
                                          #  that could be part of a contraction
endPunx = ['.', '!', '?']  #  To gather which words immediately thereafter should start a sentence
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def lineno():     ##  Returns the current line number in our program.
    return inspect.currentframe().f_back.f_lineno


def proxNewBuild(lang, textFile, splitText):

    prox_file = lang+'/data/textLibrary/textData/'+textFile+'_prox.sqlite'    # name of the sqlite database file
    proxConn = sqlite3.connect(prox_file)
    proxCursor = proxConn.cursor()

    proxP1, proxP2, proxP3, proxP4, proxP5, proxP6 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    proxP7, proxP8, proxP9, proxP10, proxP11, proxP12 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    proxP13, proxP14, proxP15, proxP16, proxP17, proxP18 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    proxP19, proxP20, proxP21, proxP22, proxP23, proxP24 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    proxM1, proxM2, proxM3, proxM4, proxM5, proxM6 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    proxM7, proxM8, proxM9, proxM10, proxM11, proxM12 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    proxM13, proxM14, proxM15, proxM16, proxM17, proxM18 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    proxM19, proxM20, proxM21, proxM22, proxM23, proxM24 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    #  The dictionaries are organized into lists that are accessed by index. Useful in while loops with ascending/descending numbers
    proxPlusLista = [proxP1, proxP2, proxP3, proxP4, proxP5, proxP6,
                     proxP7, proxP8, proxP9, proxP10, proxP11, proxP12,
                     proxP13, proxP14, proxP15, proxP16, proxP17, proxP18,
                     proxP19, proxP20, proxP21, proxP22, proxP23, proxP24]
    proxMinusLista = [proxM1, proxM2, proxM3, proxM4, proxM5, proxM6,
                      proxM7, proxM8, proxM9, proxM10, proxM11, proxM12,
                      proxM13, proxM14, proxM15, proxM16, proxM17, proxM18,
                      proxM19, proxM20, proxM21, proxM22, proxM23, proxM24]
    superProxLista = [proxPlusLista, proxMinusLista]

    for letter in alphabet:
        proxCursor.execute('''CREATE TABLE mastProx'''+letter+'''(word TEXT,
        proxP1 TEXT, proxP2 TEXT, proxP3 TEXT, proxP4 TEXT, proxP5 TEXT, proxP6 TEXT,
        proxP7 TEXT, proxP8 TEXT, proxP9 TEXT, proxP10 TEXT, proxP11 TEXT, proxP12 TEXT,
        proxP13 TEXT, proxP14 TEXT, proxP15 TEXT, proxP16 TEXT, proxP17 TEXT, proxP18 TEXT,
        proxP19 TEXT, proxP20 TEXT, proxP21 TEXT, proxP22 TEXT, proxP23 TEXT, proxP24 TEXT,
        proxM1 TEXT, proxM2 TEXT, proxM3 TEXT, proxM4 TEXT, proxM5 TEXT, proxM6 TEXT,
        proxM7 TEXT, proxM8 TEXT, proxM9 TEXT, proxM10 TEXT, proxM11 TEXT, proxM12 TEXT,
        proxM13 TEXT, proxM14 TEXT, proxM15 TEXT, proxM16 TEXT, proxM17 TEXT, proxM18 TEXT,
        proxM19 TEXT, proxM20 TEXT, proxM21 TEXT, proxM22 TEXT, proxM23 TEXT, proxM24 TEXT)''')

    print(lineno(), '\nNEW FILE\nbuilding firstfile...')
    firstFile = open(lang+'/data/textLibrary/textData/'+textFile+'-firstFile.txt', 'w+')
    fullList = []
    splitTIndex = int(0)
    splitTLen = len(splitText)
    print(lineno(), 'begin loadmakeProxLibs()')
    #  Prox and gramprox store Markov chains and build in -Liner() functions
    #  Libs declared here, made into lists of dics of lists, and called using indices on     #  The maximum length of theseslists are truncated based on the user's initial input
    print(lineno(), 'builing proxLibs...')
    firstWords = []
    for all in range(0, (len(proxPlusLista))):  #  Now that we've got an exhaustive list of real words, we'll create empty lists for all of them (could this get pre-empted for common words?)
        for each in splitText:
            proxPlusLista[all][each] = []
            proxMinusLista[all][each] = []
    while splitTIndex < len(splitText):  #
        print(lineno(), 'working here:', splitTIndex, splitText[splitTIndex:splitTIndex+15])
        pWord = splitText[splitTIndex]
        print(lineno(), 'p:', pWord)
        if pWord not in fullList:
            fullList.append(pWord)
        if len(pWord) > 0:
            try:
                tablekey = pWord[0].upper()
                if tablekey not in alphabet:
                    tablekey = 'Q'
                #print(lineno(), tablekey)
                proxNumerator, proxDicCounter, proxMax = int(1), int(0), len(proxPlusLista)
                if pWord not in allPunx:
                    fonoCursor.execute('''SELECT empsEven FROM mastFono'''+tablekey+'''
                                          WHERE entry=?''', (pWord,))
                    dataCheck = fonoCursor.fetchone()[0]  #  Checks to see if valid dictionary word
                else:
                    dataCheck = 'rawr'
                if pWord in endPunx:
                    firstWord = splitText[splitTIndex+1]
                    if firstWord not in firstWords:
                        firstWords.append(firstWord)
                        firstFile.write(firstWord+'\n')
                #print(lineno(), dataCheck)
                if len(dataCheck) > 0:
                    while proxDicCounter < proxMax and splitTIndex+proxNumerator < splitTLen:
                        try:
                            proxWord = splitText[splitTIndex+proxNumerator]
                            if len(proxWord) > 0:
                                ##print(lineno(), 'prox:', proxWord)
                                tablekey = proxWord[0].upper()
                                if tablekey not in alphabet:
                                    tablekey = 'Q'
                                #print(lineno(), tablekey)
                                if len(proxWord) > 0:
                                    if proxWord not in allPunx:
                                        fonoCursor.execute('''SELECT empsEven FROM mastFono'''+tablekey+'''
                                                              WHERE entry=?''', (proxWord,))
                                        dataCheck = fonoCursor.fetchone()[0]  #  Checks to see if valid dictionary word
                                    else:
                                        dataCheck = 'rawr'
                                    #print(lineno(), dataCheck)
                                    if len(dataCheck) > 0:
                                        if proxWord not in proxPlusLista[proxDicCounter][pWord]:
                                            #print(lineno(), 'plusadd = proxP:', proxWord, 'pWord:', pWord, proxDicCounter, proxNumerator)
                                            proxPlusLista[proxDicCounter][pWord].append(proxWord)
                                        if pWord not in proxMinusLista[proxDicCounter][proxWord]:
                                            #print(lineno(), 'minusadd = proxM:', proxWord, 'pWord:', pWord, proxDicCounter, proxNumerator)
                                            proxMinusLista[proxDicCounter][proxWord].append(pWord)
                        except TypeError:
                            #print(lineno(), 'prox tE:', proxWord)
                            proxDicCounter+=1
                            proxNumerator+=1
                            continue
                        proxDicCounter+=1
                        proxNumerator+=1
            except TypeError:
                splitTIndex+=1
                #print(lineno(), splitTIndex)
                print(lineno(), 'p tE:', pWord)
                continue
            splitTIndex+=1
            if splitTIndex%1000==0:
                print(lineno(), 'prox', splitTIndex, 'of', len(splitText))       
        else:
            splitTIndex+=1

    for superProx in superProxLista:
        #print(lineno(), 'sup:', len(superProx))
        for proxLib in superProx:
            #print(lineno(), 'lib:', len(proxLib))
            for key, val in proxLib.items():
                #print(lineno(), key, val)
                proxString = str()
                for proxy in val:
                    #print(lineno(), len(val))
                    proxString = proxString+proxy+'^'  #  Entries for each proxLib are separated by the '^'
                #print(lineno(), key, proxString)
                proxLib[key] = proxString[:-1]

    for word in fullList:
        if len(word) > 0:
            print(lineno(), word)
            entry = word
            if entry[0].upper() in alphabet:
                tableKey = entry[0].upper()
            else:
                tableKey = 'Q'

            proxP1Entry, proxP2Entry, proxP3Entry, proxP4Entry, proxP5Entry, proxP6Entry = proxP1[entry], proxP2[entry], proxP3[entry], proxP4[entry], proxP5[entry], proxP6[entry]
            proxP7Entry, proxP8Entry, proxP9Entry, proxP10Entry, proxP11Entry, proxP12Entry = proxP7[entry], proxP8[entry], proxP9[entry], proxP10[entry], proxP11[entry], proxP12[entry]
            proxP13Entry, proxP14Entry, proxP15Entry, proxP16Entry, proxP17Entry, proxP18Entry = proxP13[entry], proxP14[entry], proxP15[entry], proxP16[entry], proxP17[entry], proxP18[entry]
            proxP19Entry, proxP20Entry, proxP21Entry, proxP22Entry, proxP23Entry, proxP24Entry = proxP19[entry], proxP20[entry], proxP21[entry], proxP22[entry], proxP23[entry], proxP24[entry]
            proxM1Entry, proxM2Entry, proxM3Entry, proxM4Entry, proxM5Entry, proxM6Entry = proxM1[entry], proxM2[entry], proxM3[entry], proxM4[entry], proxM5[entry], proxM6[entry]
            proxM7Entry, proxM8Entry, proxM9Entry, proxM10Entry, proxM11Entry, proxM12Entry = proxM7[entry], proxM8[entry], proxM9[entry], proxM10[entry], proxM11[entry], proxM12[entry]
            proxM13Entry, proxM14Entry, proxM15Entry, proxM16Entry, proxM17Entry, proxM18Entry = proxM13[entry], proxM14[entry], proxM15[entry], proxM16[entry], proxM17[entry], proxM18[entry]
            proxM19Entry, proxM20Entry, proxM21Entry, proxM22Entry, proxM23Entry, proxM24Entry = proxM19[entry], proxM20[entry], proxM21[entry], proxM22[entry], proxM23[entry], proxM24[entry]

            print(lineno(), proxP1Entry, proxM1Entry)
            
            try:        
                proxCursor.execute('''INSERT INTO mastProx'''+tableKey+''' (word,
                proxP1, proxP2, proxP3, proxP4, proxP5, proxP6,
                proxP7, proxP8, proxP9, proxP10, proxP11, proxP12,
                proxP13, proxP14, proxP15, proxP16, proxP17, proxP18,
                proxP19, proxP20, proxP21, proxP22, proxP23, proxP24,
                proxM1, proxM2, proxM3, proxM4, proxM5, proxM6,
                proxM7, proxM8, proxM9, proxM10, proxM11, proxM12,
                proxM13, proxM14, proxM15, proxM16, proxM17, proxM18,
                proxM19, proxM20, proxM21, proxM22, proxM23, proxM24)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                       ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (entry,
                proxP1Entry, proxP2Entry, proxP3Entry, proxP4Entry, proxP5Entry, proxP6Entry,
                proxP7Entry, proxP8Entry, proxP9Entry, proxP10Entry, proxP11Entry, proxP12Entry,
                proxP13Entry, proxP14Entry, proxP15Entry, proxP16Entry, proxP17Entry, proxP18Entry,
                proxP19Entry, proxP20Entry, proxP21Entry, proxP22Entry, proxP23Entry, proxP24Entry,
                proxM1Entry, proxM2Entry, proxM3Entry, proxM4Entry, proxM5Entry, proxM6Entry,
                proxM7Entry, proxM8Entry, proxM9Entry, proxM10Entry, proxM11Entry, proxM12Entry,
                proxM13Entry, proxM14Entry, proxM15Entry, proxM16Entry, proxM17Entry, proxM18Entry,
                proxM19Entry, proxM20Entry, proxM21Entry, proxM22Entry, proxM23Entry, proxM24Entry))

            except KeyError:
                print(lineno(), 'fuckery:', entry)
                continue

    proxConn.commit()
    proxConn.close()


def proxGrabber(lang, textFile, thisWord):
    prox_file = lang+'/data/textLibrary/textData/'+textFile+'_prox.sqlite'    # name of the sqlite database file
    proxConn = sqlite3.connect(prox_file)
    proxCursor = proxConn.cursor()

    tablekey = thisWord[0].upper()
    if tablekey not in alphabet:
        if lang == 'eng':
            tablekey = 'Q'
        elif lang == 'esp':
            tablekey = 'K'
    proxCursor.execute('''SELECT * FROM mastProx'''+tablekey+''' WHERE word=?''', (thisWord,))
    proxInfo = proxCursor.fetchone()[1:]
    return proxInfo
