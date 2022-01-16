
import globalFunctions as gF

def veto():
    for lists in gF.superList:
        lists = []
    gF.linesCount = int(0)
    gF.printGlobalData(([],[]))
    return [], ([],[]), False, False
          #stanza, qAnteLine, rhymeThisLine, killSwitch


def removeLine(stanza):
    print('stF:', gF.lineno(), '| removeLine in | len(stanza):', len(stanza))
    if len(stanza) > 0:
        stanzaSnip = stanza.pop()  #  Remove the last line of the stanza
        print('stF:', gF.lineno(), '| stanzaSnip:', stanzaSnip)
    print('stF:', gF.lineno(), '| removeLine')
    qAnteLine = ([],[])  #  Rebuild qAnteLine, meant to direct the proceeding line(s). Returns empty if stanza empty
    if len(stanza) > 1:
        for word in stanza[-1][0]:
            qAnteLine[0].append(word)
        for word in stanza[-1][1]:
            qAnteLine[1].append(word)
    print('stF:', gF.lineno(), '| removeLine out | len(stanza):', len(stanza))
    return stanza, qAnteLine


def acceptLine(stanza, newLine):
    print('stF:', gF.lineno(), '| acceptLine in | len(stanza):', len(stanza),
          '\nnewLine:', newLine)
    stanza.append(newLine)
    print('stF:', gF.lineno(), '| acceptLine out | len(stanza):', len(stanza))
    return stanza, newLine
          #stanza, qAnteLine


def gov():
    print('stF:', gF.lineno(), '| gov begin len(rhyMap):', len(gF.rhyMap), 'len(gF.empMap):', len(gF.empMap))
    if len(gF.firstBlackList) == 0:  #  It's only 0 when you first start the program
        for lineCount in gF.rhyMap:  #  
            gF.firstBlackList.append([])
    stanza, qAnteLine, rhymeThisLine, killSwitch = veto()  #  Creates a fresh stanza, no usedList
    while gF.linesCount < len(gF.rhyMap):
        rhymeList, qAnteFonoLine = [], []
        if gF.rhySwitch == True:
            rhymeThisLine = False
            anteRhyme = gF.rhyMap.index(gF.rhyMap[gF.linesCount])  #  Use the length of the stanza with rhyMap to determine if a previous line should be rhymed with the current
            rhymeLine = []
            print('stF:', gF.lineno(), '| -', anteRhyme, gF.linesCount)
            for lines in stanza:
                print('stF:', gF.lineno(), '|', lines)
            if anteRhyme < gF.linesCount:  #  If you hit a matching letter that comes before current line, grab rhys from that line. Otherwise, go straight to forming a metered line
                print('stF:', gF.lineno(), '| rhyme search started')
                rhymeLine += stanza[anteRhyme][0]  #  Find line tuple, then select the first part of the tuple
                qAnteFonoLine = gF.fonoFunk.fonoLiner(rhymeLine)
                rhymeWord = rhymeLine.pop()
                while rhymeWord in gF.allPunx:  #  Start from the end and bypass all punctuation
                    try:
                        rhymeWord = rhymeLine.pop()  #  Picking the last word
                    except IndexError:
                        print('stF:', gF.lineno(), "| iE:", rhymeLine)
                        return  [], True  #  killSwitch event
                print('stF:', gF.lineno(), '| rhymeWord:', rhymeWord)
                print('stF:', gF.lineno(), '| len(gF.splitText):', len(gF.splitText))
                rhymeList = gF.rhyFunk.rhyWordLister([rhymeWord])  #  Syllable length can be varied, 10 returns all
                rhymeThisLine = True
        newLine, killSwitch = gF.lineFunk.gov(gF.empMap[gF.linesCount], rhymeThisLine, rhymeList, qAnteLine, qAnteFonoLine) 
        if killSwitch == True:  #  Not an elif because any of the above could trigger this; must be separate if statement
            print('stF:', gF.lineno(), '| - killSwitch')
            stanza, qAnteLine, rhymeThisLine, killSwitch = veto()
        elif len(newLine[1]) > 0:  #  Line-building functions will either return a valid, nonzero-length line, or trigger a subtraction in the stanza with empty list
            print('stF:', gF.lineno(), '| - newLine:', newLine)
            stanza, qAnteLine = acceptLine(stanza, newLine)
        elif len(stanza) > 0:  #  Check if the stanza is nonzero-length, otherwise there's nothing to subtract, resulting in an error
            stanza, qAnteLine = removeLine(stanza)
        else:  #  Redundant, as the stanza should logically be vetoed already, but just to clean house
            print('stF:', gF.lineno(), '| - vetoStanza')
            #stanza, qAnteLine, gF.usedList, rhymeThisLine, killSwitch = vetoStanza([])
            stanza, qAnteLine, rhymeThisLine, killSwitch = veto()
        gF.linesCount = len(stanza)  #  Count the length of the stanza, provided no killSwitch events occurred...
        print('stF:', gF.lineno(), 'end whileloop', gF.linesCount)

    return stanza, killSwitch