import globalFunctions as gF


def loadFonoWordData(empsKeyLine, newWord, checkInitial):
    fonoLine, vocsLine, consLine, empsLine = gF.soundsLine
    try:
        if gF.fonoSwitch == True:
            fonoLine+=gF.fonoDics[gF.soundDicsIndex[checkInitial]][newWord]
        if gF.vocsSwitch == True:    
            vocsLine+=gF.vocsDics[gF.soundDicsIndex[checkInitial]][newWord]
        if gF.consSwitch == True:
            consLine+=gF.consDics[gF.soundDicsIndex[checkInitial]][newWord]
        if gF.empsSwitch == True:
            empsLine+=gF.empsDics[gF.soundDicsIndex[checkInitial]][newWord]
            if newWord in gF.quantumList:
                presentEmpsLen = len(empsLine)
                empsLine+=empsKeyLine[presentEmpsLen:presentEmpsLen+len(gF.empsDics[gF.soundDicsIndex[checkInitial]][newWord])]
            else:
                empsLine+=gF.empsDics[gF.soundDicsIndex[checkInitial]][newWord]
        gF.soundsLine = fonoLine, vocsLine, consLine, empsLine
        return gF.soundsLine
    except KeyError:
        return KeyError


def addFonoLine(empsKeyLine, pWord):
    newWord = pWord[0]
    checkInitial = pWord[0].upper()
    try:
        soundsLine = loadFonoWordData(empsKeyLine, newWord, checkInitial)
    except KeyError:
        thisFono, thisVocs, thisCons, thisEmps = str(), str(), str(), str()
        gF.fonoCursor.execute("SELECT * FROM mastFono"+checkInitial+" WHERE fono, vocs, cons,emps=?,?,?,?", 
        (thisFono, thisVocs, thisCons, thisEmps))
        thisFono, thisVocs, thisCons, thisEmps = gF.fonoCursor.fetchall()
        if gF.fonoSwitch == True:
            gF.fonoDics[gF.soundDicsIndex[checkInitial]][newWord] = thisFono.split('^')
        if gF.vocsSwitch == True:
            gF.vocsDics[gF.soundDicsIndex[checkInitial]][newWord] = thisVocs.split('^')
        if gF.consSwitch == True:
            gF.consDics[gF.soundDicsIndex[checkInitial]][newWord] = thisCons.split('^')
        if gF.empsSwitch == True:
            boolEmps = []
            for each in thisEmps:  #  Stored as ints because could be numbers up to 2. Change to bools
                if each == '1':
                    boolEmps.append(bool(True))
                else:
                    boolEmps.append(bool(False))
            gF.empsDics[gF.soundDicsIndex[checkInitial]][newWord] = boolEmps
        loadFonoWordData(empsKeyLine, newWord, checkInitial)


def subtractFonoLine(pWord):
    newWord = pWord[0]
    checkInitial = newWord[0].upper()
    fonoLine, vocsLine, consLine, empsLine = gF.soundsLine
    if gF.fonoSwitch == True:
        fonoLine = fonoLine[:-len(gF.fonoDics[gF.soundDicsIndex[checkInitial]][newWord])]
    if gF.vocsSwitch == True:    
        vocsLine = vocsLine[:-len(gF.vocsDics[gF.soundDicsIndex[checkInitial]][newWord])]
    if gF.consSwitch == True:
        consLine = consLine[:-len(gF.consDics[gF.soundDicsIndex[checkInitial]][newWord])]
    if gF.empsSwitch == True:
        empsLine = empsLine[:-len(gF.empsDics[gF.soundDicsIndex[checkInitial]][newWord])]


def testEmps(empsKeyLine):
    print('mLF:', gF.lineno(), '| testing emps\n', empsKeyLine+' & '+gF.soundsLine[3])
    if gF.soundsLine[3] <= len(empsKeyLine):  #  This is to screen against an error
        if testEmps == gF.soundsLine[3][:len(testEmps)]:  #  Check if the word is valid
            print('mLF:', gF.lineno(), '| mPD testEmp pass')
            return True
    print('mLF:', gF.lineno(), '| mPD emps rejected')
    return False