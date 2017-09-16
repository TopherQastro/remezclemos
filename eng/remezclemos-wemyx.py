

####

#   To-do list:
#   - ensure halfbeats are viable
#   - discriminate against capital words
#   - store unknown words into a file to be handled later
#   - create linemakers that don't follow meter

#  GLOSSARY

#  Three prefixes are used to distinguish the dual-layer lines.
#  p - May be thought as the phonetic line, or the printed line. This is what will be shown as end-product
#  q - May be thought as the quantum line, because it enjoins both p and r lines in a sort of superposition to be analyzed separately and together
#  r - May be thought as the retracted or referral line, because it shows what the pLine says alternatively

#  qLine holds two lists. Most of the time, they're the same. They could split,
#  such as when contractions need to be separated, or if there's half-beats, etc.

#  qAnteLine = The line before the one currently being built, but not mutable so it could be reloaded
#  runLine = The line before the one building, but mutable so it can be cut and appended

#  qLineIndexList - Writes the index points for qLine. Starts at highest number (furthest right in sentence) and moves toward zero.
#  proxDicIndexList - Matches with qLineIndexList. Starts at 0 to find the immediate proxList for the furthest right, then the second-right gets index 1, etc.

#  superPopList = The 'list of lists' that holds words to be examined
#  superBlackList - The 'list of lists' that hold words whose paths have already been exhausted,
#      which is necessary to ensure a loop issue of trying and failing the same paths repeatedly

#  redButton = The boolean value that triggers a veto of a line, stanza, or poem that has failed, which resets all values

#  Organization of variables: empLine, qEmpLine, superPopList, superBlackList, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qWord, qLine, qAnteLine, redButton


##########
##  declaration of libraries
##########

from string import *
import tkinter as tk
import ___gloFunk as gF # Make sure to remove underscores later
import nltk
from nltk import wordnet as wn
import random
import datetime
import time
import csv
import inspect
import shelve
from collections import defaultdict
csv.field_size_limit(int(9999999))



##########
##  basic, essential, universal functions & lists
##########


def lineno():     ##  Returns the current line number in our program.
    return inspect.currentframe().f_back.f_lineno

unknownWords = open('data/unknownWords.txt', 'a')

global quantumList
quantumList = ['was', 'be', 'and', 'to', 'for', 'a', 'the', 'in', 'at', 'but', 'an', 'not', 'is']  #  List of words used for quantum emp patterns
nonEnders = ['and', 'or', 'a', 'but', 'the', 'an', ',', ';', ':', '--']

allPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '"', "''", '-', '\\', '+', '=', '/', '<', '>', '(', ')']  #  Doesn't include apostrophe, because that could be part of a contraction
midPunx = [',', ';', ':', '--']
endPunx = ['.', '!', '?']  #  To gather which words immediately thereafter should start a sentence

bannedChops = ['@', '#', '&', '*', '\\', '+', '=', '/', '<', '>']


##########
##  text and library preparation
##########

def gpDataWriter(dicList, fileBit, textFile):

    ##  Writes grammar and proximity data to hard drive

    pFile = csv.writer(open('data/textLibrary/textData/'+textFile+'-'+fileBit+'.csv', 'w+'))
    print(lineno(), 'building: data/textLibrary/textData/'+textFile+'-'+fileBit+'.csv')
    #print(dicList)
    for key, val in dicList[0].items():
        fullString = str()
        for each in dicList:
            dicString = str()
            for entr in each[key]:
                #4 print('gpData:', entr, )
                dicString = dicString+entr+'^'  #  Entries for each proxLib are separated by the '^'
            fullString = fullString+dicString[:-1]+'~'  #  Proxlibs are separated by '~'. proxPlusLista is saved in one file.
        for char in fullString:
            if char != '~':      # This is to screen for empty sets. If one char is not a tilde then it's non-empty.
                print(lineno(), fileBit, 'writing:', key, fullString[:min(20, len(fullString))])
                pFile.writerow([key, fullString[:-1]])
                break


def loadmakeData(textFile, proxPlusLista, proxMinusLista):
    global firstWords, firstPopList
    firstWords, firstPopList = [], []
    try:
        filepath = 'data/textLibrary/textData/'+textFile+'-firstFile.txt'
        print(lineno(), 'begin fwFile load', filepath) 
        firstFile = open(filepath, 'r')
        for line in firstFile:
            firstWords.append(line[:-1])
            firstPopList.append(line[:-1])
        print(lineno(), 'begin prox load')
        #  Take a look at gpDataOpener. Consider moving more code there, or bring some here
        proxPlusLista = gF.proxDataOpener(proxPlusLista, 'proxP', textFile)
        proxMinusLista = gF.proxDataOpener(proxMinusLista, 'proxM', textFile)
        print(lineno(), 'prox load complete')
            
    except FileNotFoundError:
        firstFile = open('data/textLibrary/textData/'+textFile+'-firstFile.txt', 'w+')
        splitTIndex = int(0)
        splitTLen = len(splitText)
        proxMaxDial = 19
        print(lineno(), 'begin loadmakeProxLibs()')
        #  Prox and gramprox store Markov chains and build in -Liner() functions
        #  Libs declared here, made into lists of dics of lists, and called using indices on     #  The maximum length of theseslists are truncated based on the user's initial input
        proxPlusLista = proxPlusLista[:proxMaxDial]
        proxMinusLista = proxMinusLista[:proxMaxDial]
        firstWords = []
        for all in range(0, (len(proxPlusLista))):  #  Now that we've got an exhaustive list of real words, we'll create empty lists for all of them (could this get pre-empted for common words?)
            for each in splitText:
                proxPlusLista[all][each] = []
                proxMinusLista[all][each] = []
        while splitTIndex < len(splitText):
            pWord = splitText[splitTIndex]
            proxNumerator, proxDicCounter, proxMax = int(1), int(0), len(proxPlusLista)
            if pWord in endPunx:
                firstWord = splitText[splitTIndex+1]
                if firstWord not in firstWords:
                    firstWords.append(firstWord)
                    firstFile.write(firstWord+'\n')
            while proxDicCounter < proxMax and splitTIndex+proxNumerator < splitTLen:
                proxWord = splitText[splitTIndex+proxNumerator]
                if proxWord not in proxPlusLista[proxDicCounter][pWord]:
                    print(lineno(), 'plusadd = proxP:', proxWord, 'pWord:', pWord)
                    proxPlusLista[proxDicCounter][pWord].append(proxWord)
                if pWord not in proxMinusLista[proxDicCounter][proxWord]:
                    #4 print(lineno(), 'minusadd = proxM:', proxWord, 'pWord:', pWord)
                    proxMinusLista[proxDicCounter][proxWord].append(pWord)
                proxDicCounter+=1
                proxNumerator+=1
            splitTIndex+=1
        print(lineno(), 'writing proxLibs...')
        gpDataWriter(proxPlusLista, 'proxP', textFile)
        gpDataWriter(proxMinusLista, 'proxM', textFile)
  

