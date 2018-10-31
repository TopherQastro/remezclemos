
import globalFunctions as gF

def veto():
    return [], [], 0, False
          #poem, gF.usedList, stanzaCt, killSwitch


def gov():  #  Outlines the parameters of the poem
    print('poF:', gF.lineno(), 'poemGovernor initialized\n'+str(gF.time.ctime())+'\n')
    print(gF.rhyMap, '+', gF.empMap, '+', len(gF.usedList))
    poem, gF.usedList, stanzaCt, killSwitch = veto()
    while len(poem) < gF.stanzaQuota:
        stanza, gF.usedList, killSwitch = gF.stanzaFunk.gov()
        print('poF:', gF.lineno(), 'gotStanza\n')
        writtenStanza = str()
        for each in stanza:
            thisString = str()
            for all in each[0]:
                thisString= thisString+' '+all
            for all in gF.allPunx:
                thisString = thisString.replace(' '+all, all)  #  Get rid of whitespace character in front of puncuation
            if each == stanza[-1]:
                if stanza[-1][-1] in gF.allPunx:  #  Make sure a mid-sentence puncuation doesn't end the last line.
                    thisString = thisString[:-1]
                thisString+='.'  #  Add a period to the last line
            for all in gF.endPunx:
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
            gF.usedList = ['']
        if killSwitch == True:
            gF.usedList, lastList, stanzaCt, killSwitch = veto()
        elif len(stanza) == 0 and len(poem) > 0:
            poem = poem[:-1]
        else:
            poem.append(writtenStanza)

    return poem