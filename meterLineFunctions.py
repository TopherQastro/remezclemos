
import globalFunctions as gF


def testMeterWord(qWord):  #  A subfunction of metPopDigester, which tests words given to it
    print('mLF:', gF.lineno(), '| testgF.empsKeyLine:', gF.soundsLine, gF.qLine, qWord)
    gF.qLine[0].append(qWord[0])
    gF.qLine[1].append(qWord[1])
    print('mLF:', gF.lineno(), '|\ngF.qLine:', gF.qLine, '\ngF.empsKeyLine:', gF.soundsLine[3])
    testAns = gF.fonoFunk.testEmps()
    return testAns
      

def gov(proxExpress):
    print('mLF:', gF.lineno(), '| gov() - gF.soundsLine:', gF.soundsLine, 'gF.qAnteLine:', gF.qAnteLine, '- gF.qLine:', gF.qLine)
    gF.stopTime = gF.time.time()
    killSwitch = False
    # if gF.stopTime > (gF.startTime + 300):
    #     gF.startTime = gF.time.time()
    #     gF.stopTime = gF.time.time() + 300
    #     gF.qLine = gF.lineFunk.veto(str())
    #     print('mLF:', gF.lineno(), gF.soundsLine, gF.qLine)
    #     print('mLF:', gF.lineno(), '| gov() - timeout restart:', str(gF.time.ctime())[11:20])
    #     return gF.qLine, True  #  gF.qLine, killSwitch
    runLine = gF.lineFunk.makeYLine(gF.qAnteLine, ([],[]))
    while gF.soundsLine[3] != gF.empsKeyLine:
        print('mLF:', gF.lineno(), '| gov() while0 start', gF.qLine, gF.soundsLine[3])
        print('mLF:', gF.lineno(), '| gov() - gF.soundsLine[3] check:', gF.soundsLine[3])
        result = False
        if (len(gF.superList[1]) == 0) and (len(gF.qLine[0]) == 0):  #  Check if we're starting with a completely empty line, load firstWords to gF.superList[1] if so
            print('mLF:', gF.lineno(), '| gov() - meterGov if0')
            runLine, killSwitch = gF.lineFunk.lineStarter(proxExpress)
        print('mLF:', gF.lineno(), '| runLine:', runLine)
        popWord = gF.popFunk.popWordPicker()
        print('mLF:', gF.lineno(), '| gov() - popWord:', popWord)
        print('mLF:', gF.lineno(), '| gov() - runLine:', runLine)
        print('mLF:', gF.lineno(), '| gov() - gF.qLine:', gF.qLine)
        if (len(popWord[1]) == 0):
            if len(gF.superList[6][-1]) >= gF.proxMinDial:
                gF.proxFunk.snipProxData(proxExpress, runLine)
            elif len(gF.qLine[0]) > 0:
                runLine = gF.lineFunk.removeWordR(runLine)
            elif (len(gF.superList[1][-1]+gF.superList[0][-1]+gF.thesList[-1]+gF.contList[-1]) == 0):
                print('mLF:', gF.lineno(), '| gov() - gF.qLine and popLists out')
                return True  # killSwitch
        else:
            # if popWord[1] in gF.doubles:
            #     doubInt = int(0)
            #     popWord = (popWord[0]+'(0)', popWord[1]+'(0)')
            #     fonoResult = 'gotIt'
            #     while fonoResult == 'gotIt':
            #         print('mLF:', gF.lineno(), '| ', popWord, doubInt, str(doubInt))
            #         gF.printGlobalData(gF.qLine)
            #         popWord = (popWord[0][:-3]+'('+str(doubInt)+')', popWord[1][:-3]+'('+str(doubInt)+')')
            #         gF.superList[0][-1].append(popWord[1])  #  Insert the doubled word into the last expressList
            #         fonoResult = gF.fonoFunk.addFonoLine(gF.empsKeyLine, popWord)
            #         if fonoResult != 'gotIt':
            #             popWord = (popWord[0][:-3]+'(0)', popWord[1][:-3]+'(0)')
            #             fonoResult = 'gotIt'
            #             break
            #         gF.fonoFunk.subtractFonoLine(popWord)
            #         doubInt+=1
            print('mLF:', gF.lineno(), '| gov() - popWord:', popWord, '- gF.empsKeyLine:', gF.empsKeyLine, '- soundsLine[3]:', gF.soundsLine[3])
            fonoResult = gF.fonoFunk.addFonoLine(popWord)
            print('mLF:', gF.lineno(), '| gov() - popWord:', popWord, '- gF.empsKeyLine:', gF.empsKeyLine, '- soundsLine[3]:', gF.soundsLine[3])
            gF.printGlobalData()
            if gF.soundsLine[3] == gF.empsKeyLine[:len(gF.soundsLine[3])] and fonoResult != 'noInfo':
                print('mLF:', gF.lineno(), '| gov() - runLine:', runLine)
                print('mLF:', gF.lineno(), '| gov() - gF.qLine:', gF.qLine)
                killSwitch = gF.lineFunk.acceptWordR(runLine, ([popWord[0]], [popWord[1]]))
                print('mLF:', gF.lineno(), gF.qLine)
            elif fonoResult == 'gotIt' and popWord[0] not in gF.allPunx:
                gF.fonoFunk.subtractFonoLine(popWord)
        print('mLF:', gF.lineno(), '| gov() - len(gF.superList[6][-1]) > gF.proxMinDial')
        gF.printGlobalData()
        if len(gF.superList[0][-1]+gF.superList[1][-1]+gF.superList[2][-1]+
               gF.superList[3][-1]+gF.superList[4][-1]+gF.superList[5][-1]) == 0: # All popLists out
            if len(gF.superList[6][-1]) > gF.proxMinDial:
                print('mLF:', gF.lineno(), '| gov() - len(gF.superList[6][-1]) > gF.proxMinDial')
                gF.proxFunk.snipProxData(proxExpress, runLine)
            else:
                print('mLF:', gF.lineno(), '| gov() -', gF.qLine, runLine)
                runLine = gF.lineFunk.removeWordR(runLine)
        # if len(gF.superList[1]) == 0:
        #     print('mLF:', gF.lineno(), '| gov() - superPopList out, killSwitch')
        #     return ([],[]), True
        print('mLF:', gF.lineno(), '| gov() - gF.qLine:', gF.qLine, gF.soundsLine[3])
        rhymeSpot = gF.rhyMap.index(gF.rhyMap[len(gF.stanza)])
        if (gF.soundsLine[3] == gF.empsKeyLine) and (rhymeSpot < len(gF.stanza)): #  Check rhyMap to see if this is the first line in rhyming matches
            thisFonoLine = gF.fonoFunk.fonoLiner(gF.qLine)
            rhymeAns = gF.rhyFunk.rhyLiner(thisFonoLine, gF.qAnteFonoLine)
            if rhymeAns:
                print('mLF:', gF.lineno(), '| gov() - lines rhyme:', thisFonoLine, 
                      '==', gF.qAnteSoundsLine)
                return gF.qLine, False
            else:
                print('mLF:', gF.lineno(), '| gov() - lines dont rhyme:', 
                      thisFonoLine, '==', gF.qAnteSoundsLine)
                while gF.qLine[0][-1] in gF.allPunx:
                    runLine = gF.lineFunk.removeWordR(runLine)
                runLine = gF.lineFunk.removeWordR(runLine)
        print('mLF:', gF.lineno(), '| gov() - end of meterGov ifchecks', gF.qLine, gF.soundsLine[3])
        while len(gF.soundsLine[3]) > len(gF.empsKeyLine):  #  If somehow the line went over the numbered lists
            print('mLF:', gF.lineno(), '| gov() - meterGov over emps')
            runLine = gF.lineFunk.removeWordR(runLine)
        print('mLF:', gF.lineno(), '| gov() - gF.soundsLine[3]:', gF.soundsLine[3], 
              '- gF.empsKeyLine:', gF.empsKeyLine)
    return killSwitch    


            # elif len(runLine[0]) == 1 and runLine[-1] in gF.endPunx:                
            # print('mLF:', gF.lineno(), '| gov() |  if3', runLine)
            # gF.soundsLine[3], gF.qLine, runLine = gF.lineFunk.lineStarter(gF.empsKeyLine, proxExpress, ([], []))

        # try:  
        #     if len(gF.superList[1]) == 0 and len(gF.qLine[1]) == 0 and len(runLine[0]) == 0:
        #         print('mLF:', gF.lineno(), '| gov() | killSwitch')
        #         return gF.qLine, True #  killSwitch event
        # except IndexError:  #  Either the lists are empty, or they don't exist at all
        #     print('mLF:', gF.lineno(), '| gov() | iE:', gF.qLine, runLine)
        #     gF.printGlobalData(gF.qLine)
        #     return gF.soundsLine[3], gF.qLine, True #  killSwitch event