def proxDataReboot(pLine):  # Recreates the proxData used in proxWords()
    pCt = int(0)
    proxNumList = []
    proxLineNumList = []
    while pCt < len(pLine):
        proxNumList.append(pCt)
        proxLineNumList.insert(0, pCt)
        pCt+=1
    pLNi = pCt
    return [proxLineNumList, pLNi, proxNumList]


def contractionAction(contraction, qLine):  #  Switches contractions between phonetic line and real/grammar line
    qLine[0]+=contraction
    qLine[1]+=contractionDic[contraction]


def rhymeGrab(pWord):
    print(lineno(), 'rhyGrab:', pWord)
##    try:
##        emps[pWord]  #  Check if the word has two pronunciations
##    except KeyError:  #  If there's only one way to say the word, no changes will be made\
##        return []
    if len(rhyDic[pWord]) == 0:  #  Means we haven't looked it up yet
        print(lineno(), 'rhymeGrab search')
        totalSyls = 1
        while totalSyls < 10:  #  Rhyming dictionary was only built up to 10 syllables
            theseSyls = rSyls  #  rSyls means the number of syllables that should match starting from right ('marination' and 'procreation' would have 2 rSyls of their 4 each)
            if totalSyls < theseSyls:  #  rSyls is a global variable, so it must be converted to be manipulated
                theseSyls = totalSyls  #  We can't have more syllables from the right than exist in the word, so reduce to totalSyls, which is all that exist in the word
            if (theseSyls <= totalSyls):
                print(lineno(), 'rhymeGrab going', theseSyls, totalSyls)
                tName, rName = str(totalSyls), str(theseSyls)  #  Turn into strings so we can open the file that we need
                if totalSyls < 10:
                    tName = '0'+tName
                if theseSyls < 10:
                    rName = '0'+rName
                try:
                    dicFile = csv.reader(open('data/USen/rhymes/rhymeLib-t'+tName+"r"+rName+".csv", "r"))  #  The rhymes are stored in a file named after their matching properties
                    for line in dicFile:
                        keyChain = line[0].split('^')
                        if pWord in keyChain:
                            print(lineno(), 'rhymes found')
                            theseRhymes = line[1].split('^')
                            for all in theseRhymes:
                                if '(' in all:  #  A doubWord
                                    rhymeWord = all[:-3]
                                else:  #  Append normally
                                    rhymeWord = all
                                if (rhymeWord not in rhyDic[pWord]) and (rhymeWord != pWord):
                                    rhyDic[pWord].append(rhymeWord)
                except IOError:
                    print(lineno(), 'ioE: rhyDic', rhyData, 'not found')
                    return str()
            totalSyls+=1
        if len(rhyDic[pWord]) == 0:  #  If, at this point, the rhyming dictionary returned nothing, we add a nonsense word so the dictionary entry is non-zero and this function won't search again
            rhyDic[pWord] = ['rhyfuckt']
    print(lineno(), 'got rhys:', rhyDic[pWord])
    burnList = []
    for all in rhyDic[pWord]:
        print(lineno(), 'rhytest:', all)
        if ('(' in pWord) and (all == pWord[:-3]):
            print(lineno(), 'rhyMatch:', all)
            burnList.append(all)
    for all in burnList:
        rhyDic[pWord].remove(all)
    print(lineno(), 'rhys for', pWord, rhyDic[pWord])
    return rhyDic[pWord]


def removeWordL(superPopList, qLine):  #  Remove the leftmost word from line
    # do something
    return data


def removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine):  #  Remove the rightmost word from line
    print(lineno(), 'removeWordR-in', qLine)
    if len(qLine[0]) == 0 and len(runLine[0]) > 0:  #  Cut runLine
        print(lineno(), "rMR - if0")
        minusWord0 = runLine[0].pop(0)  #  Since the previous line didn't yield any following line
        minusWord1 = runLine[1].pop(0)  #  minusWordX just holds whatever is getting popped
        if minusWord0 != minusWord1:  #  If there's a discrepency, such as converting contractions to uncontracted form
            print(lineno(), 'pLine/rLine discrepency')
            if "'" in minusWord1:  #  If rLine has a contraction, remove another word from other line
                minusWord0 = runLine[0].pop(0)  #  This just removes the second word of the contraction
    if len(qLine[0]) > 0:
        print(lineno(), "rMR - if1")
        minusWord0 = qLine[0].pop()  #  Remove word from first part of line
        minusWord1 = qLine[1].pop()  #  Until better method introduced, cut rLine here
        if minusWord0 != minusWord1:  #  If there's a discrepency, such as converting contractions to uncontracted form
            print(lineno(), 'pLine/rLine discrepency')
            if "'" in minusWord1:  #  If rLine has a contraction, remove another word from other line
                minusWord0 = qLine[0].pop()  #  This just removes the second word
                minusWord0 = minusWord1  #  superBlackList will be adding minusWord0 later, and we want that to be the contraction        
        #  Some sort of contractionAction function should go here
        pWEmps = gF.empsLine(pLEmps, [minusWord0], emps, doubles, quantumList)
        pLEmps = pLEmps[:-len(pWEmps)]  #  Cut emps from main line
        qLineIndexList = qLineIndexList[1:]
        proxDicIndexList = proxDicIndexList[:-1]
        superBlackList = superBlackList[:(len(qLine[1])+1)]  #  If we leave blacklisted words further down the road, they may negate an otherwise compatible sentence
        superBlackList[len(qLine[1])].append(minusWord0)  #  Add to blackList at correct point
    #superBlackList[-1].append(minusWord0)  #  To avoid a loop, prevent popList from checking branch again
    if len(superPopList) > (len(qLine[1]) + 1):  #  If we've gone further than checking the list of next words
        print(lineno(), 'rMR - snipPopList')
        superPopList = superPopList[:len(qLine[1]) + 1]
    print(lineno(), 'removeWordR-out', qLine, '| len(superPopList):', len(superPopList), '| superBlackList:', superBlackList)
    return pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine


