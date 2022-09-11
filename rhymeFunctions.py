
#  This next section was organized as follows:
##  tVocs (or, 't') = 

import globalFunctions as gF

softRhySwitches = {'G':'K', 'D':'T', 'S':'TH', 'JH':'CH', 'F':'V'}  #  Voiced/unvoiced constantants (See: Korean language)
fCons = 'B', 'D', 'G', 'JH', 'L', 'N', 'P', 'S', 'T', 'V', 'ZH', 'CH', 'DH', 'F', 'HH', 'K', 'M', 'NG', 'R', 'SH', 'TH', 'W', 'Z'
fVocs = ['AA', 'AH', 'AW', 'EH', 'EY', 'IH', 'OW', 'UH', 'AE', 'AO', 'AY', 'ER', 'IY', 'OY', 'UW', 'Y']
            

def rhyLinePrep(rawRhyLine):  #  Prepares the line to be analyzed for potential rhyming patterns
    refinedRhyLine = []
    for fonoBits in rawRhyLine:
        fonoBits = fonoBits.replace('0', '')
        fonoBits = fonoBits.replace('1', '')
        fonoBits = fonoBits.replace('2', '')
        if gF.consMode == 'softRhy':  #  Consonant sounds that sound similar
            for key, val in softRhySwitches.items():
                fonoBits = fonoBits.replace(key, val)  #  Changes the cons to their matches, equalizing them
        elif gF.consMode == 'ignore':
            gF.rCons = 0
            for cons in fCons:
                if cons in fonoBits:
                    fonoBits.remove(cons)
        #else:  It's 'fullList'
        #print('ryF: |', gF.lineno(), ' fonoBits: ', fonoBits)
        refinedRhyLine.append(fonoBits)
    return refinedRhyLine


def rhyLiner(fonoLine0, fonoLine1):
    print('ryF: |', 'rhyLiner0(', '\nfonoLine0:', fonoLine0, '\nfonoLine1:', fonoLine1)
    rhymeAns = False  #  So that the variable is declared False if it never hits a 'return True'
    rhyLine0 = rhyLinePrep(fonoLine0)
    rhyLine1 = rhyLinePrep(fonoLine1)
    theseSyls, theseCons = int(0), int(0)  #  Resets counts as every new word is processed
    while (len(rhyLine0) > 0) and (len(rhyLine1) > 0):
        rhyLine0bit = rhyLine0.pop()
        rhyLine1bit = rhyLine1.pop()
        print('ryF: |', gF.lineno(), ' ', rhyLine0bit, 'v.', rhyLine1bit)
        if rhyLine0bit == rhyLine1bit:
            print('ryF: |', gF.lineno(), rhyLine0bit)
            if rhyLine0bit in fVocs:
                print('ryF: |', gF.lineno(), ' sylsMatch')
                theseSyls+=1 
                if theseSyls >= gF.rSyls:  #  If we find the number of syllables necessary
                    rhymeAns = True
                    break
            else:
                theseCons+=1
                print('ryF: |', gF.lineno(), ' consMatch', theseCons, gF.rCons)
        elif (rhyLine0bit in fCons) or (rhyLine1bit in fCons):
            if gF.rCons > theseCons:  #  If we haven't surpassed the minimum consonant count, break without adding
                print('ryF: |', gF.lineno(), ' consBreak')
                break
            else:
                try:
                    while rhyLine0bit in fCons:
                        rhyLine0bit = rhyLine0.pop()
                    while rhyLine1bit in fCons:
                        rhyLine1bit = rhyLine1.pop()
                    print('ryF: |', gF.lineno(), ' newPops:', rhyLine0bit, rhyLine1bit)
                    if rhyLine0bit == rhyLine1bit:
                        print('ryF: |', gF.lineno(), ' sylsMatch')
                        theseSyls+=1
                        if theseSyls >= gF.rSyls:  #  If we find the number of syllables necessary
                            rhymeAns = True
                            break
                    elif (rhyLine1bit in fVocs) or (rhyLine1bit in fVocs):
                        rhymeAns = False
                        break
                except IndexError:
                    print('ryF: |', gF.lineno(), ' ran out', rhyLine0, '-', rhyLine1)
                    rhymeAns = False
                    break
        else:
            print('ryF: |', gF.lineno(), ' mismatched, cancelled')
            rhymeAns = False
            break
    print('ryF: |', gF.lineno(), '| rhymeLiner out - rhymeAns =', rhymeAns)
    return rhymeAns



