def vetoStanza(usedList):
    return [], ([],[]), [], int(0), False, False
          #stanza, qAnteLine, usedList, lineCt, redButton


def removeLine(stanza):
    print(lineno(), 'removeLine in | len(stanza):', len(stanza))
    if len(stanza) > 0:
        stanzaSnip = stanza.pop()  #  Remove the last line of the stanza
        superBlackList[0].append(stanzaSnip[0][0])  #  Add the first word of the line to blacklist to ensure the repeat doesn't happen
        print(lineno(), 'stanzaSnip:', stanzaSnip)
    print(lineno(), 'removeLine', len(superBlackList))
    qAnteLine = ([],[])  #  Rebuild qAnteLine, meant to direct the proceeding line(s). Returns empty if stanza empty
    if len(stanza) > 1:
        for word in stanza[-1][0]:
            qAnteLine[0].append(word)
        for word in stanza[-1][1]:
            qAnteLine[1].append(word)
    print(lineno(), 'removeLine out | len(stanza):', len(stanza))
    return stanza, qAnteLine


def acceptLine(stanza, newLine):
    print(lineno(), 'acceptLine in | len(stanza):', len(stanza))
    stanza.append(newLine)
    superBlackList = [[]]  #  Reset superBlackList to apply to next line
    print(lineno(), 'acceptLine in | len(stanza):', len(stanza))
    return stanza, newLine
          #stanza, qAnteLine


def stanzaGovernor(usedList):
    print(lineno(), 'stanzaGovernor begin len(rhyMap):', len(rhyMap), 'len(empMap):', len(empMap))
    expressList = []  #  A list of words that go to the front of the line. Declared and left empty, for now
    superBlackList = [[]]  #  Must be declared separate from vetoStanza because it starts empty but may hold screened words
    stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])  #  Creates a fresh stanza, no usedList
    while lineCt < len(rhyMap):
        anteRhyme = lineCt
        if rhySwitch == True:
            anteRhyme = rhyMap.index(rhyMap[lineCt])  #  Use the length of the stanza with rhyMap to determine if a previous line should be rhymed with the current
            print(lineno(), 'stanzaGov -', anteRhyme, lineCt)
            for each in stanza:
                print(each)
            if anteRhyme < lineCt:  #  If you hit a matching letter that comes before current line, grab rhys from that line. Otherwise, go straight to forming a metered line
                rhymeLine = stanza[anteRhyme][0]  #  Find line tuple, then select the first part of the tuple
                lastWordIndex = int(-1)
                rhymeWord = rhymeLine[lastWordIndex]
                rhymeList = []
                while rhymeLine[lastWordIndex] in allPunx:  #  Start from the end and bypass all punctuation
                    try:
                        lastWordIndex-=1  #  Subtraction pulls the index back until we're not looking at a puncuation mark
                        rhymeWord = rhymeLine[lastWordIndex]  #  Picking the last word
                    except IndexError:
                        print(lineno(), "iE:", rhymeLine, lastWordIndex)
                        return  [], [], True  #  redButton event
                print(lineno(), 'stanzaGov - rhymeWord:', rhymeWord)
                rhymeSearch = rhymeGrab(empMap[lineCt], rhymeWord)
                for all in rhymeSearch:
                    rhymeList.append(all)
                rhyInt = 0
                while rhyInt <= 3:
                    rhymeSearch = rhymeGrab(empMap[lineCt], rhymeWord+'('+str(rhyInt)+')')
                    for each in rhymeSearch:
                        rhymeList.append(each)
                    rhyInt+=1
                rhymeThisLine = True
                if len(rhymeList) > 0:  #  Ensure that this produced some rhymes
                    print(lineno(), 'stanzaGov - rhymer', rhymeWord, '|', rhymeList)
                    newLine, redButton = lineGovernor(empMap[lineCt], rhymeThisLine, rhymeList, qAnteLine)  #  If so, we try to create rhyming lines
                else:  #  Our lines created nothing, so we hit a redbutton event
                    return [], [], True
            else:  #  Then you don't need rhymes
                rhymeList = []
                print(lineno(), 'stanzaGov -', qAnteLine, usedList, False, rhymeList, empMap[lineCt])
                newLine, redButton = lineGovernor(empMap[lineCt], False, rhymeList, qAnteLine)  #
        elif metSwitch == False:
            newLine, redButton = plainLinerLtoR(qAnteLine, usedList, rhymeList, empMap[lineCt])
        else:
            print(lineno(), 'stanzaGov - lineGov')
            newLine, redButton = lineGovernor(empMap[lineCt], rhymeThisLine, [], qAnteLine)
        if redButton == True:  #  Not an elif because any of the above could trigger this; must be separate if statement
            print(lineno(), 'stanzaGov - redButton')
            if (anteRhyme < lineCt) and (rhySwitch == True):  #  This line cuts back to the rhyming line to try another
                while len(stanza) > anteRhyme:
                    print(lineno(), 'removing rhyLine from: ', stanza)
                    stanza, qAnteLine = removeLine(stanza)
                print(lineno(), stanza)
            else:
                print(lineno(), 'regular line remove: ', stanza)
                stanza, qAnteLine = removeLine(stanza)
        elif len(newLine[1]) > 0:  #  Line-building functions will either return a valid, nonzero-length line, or trigger a subtraction in the stanza with empty list
            print(lineno(), 'stanzaGov - newLine:', newLine)
            stanza, qAnteLine = acceptLine(stanza, newLine)
        elif len(stanza) > 0:  #  Check if the stanza is nonzero-length, otherwise there's nothing to subtract, resulting in an error
            stanza, qAnteLine = removeLine(stanza)
        else:  #  Redundant, as the stanza should logically be vetoed already, but just to clean house
            print(lineno(), 'stanzaGov - vetoStanza')
            #stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])
            stanza, qAnteLine = removeLine(stanza)
        lineCt = len(stanza)  #  Count the length of the stanza, provided no redButton events occurred...
        print(lineno(), 'end whileloop', lineCt)

    return stanza, usedList, redButton