def acceptWordL(qLine, nextWord, qLineIndexList, proxDicIndexList):  #  Add the rightmost word to line

##  INVERT THESE VALUES

    print('acceptWord:', qLine, '|', nextWord)
    pLine.append(nextWord)
    if len(proxNumList) > 0:
        proxNum = proxNumList[-1] + 1
    else:
        proxNum = 0
    proxNumList.append(proxNum)
    proxLineNum = proxLineNumList[0] + 1
    proxLineNumList.insert(0, proxLineNum)
    return qLineIndexList, proxDicIndexList, qLine


def acceptWordR(superBlackList, qLineIndexList, proxDicIndexList, qLine, nextWord):  #  Add word to right side of line
    print('acceptWordR-in:', qLine, '|', nextWord, qLineIndexList, proxDicIndexList)
    for each in nextWord[0]:
        qLine[0].append(each)
    for each in nextWord[1]:
        qLine[1].append(each)
    qLineIndexList, proxDicIndexList = proxDataBuilder(qLine, len(qLine[1]))
    if len(superBlackList) == len(qLine[1]):  #  We don't have any blackListed words that far ahead
        superBlackList.append([])
    print('acceptWordR-out:', qLine, '|', nextWord, qLineIndexList, proxDicIndexList)
    return superBlackList, qLineIndexList, proxDicIndexList, qLine


def listSorter(mainList, frontList, rearList):  # places words in the front or back of a list
    switchList = []
    for all in allPunx:
        if all in mainList:
            rearList.append(all)
    for all in rearList:
        if all in mainList:
            switchList.append(all)
            mainList.remove(all)
    for all in switchList:
        mainList.append(all)
    switchList = []
    for all in frontList:  # if word is in both front and rear lists, goes to front
        if all in mainList:
            switchList.append(all)
            mainList.remove(all)
    for all in switchList:
        mainList.insert(0, all)
    return mainList


def proxDataBuilder(qLine, limitNum):  #  Takes the qLine and builds proxData up to a certain length
    print(lineno(), 'proxDataBuilder |', qLine, limitNum)
    qLineLen = len(qLine[1])
    proxInt = int(0)  #  Starts the proxData
    qLineIndexList, proxDicIndexList = [], []
    while proxInt < len(qLine[1]) or proxInt < limitNum:  #  Creates a list of indexes and the reverse list to index proxDics
        proxDicIndexList.append(proxInt)
        qLineIndexList.insert(0, proxInt)
        proxInt+=1
    print(lineno(), qLineIndexList, proxDicIndexList)
    return qLineIndexList, proxDicIndexList


