
import globalFunctions as gF

def veto():
    for lists in gF.superList:
        lists = []
    gF.linesCount = int(0)
    gF.superBlackList = [[]]
    gF.printGlobalData()
    return False, False
          #rhymeThisLine, killSwitch


def removeLine():
    print('stF:', gF.lineno(), '| removeLine in | len(gF.stanza):', len(gF.stanza))
    if len(gF.stanza) > 0:
        gF.stanzaSnip = gF.stanza.pop()  #  Remove the last line of the gF.stanza
        print('stF:', gF.lineno(), '| gF.stanzaSnip:', gF.stanzaSnip)
    print('stF:', gF.lineno(), '| removeLine')
    if len(gF.qLine[1] > 0):
        return gF.stanza, q
    gF.qAnteLine = ([],[])  #  Rebuild gF.qAnteLine, meant to direct the proceeding line(s). Returns empty if gF.stanza empty
    if len(gF.stanza) > 1:
        for word in gF.stanza[-1][0]:
            gF.qAnteLine[0].append(word)
        for word in gF.stanza[-1][1]:
            gF.qAnteLine[1].append(word)
    print('stF:', gF.lineno(), '| removeLine out | len(gF.stanza):', len(gF.stanza))


def acceptLine():
    print('stF:', gF.lineno(), '| acceptLine in | len(gF.stanza):', len(gF.stanza),
          '\ngF.qLine:', gF.qLine)
    gF.stanza.append(gF.qLine)
    gF.qAnteLine = gF.qLine
    gF.fonoStanza.append(gF.fonoFunk.fonoLiner(gF.qLine))
    gF.qLine = ([],[])
    print('stF:', gF.lineno(), '| acceptLine out | len(gF.stanza):', len(gF.stanza), gF.fonoStanza)
    gF.printGlobalData()
     

def gov():
    print('stF:', gF.lineno(), '| gov begin len(rhyMap):', len(gF.rhyMap), 'len(gF.empMap):', len(gF.empMap))
    if len(gF.firstBlackList) == 0:  #  It's only 0 when you first start the program
        for lineCount in gF.rhyMap:  #  
            gF.firstBlackList.append([])
    rhymeThisLine, killSwitch = veto()  #  Creates a fresh gF.stanza, no usedList
    while gF.linesCount < len(gF.rhyMap):
        print('stF:', gF.lineno(), '| stanzaLoop begin')
        rhymeList, gF.qAnteSoundsLine = [], []
        if gF.rhySwitch == True:
            rhymeSwitch = False
            rhymeThisLine = gF.rhyMap.index(gF.rhyMap[gF.linesCount])  #  Use the length of the gF.stanza with rhyMap to determine if a previous line should be rhymed with the current
            print('stF:', gF.lineno(), '| -', rhymeThisLine, gF.linesCount)
            for lines in gF.stanza:
                print('stF:', gF.lineno(), '|', lines)
            if rhymeThisLine < gF.linesCount:  #  If you hit a matching letter that comes before current line, grab rhys from that line. Otherwise, go straight to forming a metered line
                print('stF:', gF.lineno(), '| rhyme search started')
                gF.qAnteFonoLine = gF.fonoStanza[rhymeThisLine]  #  Find line tuple, then select the first part of the tuple
                print('stF:', gF.lineno(), '| gF.anteRhymeLine =', gF.qAnteFonoLine)
                #gF.qAnteSoundsLine = gF.fonoFunk.fonoLiner(rhymeLine)
                #rhymeWord = rhymeLine.pop()
                #while rhymeWord in gF.allPunx:  #  Start from the end and bypass all punctuation
                #    try:
                #        rhymeWord = rhymeLine.pop()  #  Picking the last word
                #    except IndexError:
                #        print('stF:', gF.lineno(), "| iE:", rhymeLine)
                #        return  [], True  #  killSwitch event
                #print('stF:', gF.lineno(), '| rhymeWord:', rhymeWord)
                print('stF:', gF.lineno(), '| len(gF.splitText):', len(gF.splitText))
                rhymeList = gF.rhyFunk.rhyWordLister(gF.qAnteFonoLine)  #  Syllable length can be varied, 10 returns all
                rhymeSwitch = True
        gF.empsKeyLine = gF.empMap[gF.linesCount]
        killSwitch = gF.lineFunk.gov(rhymeSwitch, rhymeList) 
        if killSwitch == True:  #  Not an elif because any of the above could trigger this; must be separate if statement
            print('stF:', gF.lineno(), '| - killSwitch')
            rhymeSwitch, killSwitch = veto()
        elif len(gF.qLine[1]) > 0:  #  Line-building functions will either return a valid, nonzero-length line, or trigger a subtraction in the gF.stanza with empty list
            print('stF:', gF.lineno(), '| - gF.qLine:', gF.qLine)
            acceptLine()
        elif len(gF.stanza) > 0:  #  Check if the gF.stanza is nonzero-length, otherwise there's nothing to subtract, resulting in an error
            removeLine()
        else:  #  Redundant, as the gF.stanza should logically be vetoed already, but just to clean house
            print('stF:', gF.lineno(), '| - vetogF.stanza')
            #gF.stanza, gF.qAnteLine, gF.usedList, rhymeThisLine, killSwitch = vetogF.stanza([])
            rhymeSwitch, killSwitch = veto()
        gF.linesCount = len(gF.stanza)  #  Count the length of the gF.stanza, provided no killSwitch events occurred...
        print('stF:', gF.lineno(), 'end whileloop', gF.linesCount)

    return killSwitch