def rhyWordLister(rhyFonoLine):  #  This finds any words that rhyme to be placed in the expressList later    
    print('ryF: |', gF.lineno(), '| rhyWordLister(', rhyFonoLine, ')')
    rhyListFono = rhyLinePrep(rhyFonoLine)
    #fonoFile = open('eng/data/USen/USen-primaryFono.txt', "r")
    #for line in fonoFile:
    #    if rhymeWord+'  ' == line[0:len(rhymeWord)+2]:
    #        rhymeFono = line[len(rhymeWord)+2:].rstrip('\n')
    #        break
    print('ryF: |', gF.lineno(), '| rhyListFono =', rhyListFono)    
    fonoFile = open('eng/data/USen/USen-primaryFono.txt', "r")  #  Need to reopen the file or it starts list from inputted rhymeWord
    finalRhymeList = []
    for line in fonoFile:
        rhyPopFono = []
        for rhyPoppers in rhyListFono:
            rhyPopFono.append(rhyPoppers)
        lineSplitSpot = line.index('  ')
        checkWord = line[:lineSplitSpot]
        checkFono = line[lineSplitSpot+2:].rstrip('\n')
        checkPopFono = checkFono.split(' ')
        checkPopFono = rhyLinePrep(checkPopFono)
        #print('ryF: |', gF.lineno(), ' listFono: ', checkWord, ':', checkPopFono)
        theseSyls, theseCons = int(0), int(0)  #  Resets counts as every new word is processed
        if checkWord[0] in gF.lowerAlphabet:
            checkInitial = checkWord[0].upper()
        else:
            checkInitial = 'Q'
        while (len(rhyPopFono) > 0) and (len(checkPopFono) > 0):
            checkBit = checkPopFono.pop()
            rhymeBit = rhyPopFono.pop()
            #print('ryF: |', gF.lineno(), ' ', checkBit, 'v.', rhymeBit)
            if checkBit == rhymeBit:
                if rhymeBit in fVocs:
                    #print('ryF: |', gF.lineno(), ' sylsMatch')
                    theseSyls+=1 
                    if theseSyls >= gF.rSyls:  #  If we find the number of syllables necessary
                        finalRhymeList.append(checkWord.lower())
                        #print('ryF: |', gF.lineno(), 'rhyme found:', checkWord, '\nfinalRhymeList:', finalRhymeList)
                        break
                else:
                    theseCons+=1
                    #print('ryF: |', gF.lineno(), ' consMatch', theseCons, gF.rCons)
                if (len(checkPopFono) == 0) or (len(rhyPopFono) == 0):
                    finalRhymeList.append(checkWord.lower())
                    #print('ryF: |', gF.lineno(), 'shortrhyme found:', checkWord, '\nfinalRhymeList:', finalRhymeList)
                    break
            elif (checkBit in fCons) or (rhymeBit in fCons):
                if gF.rCons >= theseCons:  #  If we haven't surpassed the minimum consonant count, break without adding
                    #print('ryF: |', gF.lineno(), ' consBreak')
                    break
                else:
                    try:
                        while checkBit in fCons:
                            checkBit = checkPopFono.pop()
                        while rhymeBit in fCons:
                            rhymeBit = rhyPopFono.pop()
                        #print('ryF: |', gF.lineno(), ' newPops:', checkBit, rhymeBit)
                        if checkBit == rhymeBit:
                            #print('ryF: |', gF.lineno(), ' sylsMatch')
                            theseSyls+=1
                            if theseSyls >= gF.rSyls:  #  If we find the number of syllables necessary
                                #print('ryF: |', gF.lineno(), 'rhyme found:', checkWord, '\nfinalRhymeList:', finalRhymeList)
                                break
                            if (len(checkPopFono) == 0) or (len(rhyPopFono) == 0):  #  If the word has no more sounds, but they all match
                                finalRhymeList.append(checkWord.lower())
                                #print('ryF: |', gF.lineno(), 'shortrhyme found:', checkWord, '\nfinalRhymeList:', finalRhymeList)
                                break
                    except IndexError:
                        #print('ryF: |', gF.lineno(), ' ran out', rhyListFono, '-', checkPopFono)
                        break
            else:
                #print('ryF: |', gF.lineno(), ' mismatched, cancelled')
                break
        
    #print('ryF: |', gF.lineno(), '| finalRhymeList:', finalRhymeList)

    return finalRhymeList

#fonoLine0 = ['AY1', 'BH', 'IY', 'GH']
#fonoLine1 = ['AY1', 'BH', 'IY', 'GH']
#rhyLiner(fonoLine0, fonoLine1)