def superPopListMaker(pLEmps, superPopList, superBlackList, expressList, qLineIndexList, proxDicIndexList, qLine, runLine): #  Creates a list-of-lists to pull from
    print(lineno(), 'sPLM init | len(superPopList)', len(superPopList))
    keepList = []  #  Will return empty set upon failure
    testLine = ([],[])
    if len(runLine[0]) > 0:  #  If there's a previous line, add it into testLine
        for each in runLine[0]:
            testLine[0].append(each)
        for each in runLine[1]:
            testLine[1].append(each)
    for each in qLine[0]:
        testLine[0].append(each)
    for each in qLine[1]:
        testLine[1].append(each)
    while len(superPopList) < len(qLine[1]):  #  If we receive a line that isn't aligned with the popList
        superPopList.append([])
    print(lineno(), 'superPopMaker start |', len(superPopList), '|', testLine, 'proxData:', qLineIndexList, proxDicIndexList)
    # qLineIndexList: List of positions on the qLine
    # proxDicIndexList: List of positions for the qLine to find in proxDics
    qLineIndexList, proxDicIndexList = proxDataBuilder(testLine, len(testLine[1]))  #  Refresh proxData
    testLineLen = len(testLine[1])
    if testLineLen == 0:  #  If we've received a totally empty line, populate it with firstWords, but not directly or corrupt global bank
        print(lineno(), 'sPM - zeroLine')
        startList = firstWordSuperPopList(superBlackList)
        return startList, [[]], qLineIndexList, proxDicIndexList, qLine, runLine
              #superPopList, superBlackList, etc

    # use rWord here, make method for dealing with doubles
    print(lineno(), 'sPM - len(testLine) >= 1', qLineIndexList, proxDicIndexList)
    try:
        print(lineno(), 'sPM - this blackList:', qLine, len(superBlackList))#, superBlackList[len(qLine[1])])
        while len(qLineIndexList) > 0:
            for all in proxP1[testLine[1][-1]]:
                if all not in superBlackList[len(qLine[1])]:  #  Screen against the initial superBlackList 
                    keepList.append(all)  #  Practically an 'else' clause, because the 'if' above returns an answer
            #print(lineno(), 'sPM - this keepList:', keepList)
            if len(qLineIndexList) > 1:  #  Only keep going if we need more than 2 words analyzed
                for each in proxDicIndexList[1:]:  #  Skip first indexNum, we already found it
                    testList = proxPlusLista[each][testLine[1][qLineIndexList[each]]]  #  Scans approximate words with indexes
                    burnList = []  #  burnList holds words that don't match with mutual proxLists
                    testString = str()  #  Look for that same string in the rawText
                    #print(lineno(), each, len(superBlackList))
                    #print(lineno(), superBlackList[qLineIndexList[0]-len(runLine[0])])
                    #qLineIndexLen = len(qLineIndexList)  #  Use this to rebuild testString without words that have failed
                    for all in qLineIndexList:  #  Build a line with words already used
                        testString = testLine[1][all]+' '+testString  #  Build backwards because we trim failed lines from the front
                    for all in keepList:
                        testString+=all+' '  #  Add the new word to the string, plus a space so we don't see a false positive with a partial word ('you' mistaken for 'your')
                        if (all not in testList) or (testString not in rawText) or (all in superBlackList[len(qLine[1])]):  #  Add blackList screening later
                            burnList.append(all)  #  Screen it with a burnList so we don't delete as we iterate thru list
                        testString = testString[:-(len(all)+1)]  #  Remove the word to prepare for another testString addition
                    #print(lineno(), 'len(keepList):', len(keepList), 'len(burnList):', len(burnList))
                    if len(keepList) > 0:
                        for all in burnList:
                            keepList.remove(all)
                    else:  #  If we run out prematurely, stop iterating over the list
                        print(lineno(), 'sPLM keepList out')
                        break
            keepList = listSorter(keepList, expressList, [])
            if len(keepList) == 0:
                qLineIndexList = qLineIndexList[:-1]
                proxDicIndexList = proxDicIndexList[:-1]
                print(lineno(), 'snipping proxData', qLineIndexList, proxDicIndexList)
                if len(qLineIndexList) > 0:  #  Ensure that the line has something to check
                    if (qLineIndexList[0] > proxMinDial) and (len(qLineIndexList) < proxMinDial):  #  This keeps the chain longer than a minimum length
                        pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
                        return superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine  #  Give up
            else:
                print(lineno(), 'superPopMaker grown |', len(superPopList), '|', testLine, 'proxData:', qLineIndexList, proxDicIndexList)
                break
    except KeyError:
        print(lineno(), 'kE:', testLine, 'len(superPopList):', len(superPopList))
        unknownWords.write(testLine[1][-1])
        pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
        #qLineIndexList, proxDicIndexList = proxDataBuilder(qLine, len(qLine[0]))
        return superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
    #print(superPopList)
    #input('waiting...')
    print(lineno(), 'sPM - appendKeep', len(keepList), len(superPopList), len(testLine[1]))
    while len(superPopList) <= len(testLine[1]):  #  If we don't have a proper amount to pop from
        superPopList.append([])
    for all in keepList:
        if all not in superPopList[len(qLine[1])]:
            superPopList[len(qLine[1])].append(all)  #  If we didn't find anything, append an empty set
    return superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine


def plainPopDigester():  #  Digests words from list without regard to their syllables or meter
    return doo, doo


def empPopDigester():  #  Digests words based on the length of their syllables
    return doo, doo


def metPopDigester(empLine, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine):  #  Digests words that fit a particular meter
    print(lineno(), 'metPopDigester start', 'len(superPopList):', len(superPopList))
    expressList, contractionWords, punxList = [], [], []  #  The first creates a list of preferential words, the second holds a list of contractions
    pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)  #  Using 'p' prefix because measuring 'phonetic'
    print(lineno(), 'mPD pLEmps:', pLEmps, qLine)
    if len(superPopList) <= len(qLine[1]):
        print(lineno(), 'mPD not aligned:', "len(superPopList):", len(superPopList), qLine)
        superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(pLEmps, superPopList, superBlackList, [], qLineIndexList, proxDicIndexList, qLine, runLine)
    #elif len(superPopList) < len(qLine[1]):
        
    print(lineno(), "len(superPopList):", len(superPopList), "| len(superPopList):", len(superPopList), 'qLine:', qLine)
    while len(superPopList[len(qLine[1])]) > 0:
        print(lineno(), "len(superPopList):", len(superPopList), 'qLine:', qLine)
        #print(lineno(), 'mPD - testBlack', superBlackList[len(qLine[1])])
        pWord = superPopList[len(qLine[1])].pop(random.choice(range(0, len(superPopList[len(qLine[1])]))))  #  Used random in past, but organized lists put preferential stuff in front / superPopList[-1].index(random.choice(superPopList[-1]))
        if (pWord in contractionList) and (pWord[:-2] != "'s") and (pWord[-1] != "'") and (pWord[:2] != "o'"):  #  This line will place contractions in a special list to be switched if nothing works
            contractionWords.append(pWord)
        elif pWord in allPunx:
            punxList.append(pWord)
        if pWord not in allPunx:  #  A zero-length emps value is an unrecognized word
            testLine = []
            for each in qLine[0]:
                testLine.append(each)
            testLine.append(pWord)
            testEmps = gF.empsLine(empLine, testLine, emps, doubles, quantumList)
            if len(testEmps) <= len(empLine):  #  This is to screen against an error
                print(lineno(), 'mPD testEmp0 |', pWord)
                if testEmps == empLine[:len(testEmps)]:  #  Check if the word is valid
                    print(lineno(), 'mPD testEmp pass')
                    qWord = ([pWord], [pWord])  #  pWord is the same word unless the phonetic data doesn't match the 'real' data
                    superBlackList, qLineIndexList, proxDicIndexList, qLine = acceptWordR(superBlackList, qLineIndexList, proxDicIndexList, qLine, qWord)
                    print(lineno(), 'mPD acceptR', qLine, testEmps)
                    return testEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
        elif (len(qLine[1]) > 2):  #  We want qLine to have more than 2 words before trying punctuation because it sounds better, although it isn't necessary for function. Also, make sure to exhaust all other possibilities first
            print(lineno(), 'punxSearch', qLine[1][-(min(punxProxNum, len(qLine[1]))):])
            punxCt = int(0)
            for all in qLine[1][-(min(punxProxNum, len(qLine[1]))):]:
                if all in allPunx:  #  Will discriminate any puncuation within the designated length of punxProxNum
                    print(lineno(), 'found punk within punxProxNum:', all)
                    punxCt+=1
            if punxCt == 0:
                superBlackList, qLineIndexList, proxDicIndexList, qLine = acceptWordR(superBlackList, qLineIndexList, proxDicIndexList, qLine, ([pWord], [pWord]))
                print(lineno(), 'mPD acceptR', qLine, pLEmps)
                return pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine        

