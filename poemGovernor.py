

def vetoPoem():
    return [], [], 0, False
          #poem, usedList, stanzaCt, redButton


def poemGovernor(usedList):  #  Outlines the parameters of the poem
    print(lineno(), 'poemGovernor initialized\n'+str(time.ctime())+'\n')
    global startTime
    startTime = time.time()
    print(rhyMap, '+', empMap, '+', usedList)
    poem, usedList, stanzaCt, redButton = vetoPoem()
    while len(poem) < stanzaQuota:
        stanza, usedList, redButton = stanzaGovernor(usedList)
        print(lineno(), 'gotStanza\n')
        writtenStanza = str()
        for each in stanza:
            thisString = str()
            for all in each[0]:
                thisString= thisString+' '+all
            for all in allPunx:
                thisString = thisString.replace(' '+all, all)  #  Get rid of whitespace character in front of puncuation
            if each == stanza[-1]:
                if stanza[-1][-1] in allPunx:  #  Make sure a mid-sentence puncuation doesn't end the last line.
                    thisString = thisString[:-1]
                thisString+='.'  #  Add a period to the last line
            for all in endPunx:
                try:
                    endPunkI = thisString.index(all)
                    thisString = thisString[:endPunkI+2]+thisString[endPunkI+2].upper()+thisString[endPunkI+3:]
                except:
                    continue
            print(thisString[1].upper()+thisString[2:])
#        input('press enter to continue')
            writtenStanza+=thisString[1].upper()+thisString[2:]+'\n'
        print('\n')
        if usedSwitch == 1:
            usedList = ['']
        if redButton == True:
            usedList, lastList, stanzaCt, redButton = vetoPoem()
        elif len(stanza) == 0 and len(poem) > 0:
            poem = poem[:-1]
        else:
            poem.append(writtenStanza)
        if len(poem) == stanzaQuota:
            return poem, usedList