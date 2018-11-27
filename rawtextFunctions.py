
import globalFunctions as gF

def gov():

    if gF.defaultSwitch == True:
        gF.lang = 'eng'
        gF.accent = 'USen'
        gF.empMode = 'USen-unik'
        gF.textFile = 'bibleX'
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
        gF.empMap = [[bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)],
                     [bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)],
                     [bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)],
                    #[bool(0), bool(1), bool(0), bool(0), bool(1)],
                     [bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)]]

    gF.rawText = str(open(gF.lang+'/data/textLibrary/'+gF.textFile+'.txt', 'r', 
                    encoding='utf-8').read())

    nullSpace = ''  #  Certain characters will be replaced by null character
    nullReplace = ['- \n', '-\n', '\n']  #  Hyphen at the end of lines indicates words that are broken
    whiteSpace = ' '  #  Whitespace erases characters, then whitespace shrinks itself
    whiteReplace = ['_', '^', '~', '     ', '    ', '   ', '  ']

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
        contractionFile = open(gF.lang+'/data/'+gF.accent+'/contractionList.txt', 'r')
        contractionSwitch = gF.csv.reader(open(gF.lang+'/data/'+gF.accent+'/contractionSwitches.csv', 'r+'))
        for line in contractionFile:  #  Makes a dictionary of contractions
            gF.contractionList.append(line[:-1])  #  Remove '\n' before appending
        print(gF.lineno(), 'len(contractionList):', len(gF.contractionList), 
              gF.contractionList[:10])
        try:
            for line in contractionSwitch:
                #if "'s" not in line[0]:  #  There's a problem with whether the line is a possessive or contraction of "___ is"
                gF.contDic[line[0]] = line[1]
        except IndexError:
            gF.contDic = dd(list)
        #print(gF.contDic)
        print(gF.lineno(), 'len(contractionDic):', len(gF.contDic), 
              gF.contDic["can't"], gF.contDic["don't"])

    if gF.thesSwitch == True:
        try:
            thesaurusFile = gF.csv.reader(open(gF.lang+'/data/textLibrary/textData/'
                                            +gF.textFile+'-thesaurusFile.csv', 'r'))
            print(gF.lineno(), 'loading thesDic...')
            for line in thesaurusFile:
                thesWords = line[1].split('^')
                gF.thesDic[line[0]] = []
                for all in thesWords:
                    if (len(all) > 0) and (all not in gF.allPunx) and (all != line[0]):
                        gF.thesDic[line[0]].append(all)
            
        except FileNotFoundError:
            print(gF.lineno(), 'building thesDic...')
            thesaurusFile = gF.csv.writer(open(lang+'/data/textLibrary/textData/'+gF.textFile+'-thesaurusFile.csv', 'w+'))
            for all in splitText:
                finalList = []
                try:
                    #print('\n.\n')
                    gF.thesDic[all]  #  Test to see if the thesaurus has an entry already
                except KeyError:
                    try:
                        syns = wn.synsets(all)
                        for each in syns:
                            wordData = str(each).split("'")
                            synList = [str(lemma.name()) for lemma in wn.synset(wordData[1]).lemmas()]
                            for syn in synList:
                                if (syn not in finalList) and (syn != all) and (len(syn) > 0) and (syn not in allPunx):
                                    finalList.append(syn)
                        #print('thesaurus['+all+']:', finalList)
                        gF.thesDic[all] = finalList
                        thesLine = str()
                        for each in finalList:
                            thesLine+=(each+'^')
                        thesaurusFile.writerow([all, thesLine[:-1]])
                    except ValueError:
                        print('ValueError:', all)
                        continue
                    
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
    
    gF.proxFunk.loadmakeData()