##            else:
##                ##print(lineno(), 'fuckt')
##                pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
    #  At this point, superPopList is empty, so we try either switching contractions or
    print(lineno(), "len(contractionWords):", len(contractionWords))
    if len(contractionWords) > 0:  #  If any contractions were found in the superPopList we just tried
        print(contractionWords)
        for each in contractionWords:
            contWord = contractionDic[each]
            print(lineno(), 'contraction attempt:', each, contWord)
            checkStr = isinstance(contWord, str)  #  Sometimes contWord goes thru as list instead, not sure why
            if checkStr == True:
                contLine = gF.stringToLine(contWord)  #  Dealing with a string of two words, which needs to go thru as line
                print(lineno(), 'cont stringToLine:')
            else:
                contLine = contWord
            testLine = []
            for each in qLine[0]:
                testLine.append(each)
            for each in contLine:
                testLine.append(each)
            print(lineno(), 'contLine:', contLine)
            testEmps = gF.empsLine(empLine, testLine, emps, doubles, quantumList)
            print(lineno(), testEmps, '|', empLine[:len(testEmps)])
            if len(testEmps) <= len(empLine):  #  This is to screen against an error
                print(lineno(), 'mPD testContEmp0 |', pWord, testEmps, 'len(superPopList):', len(superPopList))
                if testEmps == empLine[:len(testEmps)]:  #  Check if the word is valid
                    qWord = (contLine, [each])  #  Appending two different words to the line
                    superBlackList, qLineIndexList, proxDicIndexList, qLine = acceptWordR(superBlackList, qLineIndexList, proxDicIndexList, qLine, qWord)
                    print(lineno(), 'mPD acceptR contraction', qLine, testEmps)
                    return testEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
