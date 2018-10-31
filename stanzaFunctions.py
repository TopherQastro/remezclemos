
import globalFunctions as gF

def veto():
    return [], ([],[]), int(0), False, False
          #stanza, qAnteLine, lineCt, rhymeThisLine, killSwitch


def removeLine(stanza):
    print('stF:', gF.lineno(), '| removeLine in | len(stanza):', len(stanza))
    if len(stanza) > 0:
        stanzaSnip = stanza.pop()  #  Remove the last line of the stanza
        gF.superBlackList[0].append(stanzaSnip[0][0])  #  Add the first word of the line to blacklist to ensure the repeat doesn't happen
        print('stF:', gF.lineno(), '| stanzaSnip:', stanzaSnip)
    print('stF:', gF.lineno(), '| removeLine', len(gF.superBlackList))
    qAnteLine = ([],[])  #  Rebuild qAnteLine, meant to direct the proceeding line(s). Returns empty if stanza empty
    if len(stanza) > 1:
        for word in stanza[-1][0]:
            qAnteLine[0].append(word)
        for word in stanza[-1][1]:
            qAnteLine[1].append(word)
    print('stF:', gF.lineno(), '| removeLine out | len(stanza):', len(stanza))
    return stanza, qAnteLine


def acceptLine(stanza, newLine):
    print('stF:', gF.lineno(), '| acceptLine in | len(stanza):', len(stanza))
    stanza.append(newLine)
    gF.superBlackList = [[]]  #  Reset superBlackList to apply to next line
    print('stF:', gF.lineno(), '| acceptLine in | len(stanza):', len(stanza))
    return stanza, newLine
          #stanza, qAnteLine


def gov():
    print('stF:', gF.lineno(), '| gov begin len(rhyMap):', len(gF.rhyMap), 
          'len(gF.empMap):', len(gF.empMap))
    stanza, qAnteLine, lineCt, rhymeThisLine, killSwitch = veto()  #  Creates a fresh stanza, no usedList
    while lineCt < len(gF.rhyMap):
        anteRhyme = lineCt
        if gF.rhySwitch == True:
            anteRhyme = gF.rhyMap.index(gF.rhyMap[lineCt])  #  Use the length of the stanza with rhyMap to determine if a previous line should be rhymed with the current
            print('stF:', gF.lineno(), '| -', anteRhyme, lineCt)
            for each in stanza:
                print(each)
            if anteRhyme < lineCt:  #  If you hit a matching letter that comes before current line, grab rhys from that line. Otherwise, go straight to forming a metered line
                rhymeLine = stanza[anteRhyme][0]  #  Find line tuple, then select the first part of the tuple
                lastWordIndex = int(-1)
                rhymeWord = rhymeLine[lastWordIndex]
                rhymeList = []
                while rhymeLine[lastWordIndex] in gF.allPunx:  #  Start from the end and bypass all punctuation
                    try:
                        lastWordIndex-=1  #  Subtraction pulls the index back until we're not looking at a puncuation mark
                        rhymeWord = rhymeLine[lastWordIndex]  #  Picking the last word
                    except IndexError:
                        print('stF:', gF.lineno(), "| iE:", rhymeLine, lastWordIndex)
                        return  [], [], True  #  killSwitch event
                print('stF:', gF.lineno(), '| rhymeWord:', rhymeWord)
                rhymeSearch = rhymeGrab(gF.empMap[lineCt], rhymeWord)
                for all in rhymeSearch:
                    rhymeList.append(all)
                rhyInt = 0
                while rhyInt <= 3:
                    rhymeSearch = rhymeGrab(gF.empMap[lineCt], rhymeWord+'('+str(rhyInt)+')')
                    for each in rhymeSearch:
                        rhymeList.append(each)
                    rhyInt+=1
                rhymeThisLine = True
                if len(rhymeList) > 0:  #  Ensure that this produced some rhymes
                    print('stF:', gF.lineno(), '| rhymer', rhymeWord, '|', rhymeList)
                    newLine, killSwitch = gF.lineFunk.gov(gF.empMap[lineCt], rhymeThisLine, rhymeList, qAnteLine)  #  If so, we try to create rhyming lines
                else:  #  Our lines created nothing, so we hit a killSwitch event
                    return [], [], True
            else:  #  Then you don't need rhymes
                rhymeList = []
                print('stF:', gF.lineno(), '| -', qAnteLine, gF.usedList, False, rhymeList, gF.empMap[lineCt])
                newLine, killSwitch = gF.lineFunk.gov(gF.empMap[lineCt], False, rhymeList, qAnteLine)  #
        elif gF.metSwitch == False:
            newLine, killSwitch = plainLinerLtoR(qAnteLine,  rhymeList, gF.empMap[lineCt])
        else:
            print('stF:', gF.lineno(), '| - lineGov')
            newLine, killSwitch = gF.lineFunk.gov(gF.empMap[lineCt], rhymeThisLine, [], qAnteLine)
        if killSwitch == True:  #  Not an elif because any of the above could trigger this; must be separate if statement
            print('stF:', gF.lineno(), '| - killSwitch')
            if (anteRhyme < lineCt) and (gF.rhySwitch == True):  #  This line cuts back to the rhyming line to try another
                while len(stanza) > anteRhyme:
                    print('stF:', gF.lineno(), 'removing rhyLine from: ', stanza)
                    stanza, qAnteLine = removeLine(stanza)
                print('stF:', gF.lineno(), stanza)
            else:
                print('stF:', gF.lineno(), 'regular line remove: ', stanza)
                stanza, qAnteLine = removeLine(stanza)
        elif len(newLine[1]) > 0:  #  Line-building functions will either return a valid, nonzero-length line, or trigger a subtraction in the stanza with empty list
            print('stF:', gF.lineno(), '| - newLine:', newLine)
            stanza, qAnteLine = acceptLine(stanza, newLine)
        elif len(stanza) > 0:  #  Check if the stanza is nonzero-length, otherwise there's nothing to subtract, resulting in an error
            stanza, qAnteLine = removeLine(stanza)
        else:  #  Redundant, as the stanza should logically be vetoed already, but just to clean house
            print('stF:', gF.lineno(), '| - vetoStanza')
            #stanza, qAnteLine, gF.usedList, lineCt, rhymeThisLine, killSwitch = vetoStanza([])
            stanza, qAnteLine = removeLine(stanza)
        lineCt = len(stanza)  #  Count the length of the stanza, provided no killSwitch events occurred...
        print('stF:', gF.lineno(), 'end whileloop', lineCt)

    return stanza, killSwitch