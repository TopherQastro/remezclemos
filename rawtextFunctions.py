
import globalFunctions as gF

def gov():

    if gF.defaultSwitch == True:
        gF.lang = 'eng'
        gF.accent = 'USen'
        gF.empMode = 'USen-even'
        gF.textFile = 'bibleZ'
        gF.poemQuota = 100
        gF.stanzaQuota = 1
        gF.proxMinDial = int(3)
        gF.proxMaxDial = int(20)
        gF.punxDial = int(3)
        gF.usedSwitch = False
        gF.rhySwitch = True
        gF.metSwitch = True
        gF.thesSwitch = True
        gF.rhyMap = 'aa'
        gF.empMap = [[bool(0), bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)],
                     [bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)],
                     [bool(0), bool(1), bool(1), bool(0), bool(1), bool(0), bool(1)],
                    #[bool(0), bool(1), bool(0), bool(0), bool(1)],
                     [bool(1), bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)]]

    gF.rawText = str(open(gF.lang+'/data/textLibrary/'+gF.textFile+'.txt', 'r', 
                    encoding='utf-8').read())

    nullSpace = ''  #  Certain characters will be replaced by null character
    nullReplace = ['- \n', '-\n']  #  Hyphen at the end of lines indicates words that are broken
    whiteSpace = ' '  #  Whitespace erases characters, then whitespace shrinks itself
    whiteReplace = ['_', '^', '~', '\n', '     ', '    ', '   ', '  ']

    gF.rawText = gF.rawText.replace('``', '"')
    gF.rawText = gF.rawText.replace("''", '"')
    gF.rawText = gF.rawText.replace('`', "'")
    gF.rawText = gF.rawText.replace('&', ' and ')
    for all in gF.allPunx:  #  Put a space around punctuation to tokenize later
        gF.rawText = gF.rawText.replace(all, ' '+all+' ')
    for nullSpaceVictims in nullReplace:
        gF.rawText = gF.rawText.replace(nullSpaceVictims, '')
    for whiteSpaceVictims in whiteReplace:
        gF.rawText = gF.rawText.replace(whiteSpaceVictims, ' ')  
    gF.rawText = gF.rawText.lower()

    #  Tokenizes raw text, grooms into lists of words
    gF.splitText = gF.rawText.split(' ')  # The reason for placing a space between all tokens to be grabbed
    print('rtF:', gF.lineno(), '| len(gF.splitText):', len(gF.splitText))
    for splitWords in gF.splitText:
        if len(splitWords) > 0:
            if splitWords[0] in gF.lowerAlphabet:
                gF.splitDics[gF.lowerAlphabet.index(splitWords[0])].append(splitWords)
            else:
                gF.splitDics[gF.lowerAlphabet.index('q')].append(splitWords)


    #$input('paused...')

    #  Prepares switches to contractions
    if gF.contSwitch == True:
        gF.altFunk.contractionLoad()

    if gF.thesSwitch == True:
       gF.dynaFunk.thisThesLoad()
                    
    gF.emps = gF.globalOpen(gF.lang+'/data/'+gF.accent+'/empDic-'
                                     +gF.empMode+'.csv', 'lista')
    for key, val in gF.emps.items():  #  Stored as ints because could be numbers up to 2. Change to bools
        boolSwitch = []
        for each in val:
            if each == '1':
                boolSwitch.append(bool(True))
            else:
                boolSwitch.append(bool(False))
        gF.emps[key] = boolSwitch
    gF.vocs = gF.globalOpen(gF.lang+'/data/'+gF.accent+
                              '/vocDic-USen-MAS.csv', 'lista')
    gF.cons = gF.globalOpen(gF.lang+'/data/'+gF.accent+
                              '/conDic-USen-MAS.csv', 'lista')
    gF.fono = gF.globalOpen(gF.lang+'/data/'+gF.accent+
                              '/fonDic-USen-MAS.csv', 'lista')
    print(gF.lineno(), 'len(emps):', len(gF.emps))

    print(gF.lineno(), 'opening doubles')
    for key, val in gF.emps.items():
        if '(' in key:
            gF.doubles.append(key[:-3])
        else:
            gF.doubles.append(key)

    print(gF.lineno(), "rhySwitch =", gF.rhySwitch)

    gF.fono_file = 'eng/data/USen/USen_fonoDB.sqlite'    # name of the sqlite database file
    gF.fonoConn = gF.sqlite3.connect(gF.fono_file)
    gF.fonoCursor = gF.fonoConn.cursor()

    gF.prox_file = gF.lang+'/data/textLibrary/textData/'+gF.textFile+'_prox.sqlite'    # name of the sqlite database file
    gF.proxConn = gF.sqlite3.connect(gF.prox_file)
    gF.proxCursor = gF.proxConn.cursor()
    
    gF.proxFunk.loadmakeData()


def lineToString(pLine):
    pString = str()
    for each in pLine:
        pString+=str(each)+' '
    for each in silentPunx:
        if each in pString:
            pString.replace(' '+each, each)
   #$ print('line2Str:', pString)
    return pString
    
def stringToLine(pString):
    for all in silentPunx:
        if all in pString:
            pString = pString.replace(all, ' '+all)
    pLine = pString.split(' ')
    while '' in pLine:
        pLine.remove('')
   #$ print('str2Line:', pLine)
    return pLine