##                else:
##                    ##print(lineno(), 'fuckt')
##                    pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
    print(lineno(), "len(superPopList):", len(superPopList), "| len(superPopList[-1]):", len(superPopList[-1]), 'qLine:', qLine)
    if len(qLine[1]) > 0 or len(runLine[1]) > 0: #and len(qLine[1]) > proxMinDial:  #  If we have enough words, then we can remove rightmost element and metadata, then try again
        try:
            print(lineno(), 'snipLine', qLine, '|', runLine)
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(pLEmps, superPopList, superBlackList, [], qLineIndexList, proxDicIndexList, qLine, runLine)
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = metPopDigester(empLine, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            return pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
        except RuntimeError:
            return [], [[]], [[]], [], [], ([],[]), ([],[])  #  redButton situation
    else:
        print(lineno(), 'no qLine or runLine')
        return [], [[]], [[]], [], [], ([],[]), ([],[])  #  redButton situation
    print(lineno(), 'mPD end')
    return pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
          #pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine
 
        
def firstWordSuperPopList(superBlackList):  #  Creates a superPopList that reloads the global firstWords list
    print(lineno(), 'firstWordSuperPopList start')
    superPopList = [[]]
    for all in firstWords:
        if all not in superBlackList[0]:
            superPopList[0].append(all)
    print(lineno(), len(superPopList))
    return superPopList


def makeList(listA):  #  Simple function that appends all from one list to other, so they are not bound together
    [] = listB
    for all in listA:
        listB.append(all)
    return listB
        
    
##############
#  line building


def vetoLine(qAnteLine, superBlackList):  #  Resets values in a line to
    print(lineno(), 'resetLine, qAnteLine:', qAnteLine)
    runLine = ([],[])
    for each in qAnteLine[0]:  #  Re-create any qAnteLinesuperPopList, superBlackList, qLine, qLineIndexList, proxDicIndexList as a mutable variable
        runLine[0].append(each)
    for each in qAnteLine[1]:  #  Re-create any qAnteLinesuperPopList, superBlackList, qLine, qLineIndexList, proxDicIndexList as a mutable variable
        runLine[1].append(each)
    superPopList = firstWordSuperPopList(superBlackList)
    return superPopList, superBlackList, [], [], ([],[]), runLine, False
          #superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine, redButton


def plainLinerLtoR(vars):
    data
    # without rhyme or meter


def plainLinerRtoL(vars):
    data


def meterLiner(empLine, superBlackList, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine):  #
    print(lineno(), 'meterLiner start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    pLEmps, superPopList, runLine = [], [[]], ([],[])
    for each in qAnteLine[0]:  #  qAnteLine gets appended to runLine because this function will be cutting from it when it doesn't yield results
        runLine[0].append(each)
    for each in qAnteLine[1]:
        runLine[1].append(each)
    while pLEmps != empLine:  #  Keep going until the line is finished or returns blank answer
        print(lineno(), 'empLine:', empLine, 'pLEmps:', len(pLEmps), pLEmps)
        if (len(runLine[1]) == 0) and (len(qLine[1]) == 0):  #  Check if we're starting with a completely empty line, load firstWords to superPopList if so
            print(lineno(), 'met if0')
            superPopList = firstWordSuperPopList(superBlackList)
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = metPopDigester(empLine, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
            if len(superPopList[0]) == 0 and len(qLine[1]) == 0:
                print(lineno(), 'redButton == True')
                return superPopList, superBlackList, usedList, qLine, qAnteLine, True #  redButton event
        elif len(runLine[1]) > 0:  #  Checks before trying to manipulate qAnteLine just below, also loops it so it subtracts from anteLine first
            print(lineno(), 'met if1')
            while len(superBlackList) <= len(qLine[1]):  #  Make sure superBlackList is long enough to add to w/ runLine
                superBlackList.append([])
            print(lineno(), 'runLine + qLine:', qLine, ', superBlackList:', len(superBlackList))
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = superPopListMaker(pLEmps, superPopList, superBlackList, expressList, qLineIndexList, proxDicIndexList, qLine, runLine)
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = metPopDigester(empLine, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            print(lineno(), 'qLine - runLine:', qLine)
        elif len(qLine[1]) > 0:
            print(lineno(), 'met if2 qLine:', qLine, 'len(superBlackList):', len(superBlackList), 'len(superPopList):', len(superPopList))
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = superPopListMaker(pLEmps, superPopList, superBlackList, expressList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = metPopDigester(empLine, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
            if len(superPopList[0]) == 0 and len(qLine[1]) == 0:  #  Nothing seems to work
                print(lineno(), 'met if2-if')
                return superPopList, superBlackList, usedList, qLine, qAnteLine, True  #  redButton event, as nothing in the list worked
        else:  #  No runLine, no qLine, and superPopList[0] is out of firstWords
            print(lineno(), 'met if3')
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine, redButton = vetoLine(qAnteLine, superBlackList)
            return [[]], superBlackList, usedList, qLine, qAnteLine, True
        print(lineno(), 'end of meterLiner while')
        if len(qLine[1]) > 0:  #  Make sure there's a line to analyze
            print(lineno(), 'metLiner if out')
            pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)
        elif len(runLine[1]) == 0:  #  If runLine is also out, redButton
            print(lineno(), 'metLiner elif out')
            return [[]], superBlackList, usedList, qLine, qAnteLine, True
        while len(pLEmps) > len(empLine):  #  If somehow the line went over the numbered lists
            (lineno(), 'meterLiner over emps')
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = superPopListMaker(pLEmps, superPopList, superBlackList, expressList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
        if pLEmps == empLine:
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = superPopListMaker(pLEmps, superPopList, superBlackList, expressList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
            if qLine[1][-1] in nonEnders:  #  Words that don't sound good as the last word of a line, such as conjunctions without something else to connect
                pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            else:
                for all in allPunx:
                    if all in superPopList[-1]:  #  If puncuation fits, place one on the end of a line (will give the next line an easier start, too)
                        superBlackList, qLineIndexList, proxDicIndexList, qLine = acceptWordR(superBlackList, qLineIndexList, proxDicIndexList, qLine, ([all], [all]))
                        break                        
    print(lineno(), 'meterLiner out:', qLine, 'len(superPopList):', len(superPopList))
    return superPopList, superBlackList, usedList, qLine, qAnteLine, False
          #superPopList, qAnteLine, qLine, usedList, redButton
            

def rhymeLiner(empLine, superBlackList, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine):
    print(lineno(), 'rhymeLiner start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    for all in rhymeList:
        if all not in expressList:
            expressList.append(all)
    superPopList, superBlackList, usedList, qLine, qAnteLine, redButton = meterLiner(empLine, superBlackList, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)  #  First, let it build a line, then if it doesn't happen to rhyme, send it back
    print(lineno(), 'redButton:', redButton)
    if redButton == True:
        return usedList, qLine, True
    pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)
    while qLine[0][-1] not in rhymeList:  #  Unless we find a rhyme to escape this loop, it'll subtract the word every time it gets to the beginning of the loop
        print(lineno(), 'rhymeLiner w/o rhyming line')
        for each in superPopList[len(qLine[0])-1]:  #  Let's see if there was a rhyme in our popList to add. If we don't return anything, it leaves this section like an moves on, like an implied "else"
            if (each in rhymeList) and (each not in nonEnders):  #  If there's a rhyme, then we can switch out the last word for that instead
                print(lineno(), 'gotRhyme', 'len(superPopList):', len(superPopList))
                pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)  #  Remove the last 
                superBlackList, qLineIndexList, proxDicIndexList, qLine = acceptWordR(superBlackList, qLineIndexList, proxDicIndexList, qLine, ([each], [each]))
                return usedList, qLine, False  #  We've found a rhyming line, and we're done building
        if (len(qLine[1]) > 0) and (len(superPopList[len(qLine[1])-1]) > 0):  #  If it gets to this line, there was no rhyming matches
            print(lineno(), 'rhymeLiner out')
            pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)  #  Remove the last word
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine = superPopListMaker(pLEmps, superPopList, superBlackList, expressList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
            superPopList, superBlackList, usedList, qLine, qAnteLine, redButton = meterLiner(empLine, superBlackList, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)  #  Here and below, meterLiner now has an expressList with the rhyming words, to increase their preference
            if redButton == True:
                return usedList, qLine, True
        else:
            print(lineno(), 'rhymeLiner redButton')
            return usedList, qLine, True
    return usedList, qLine, False


def lineGovernor(superBlackList, qAnteLine, usedList, expressList, rhymeThisLine, rhymeList, empLine):
    print(lineno(), 'lineGovernor start', rhymeThisLine)
    superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine, redButton = vetoLine(qAnteLine, superBlackList)  #  Start with empty variables declared. This function is also a reset button if lines are to be scrapped.
    if rhymeThisLine == True:
        print(lineno(), 'len(rhymeList):', len(rhymeList))
        if (len(rhymeList) > 0):  #  This dictates whether stanzaGovernor sent a rhyming line. An empty line indicates metered-only, or else it would've been a nonzero population
            usedList, qLine, redButton = rhymeLiner(empLine, superBlackList, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
        else:
            print(lineno(), 'no rhymes')
            return superBlackList, [], ([],[]), True  #  usedList, qLine, redButton
    elif metSwitch == True:  #  If metSwitch is off, then we wouldn't have either rhyme or meter
        print(lineno(), 'lineGov - meterLiner activate')
        superPopList, superBlackList, usedList, qLine, qAnteLine, redButton = meterLiner(empLine, superBlackList, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
    else:
        print(lineno(), 'lineGov - plainLiner activate')
        usedList, qLine, redButton = plainLinerLtoR(qAnteLine, usedList, expressList, rhymeList, qLineIndexList, proxDicIndexList, empLine)
    if redButton == True:
        print(lineno(), 'lineGov - redButton')
        superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine, redButton = vetoLine(qAnteLine, superBlackList)
        return superBlackList, [], [], True
    else:
        print(lineno(), 'lineGov - last else', qLine)
        return superBlackList, usedList, qLine, False  #  usedList, qLine, redButton
            


################
#  poem building


def vetoStanza(usedList):
    return [], ([],[]), [], int(0), False, False
          #stanza, qAnteLine, usedList, lineCt, redButton


def removeLine(stanza, superBlackList):
    print(lineno(), 'removeLine in | len(stanza):', len(stanza))
    if len(stanza) > 0:
        stanzaSnip = stanza.pop()  #  Remove the last line of the stanza
        superBlackList[0].append(stanzaSnip[0][0])  #  Add the first word of the line to blacklist to ensure the repeat doesn't happen
        print(lineno(), 'stanzaSnip:', stanzaSnip)
    print(lineno(), 'removeLine', len(superBlackList))
    qAnteLine = ([],[])  #  Rebuild qAnteLine, meant to direct the proceeding line(s). Returns empty if stanza empty
    if len(stanza) > 1:
        for each in stanza[-1][0]:
            qAnteLine[0].append(each)
        for each in stanza[-1][1]:
            qAnteLine[1].append(each)
    print(lineno(), 'removeLine out | len(stanza):', len(stanza))
    return stanza, superBlackList, qAnteLine


def acceptLine(stanza, superBlackList, newLine):
    print(lineno(), 'acceptLine in | len(stanza):', len(stanza))
    stanza.append(newLine)
    superBlackList = [[]]  #  Reset superBlackList to apply to next line
    print(lineno(), 'acceptLine in | len(stanza):', len(stanza))
    return stanza, superBlackList, newLine
          #stanza, qAnteLine


def stanzaGovernor(usedList):
    print(lineno(), 'stanzaGovernor begin len(rhyMap):', len(rhyMap), 'len(empMap):', len(empMap))
    expressList = []  #  A list of words that go to the front of the line. Declared and left empty, for now
    superBlackList = [[]]  #  Must be declared separate from vetoStanza because it starts empty but may hold screened words
    stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])  #  Creates a fresh stanza, no usedList
    while lineCt < len(rhyMap):
        if rhySwitch == True:
            anteRhyme = rhyMap.index(rhyMap[lineCt])  #  Use the length of the stanza with rhyMap to determine if a previous line should be rhymed with the current
            print(lineno(), 'stanzaGov -', anteRhyme, lineCt)
            for each in stanza:
                print(each)
            if anteRhyme < lineCt:  #  If you hit a matching letter that comes before current line, grab rhys from that line. Otherwise, go straight to forming a metered line
                rhymeLine = stanza[anteRhyme][0]  #  Find line tuple, then select the first part of the tuple
                lastWordIndex = int(-1)
                rhymeWord = rhymeLine[lastWordIndex]
                while rhymeLine[lastWordIndex] in allPunx:  #  Start from the end and bypass all punctuation
                    try:
                        lastWordIndex-=1  #  Subtraction pulls the index back until we're not looking at a puncuation mark
                        rhymeWord = rhymeLine[lastWordIndex]  #  Picking the last word
                    except IndexError:
                        print(lineno(), "iE:", rhymeLine, lastWordIndex)
                        return  [], [], True  #  redButton event
                print(lineno(), 'stanzaGov - rhymeWord:', rhymeWord)
                rhymeList = rhymeGrab(rhymeWord)
                if len(rhymeList) == 0 or 'rhyfuckt' in rhymeList:
                    rhymeList = rhymeGrab(rhymeWord+'(0)')
                rhymeThisLine = True
                if len(rhymeList) > 0:  #  Ensure that this produced some rhymes
                    print(lineno(), 'stanzaGov - rhymer', rhymeWord, '|', rhymeList)
                    superBlackList, usedList, newLine, redButton = lineGovernor(superBlackList, qAnteLine, usedList, expressList, rhymeThisLine, rhymeList, empMap[lineCt])  #  If so, we try to create rhyming lines
                else:  #  Our lines created nothing, so we hit a redbutton event
                    return [], [], True
            else:  #  Then you don't need rhymes
                rhymeList = []
                print(lineno(), 'stanzaGov -', qAnteLine, usedList, expressList, False, rhymeList, empMap[lineCt])
                superBlackList, usedList, newLine, redButton = lineGovernor(superBlackList, qAnteLine, usedList, expressList, False, rhymeList, empMap[lineCt])  #
        elif metSwitch == False:
            usedList, newLine, redButton = plainLinerLtoR(qAnteLine, usedList, expressList, rhymeList, empMap[lineCt])
        else:
            print(lineno(), 'stanzaGov - lineGov')
            superBlackList, usedList, newLine, redButton = lineGovernor(superBlackList, qAnteLine, usedList, expressList, rhymeThisLine, [], empMap[lineCt])
        if redButton == True:  #  Not an elif because any of the above could trigger this; must be separate if statement
            print(lineno(), 'stanzaGov - redButton')
            #stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])  #  Creates a fresh stanza, no usedList
            stanza, superBlackList, qAnteLine = removeLine(stanza, superBlackList)
        elif len(newLine[1]) > 0:  #  Line-building functions will either return a valid, nonzero-length line, or trigger a subtraction in the stanza with empty list
            print(lineno(), 'stanzaGov - newLine:', newLine)
            stanza, superBlackList, qAnteLine = acceptLine(stanza, superBlackList, newLine)
        elif len(stanza) > 0:  #  Check if the stanza is nonzero-length, otherwise there's nothing to subtract, resulting in an error
            stanza, superBlackList, qAnteLine = removeLine(stanza, superBlackList)
        else:  #  Redundant, as the stanza should logically be vetoed already, but just to clean house
            print(lineno(), 'stanzaGov - vetoStanza')
            #stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])
            stanza, superBlackList, qAnteLine = removeLine(stanza, superBlackList)
        lineCt = len(stanza)  #  Count the length of the stanza, provided no redButton events occurred...

    return stanza, usedList, redButton


############0####
#  poem building


def vetoPoem():
    return [], [], 0, False
          #poem, usedList, stanzaCt, redButton


def poemGovernor(usedList):  #  Outlines the parameters of the poem
    print(lineno(), 'poemGovernor initialized\n'+str(time.ctime())+'\n')
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
        


################
#  MAIN SECTION


def main__init():
    
    textFile = 'shkspr'
    print(lineno(), 'initializing program', str(time.ctime())[11:20], '\ntextFile:', textFile, '\n')

    #########################
    #  Static data, will change with GUI and testVals progs

##    values = guiInterface()
    global rhyDic
    rhyDic = defaultdict(list)

    global poemQuota, stanzaQuota
    poemQuota = 20
    stanzaQuota = 1
     
    global rawText
    rawText = str(open('data/textLibrary/'+textFile+'.txt', 'r', encoding='latin-1').read())
    rawText = rawText.replace('\n', ' ')  #  First clean up some meta-bits that inhibit text digestion
    rawText = rawText.replace('_', " ")
    rawText = rawText.replace('``', '"')
    rawText = rawText.replace("''", '"')
    rawText = rawText.replace('`', "'")
    rawText = rawText.replace('	', " ")	
    rawText = rawText.replace('&', ' and ')
    for all in allPunx:  #  Put a space around punctuation to tokenize later
        rawText = rawText.replace(all, ' '+all+' ')
    rawText = rawText.replace("     ", ' ')  #  Makes 5 whitespace characters shrink into 1 in text
    rawText = rawText.replace("    ", ' ')  #  Makes 4 into 1
    rawText = rawText.replace("   ", ' ')  #  Makes 3 into 1
    rawText = rawText.replace("  ", ' ')  #  Then 2 to 1 for good measure, overall 120:1. Every significant token should still have one space between the adjacent
    rawText = rawText.lower()

    #  Tokenizes raw text, grooms into lists of words
    global splitText
    splitText = rawText.split(' ')  # The reason for placing a space between all tokens to be grabbed

    global proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20
    global proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20
    global proxPlusLista, proxMinusLista, proxLib # gramProxLib, gramProxPlusLista, gramProxMinusLista
    #  These dictionaries contain lists of words that come after
    proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    #  The dictionaries are organized into lists that are accessed by index. Useful in while loops with ascending/descending numbers
    proxPlusLista = [proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20]
    proxMinusLista = [proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20]

    global proxMinDial, proxMaxDial, punxProxNum
    proxMinDial = int(2)
    proxMaxDial = int(20)
    punxProxNum = int(3)

    stanza, usedList = [], []

    global rhyMap, empMap
    rhyMap = 'aaa'
    empMap = [[bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)],
              [bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)],
              [bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)]]

    empMode = 0

    contractionFile = open('data/USen/contractionList.txt', 'r')
    contractionSwitch = csv.reader(open('data/USen/contractionSwitches.csv', 'r+'))
    global contractionDic, contractionList  #  These are immutable and should be accessed wherever
    contractionDic = defaultdict(list)  #  Use a dictionary to look up contraction switches
    contractionList = []  #  Use a list to check if the contraction exists (circumvents excepting KeyErrors)
    for line in contractionFile:  #  Makes a dictionary of contractions
        contractionList.append(line[:-1])  #  Remove '\n' before appending
    print(lineno(), 'len(contractionList):', len(contractionList), contractionList[:10])
    for line in contractionSwitch:
        #if "'s" not in line[0]:  #  There's a problem with whether the line is a possessive or contraction of "___ is"
        contractionDic[line[0]] = line[1]
    #print(contractionDic)
    print(lineno(), 'len(contractionDic):', len(contractionDic), contractionDic["can't"], contractionDic["don't"])
        
        
    global rSyls
    rSyls = 2

    global usedSwitch, rhySwitch, metSwitch, thesSwitch
    usedSwitch = False
    rhySwitch = True
    metSwitch = True
    thesSwitch = False
    
    #
    ##########################


    print('opening fonoFiles')  #  These are global values, so they need to be opened regardless
    global emps
    emps = gF.globalOpen('data/USen/empDic-USen-unik.csv', 'lista')
    for key, val in emps.items():  #  Stored as ints because could be numbers up to 2. Change to bools
        boolSwitch = []
        for each in val:
            if each == '1':
                boolSwitch.append(bool(True))
            else:
                boolSwitch.append(bool(False))
        emps[key] = boolSwitch
    vocs = gF.globalOpen('data/USen/vocDic-USen-MAS.csv', 'lista')
    cons = gF.globalOpen('data/USen/conDic-USen-MAS.csv', 'lista')
    fono = gF.globalOpen('data/USen/fonDic-USen-MAS.csv', 'lista')
    
    # if rhySwitch == on, load rhyming dictionary here
    # write it in __gloFunk
    
    print(lineno(), 'len(emps):', len(emps))
    print(lineno(), 'opening doubles')
    global doubles
    doubles = []
    for key, val in emps.items():
        if '(' in key:
            doubles.append(key[:-3])
    print(lineno(), "rhySwitch =", rhySwitch)
    loadmakeData(textFile, proxPlusLista, proxMinusLista)  #  Loads the data needed or makes it
    poemCt = int(0)
    while poemCt < poemQuota:
        poem, usedList = poemGovernor(stanzaQuota)
        poemCt+=1
        print('Poem #'+str(poemCt), '|', str(time.ctime())[11:20])
        for each in poem:
            print(each, '\n')
        input('paused')

    print('PROGRAM FINISHED')

main__init() #  and now that everything's in place, set it off!

##  END
