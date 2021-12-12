
from fonoFunctions import fonoLiner
import globalFunctions as gF


def testMeterWord(empsKeyLine, qLine, qWord):  #  A subfunction of metPopDigester, which tests words given to it
    print('mLF:', gF.lineno(), '| testempsKeyLine:', gF.soundsLine, qLine, qWord)
    qLine[0].append(qWord[0])
    qLine[1].append(qWord[1])
    print('mLF:', gF.lineno(), '|\nqLine:', qLine, '\nempsKeyLine:', gF.soundsLine[3])
    testAns = gF.fonoFunk.testEmps(empsKeyLine, gF.soundsLine[3])
    return testAns
      

def gov(empsKeyLine, rhymeThisLine, qLine, qAnteLine, qAnteFonoLine, proxExpress):
    print('mLF:', gF.lineno(), '| gov() - gF.soundsLine:', gF.soundsLine, 'qAnteLine:', qAnteLine, '- qLine:', qLine)
    gF.stopTime = gF.time.time()
    killSwitch = False
    if gF.stopTime > (gF.startTime + 300):
        qLine = gF.lineFunk.veto(str())
        print('mLF:', gF.lineno(), gF.soundsLine, qLine)
        print('mLF:', gF.lineno(), '| gov() - timeout restart:', str(gF.time.ctime())[11:20])
        return qLine, True  #  qLine, killSwitch
    runLine = ([],[])
    for words in qAnteLine[0]:
        runLine[0].append(words)
    for words in qAnteLine[1]:
        runLine[1].append(words)
    while gF.soundsLine[3] != empsKeyLine:
        print('mLF:', gF.lineno(), '| gov() while0 start', qLine, gF.soundsLine[3])
        print('mLF:', gF.lineno(), '| gov() - gF.soundsLine[3] check:', gF.soundsLine[3])
        result = False
        if (len(gF.superList[1]) == 0) and (len(qLine[0]) == 0):  #  Check if we're starting with a completely empty line, load firstWords to gF.superList[1] if so
            print('mLF:', gF.lineno(), '| gov() - meterGov if0')
            runLine, qLine = gF.lineFunk.lineStarter(runLine, proxExpress)
        print('mLF:', gF.lineno(), '| runLine:', runLine)
        popWord = gF.popFunk.popWordPicker(qLine)
        print('mLF:', gF.lineno(), '| gov() - popWord:', popWord)
        print('mLF:', gF.lineno(), '| gov() - runLine:', runLine)
        print('mLF:', gF.lineno(), '| gov() - qLine:', qLine)
        if (len(popWord[1]) == 0):
            if len(gF.superList[6][-1]) > gF.proxMinDial:
                gF.proxFunk.snipProxData(proxExpress, qLine, runLine)
            elif len(qLine[0]) > 0:
                qLine, runLine = gF.lineFunk.removeWordR(qLine, runLine)
            elif (len(gF.superList[1][-1]+gF.superList[0][-1]+gF.thesList[-1]+gF.contList[-1]) == 0):
                print('mLF:', gF.lineno(), '| gov() - qLine and popLists out')
                return qLine, True  #  qLine, killSwitch
        else:
            # if popWord[1] in gF.doubles:
            #     doubInt = int(0)
            #     popWord = (popWord[0]+'(0)', popWord[1]+'(0)')
            #     fonoResult = 'gotIt'
            #     while fonoResult == 'gotIt':
            #         print('mLF:', gF.lineno(), '| ', popWord, doubInt, str(doubInt))
            #         gF.printGlobalData(qLine)
            #         popWord = (popWord[0][:-3]+'('+str(doubInt)+')', popWord[1][:-3]+'('+str(doubInt)+')')
            #         gF.superList[0][-1].append(popWord[1])  #  Insert the doubled word into the last expressList
            #         fonoResult = gF.fonoFunk.addFonoLine(empsKeyLine, popWord)
            #         if fonoResult != 'gotIt':
            #             popWord = (popWord[0][:-3]+'(0)', popWord[1][:-3]+'(0)')
            #             fonoResult = 'gotIt'
            #             break
            #         gF.fonoFunk.subtractFonoLine(popWord)
            #         doubInt+=1
            print('mLF:', gF.lineno(), '| gov() - popWord:', popWord, '- empsKeyLine:', empsKeyLine, '- soundsLine[3]:', gF.soundsLine[3])
            fonoResult = gF.fonoFunk.addFonoLine(empsKeyLine, popWord)
            print('mLF:', gF.lineno(), '| gov() - popWord:', popWord, '- empsKeyLine:', empsKeyLine, '- soundsLine[3]:', gF.soundsLine[3])
            gF.printGlobalData(qLine)
            if gF.soundsLine[3] == empsKeyLine[:len(gF.soundsLine[3])] and fonoResult != 'noInfo':
                print('mLF:', gF.lineno(), '| gov() - runLine:', runLine)
                print('mLF:', gF.lineno(), '| gov() - qLine:', qLine)
                qLine, killSwitch = gF.lineFunk.acceptWordR(runLine, qLine, popWord)
                print('mLF:', gF.lineno(), qLine)
            elif fonoResult == 'gotIt':
                gF.fonoFunk.subtractFonoLine(popWord)
        print('mLF:', gF.lineno(), '| gov() - len(gF.superList[6][-1]) > gF.proxMinDial')
        gF.printGlobalData(qLine)
        if len(gF.superList[0][-1]+gF.superList[1][-1]+gF.superList[2][-1]+gF.superList[3][-1]+gF.superList[4][-1]+gF.superList[5][-1]) == 0:
            if len(gF.superList[6][-1]) > gF.proxMinDial:
                print('mLF:', gF.lineno(), '| gov() - len(gF.superList[6][-1]) > gF.proxMinDial')
                gF.proxFunk.snipProxData(proxExpress, qLine, runLine)

            else:
                print('mLF:', gF.lineno(), '| gov() -', qLine, runLine)
                qLine, runLine = gF.lineFunk.removeWordR(qLine, runLine)
        # if len(gF.superList[1]) == 0:
        #     print('mLF:', gF.lineno(), '| gov() - superPopList out, killSwitch')
        #     return ([],[]), True
        print('mLF:', gF.lineno(), '| gov() - qLine:', qLine, gF.soundsLine[3])
        if (gF.soundsLine[3] == empsKeyLine) and (rhymeThisLine == True):
            thisFonoLine = fonoLiner(qLine)
            rhymeAns = gF.rhyFunk.rhyLiner(thisFonoLine, qAnteFonoLine)
            if rhymeAns == True:
                print('mLF:', gF.lineno(), '| gov() - lines rhyme:', thisFonoLine, '==', qAnteFonoLine)
                return qLine, False
            else:
                print('mLF:', gF.lineno(), '| gov() - lines dont rhyme:', thisFonoLine, '==', qAnteFonoLine)
                while qLine[0][-1] in gF.allPunx:
                    qLine, runLine = gF.lineFunk.removeWordR(qLine, runLine)
                qLine, runLine = gF.lineFunk.removeWordR(qLine, runLine)
        print('mLF:', gF.lineno(), '| gov() - end of meterGov ifchecks', qLine, gF.soundsLine[3])
        while len(gF.soundsLine[3]) > len(empsKeyLine):  #  If somehow the line went over the numbered lists
            print('mLF:', gF.lineno(), '| gov() - meterGov over emps')
            qLine, runLine = gF.lineFunk.removeWordR(qLine, runLine)
        print('mLF:', gF.lineno(), '| gov() - gF.soundsLine[3]:', gF.soundsLine[3], '- empsKeyLine:', empsKeyLine)
    return qLine, killSwitch    


            # elif len(runLine[0]) == 1 and runLine[-1] in gF.endPunx:                
            # print('mLF:', gF.lineno(), '| gov() |  if3', runLine)
            # gF.soundsLine[3], qLine, runLine = gF.lineFunk.lineStarter(empsKeyLine, proxExpress, ([], []))

        # try:  
        #     if len(gF.superList[1]) == 0 and len(qLine[1]) == 0 and len(runLine[0]) == 0:
        #         print('mLF:', gF.lineno(), '| gov() | killSwitch == True')
        #         return qLine, True #  killSwitch event
        # except IndexError:  #  Either the lists are empty, or they don't exist at all
        #     print('mLF:', gF.lineno(), '| gov() | iE:', qLine, runLine)
        #     gF.printGlobalData(qLine)
        #     return gF.soundsLine[3], qLine, True #  killSwitch event