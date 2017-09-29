

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

#  Organization of variables: empLine, qEmpLine, superPopList, superBlackList, usedList, rhymeList, qLineIndexList, proxDicIndexList, qWord, qLine, qAnteLine, redButton


##########
##  declaration of libraries
##########

from string import *
import tkinter as tk
import ___gloFunk as gF # Make sure to remove underscores later
import nltk
from nltk.corpus import wordnet as wn
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


global quantumList
quantumList = ['was', 'be', 'and', 'to', 'for', 'a', 'the', 'in', 'at', 'but', 'an', 'not', 'is', 'do', 'did', 'can', 'could', 'will', 'does']  #  List of words used for quantum emp patterns
nonEnders = ['and', 'or', 'a', 'but', 'the', 'an', ',', ';', ':', '--']

allPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '"', "''", '-', '\\', '+', '=', '/', '<', '>', '(', ')']  #  Doesn't include apostrophe, because that could be part of a contraction
midPunx = [',', ';', ':', '--']
endPunx = ['.', '!', '?']  #  To gather which words immediately thereafter should start a sentence

bannedChops = ['@', '#', '&', '*', '\\', '+', '=', '/', '<', '>']


##########
##  text and library preparation
##########

def gpDataWriter(lang, dicList, fileBit, textFile):

    ##  Writes grammar and proximity data to hard drive

    pFile = csv.writer(open(lang+'/data/textLibrary/textData/'+textFile+'-'+fileBit+'.csv', 'w+'))
    #$print(lineno(), 'building: data/textLibrary/textData/'+textFile+'-'+fileBit+'.csv')
    ##$print(dicList)
    for key, val in dicList[0].items():
        fullString = str()
        for each in dicList:
            dicString = str()
            for entr in each[key]:
                #4 #$print('gpData:', entr, )
                dicString = dicString+entr+'^'  #  Entries for each proxLib are separated by the '^'
            fullString = fullString+dicString[:-1]+'~'  #  Proxlibs are separated by '~'. proxPlusLista is saved in one file.
        for char in fullString:
            if char != '~':      # This is to screen for empty sets. If one char is not a tilde then it's non-empty.
                #$print(lineno(), fileBit, 'writing:', key, fullString[:min(20, len(fullString))])
                pFile.writerow([key, fullString[:-1]])
                break


def loadmakeData(lang, textFile, proxPlusLista, proxMinusLista):
    global firstWords, firstPopList
    firstWords, firstPopList = [], []
    try:
        filepath = (lang+'/data/textLibrary/textData/'+textFile+'-firstFile.txt')
        #$print(lineno(), 'begin fwFile load', filepath) 
        firstFile = open(filepath, 'r')
        for line in firstFile:
            firstWords.append(line[:-1])
            firstPopList.append(line[:-1])
        #$print(lineno(), 'begin prox load')
        #  Take a look at gpDataOpener. Consider moving more code there, or bring some here
        proxPlusLista = gF.proxDataOpener(lang, proxPlusLista, 'proxP', textFile)
        proxMinusLista = gF.proxDataOpener(lang, proxMinusLista, 'proxM', textFile)
        #$print(lineno(), 'prox load complete')
            
    except FileNotFoundError:
        firstFile = open(lang+'/data/textLibrary/textData/'+textFile+'-firstFile.txt', 'w+')
        splitTIndex = int(0)
        splitTLen = len(splitText)
        proxMaxDial = 19
        #$print(lineno(), 'begin loadmakeProxLibs()')
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
                    ##$print(lineno(), 'plusadd = proxP:', proxWord, 'pWord:', pWord)
                    proxPlusLista[proxDicCounter][pWord].append(proxWord)
                if pWord not in proxMinusLista[proxDicCounter][proxWord]:
                    #4 #$print(lineno(), 'minusadd = proxM:', proxWord, 'pWord:', pWord)
                    proxMinusLista[proxDicCounter][proxWord].append(pWord)
                proxDicCounter+=1
                proxNumerator+=1
            splitTIndex+=1
        #$print(lineno(), 'writing proxLibs...')
        gpDataWriter(lang, proxPlusLista, 'proxP', textFile)
        gpDataWriter(lang, proxMinusLista, 'proxM', textFile)
  

def contractionAction(contraction, qLine):  #  Switches contractions between phonetic line and real/grammar line
    qLine[0]+=contraction
    qLine[1]+=contractionDic[contraction]


def rhymeGrab(empLine, pWord):
    #$print(lineno(), 'rhyGrab:', pWord)
##    try:
##        emps[pWord]  #  Check if the word has two pronunciations
##    except KeyError:  #  If there's only one way to say the word, no changes will be made\
##        return []
    pWEmps = gF.empsLine(empLine, [pWord], emps, doubles, quantumList)
    if len(rhyDic[pWord]) == 0:  #  Means we haven't looked it up yet
        #$print(lineno(), 'rhymeGrab search')
        totalSyls = 1
        while totalSyls < 10:  #  Rhyming dictionary was only built up to 10 syllables
            rSyls = 1 #  rSyls means the number of syllables that should match starting from right ('marination' and 'procreation' would have 2 rSyls of their 4 each)
            while rSyls <= len(pWEmps):
                #$print(lineno(), 'rhymeGrab going', rSyls, totalSyls)
                tName, rName = str(totalSyls), str(rSyls)  #  Turn into strings so we can open the file that we need
                if totalSyls < 10:
                    tName = '0'+tName
                if rSyls < 10:
                    rName = '0'+rName
                try:
                    dicFile = csv.reader(open(lang+'/data/'+accent+'/rhymes/rhymeLib-t'+tName+"r"+rName+".csv", "r"))  #  The rhymes are stored in a file named after their matching properties
                    for line in dicFile:
                        keyChain = line[0].split('^')
                        valChain = line[1].split('^')
                        if (pWord in keyChain) or (pWord in valChain):
                            #$print(lineno(), 'rhymes found')
                            for all in keyChain:
                                if '(' in all:  #  A doubWord
                                    rhymeWord = all[:-3]
                                else:  #  Append normally
                                    rhymeWord = all
                                if (rhymeWord not in rhyDic[pWord]) and (rhymeWord != pWord):
                                    rhyDic[pWord].append(rhymeWord)
                            for all in valChain:
                                if '(' in all:  #  A doubWord
                                    rhymeWord = all[:-3]
                                else:  #  Append normally
                                    rhymeWord = all
                                if (rhymeWord not in rhyDic[pWord]) and (rhymeWord != pWord):
                                    rhyDic[pWord].append(rhymeWord)
                except IOError:
                    #$print(lineno(), 'ioE: rhyDic', pWord, 'not found')
                    return str()
                rSyls+=1
            totalSyls+=1
        if len(rhyDic[pWord]) == 0:  #  If, at this point, the rhyming dictionary returned nothing, we add a nonsense word so the dictionary entry is non-zero and this function won't search again
            rhyDic[pWord] = []
    #$print(lineno(), 'got rhys for', pWord+':', rhyDic[pWord])
    burnList = []
    for all in rhyDic[pWord]:
        #$print(lineno(), 'rhytest:', all)
        if ('(' in pWord) and (all == pWord[:-3]):
            #$print(lineno(), 'rhyMatch:', all)
            burnList.append(all)
    for all in burnList:
        rhyDic[pWord].remove(all)
    #$print(lineno(), 'rhys for', pWord, rhyDic[pWord])
    return rhyDic[pWord]


def removeWordL(superPopList, qLine):  #  Remove the leftmost word from line
    # do something
    return data


def removeWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine):  #  Remove the rightmost word from line
    #$print(lineno(), 'removeWordR-in', 'qLine:', qLine, 'runLine:', runLine)
    if len(qLine[0]) == 0 and len(runLine[0]) > 0:  #  Cut runLine
        #$print(lineno(), "rMR - if0")
        minusWordX = runLine[0].pop(0)  #  Since the previous line didn't yield any following line
        minusWordY = runLine[1].pop(0)  #  minusWordX just holds whatever is getting popped
        if minusWordX != minusWordY:  #  If there's a discrepency, such as converting contractions to uncontracted form
            #$print(lineno(), 'pLine/rLine discrepency')
            if "'" in minusWord1:  #  If rLine has a contraction, remove another word from other line
                minusWordX = runLine[0].pop(0)  #  This just removes the second word of the contraction
    if len(qLine[0]) > 0:
        #$print(lineno(), "rMR - if1")
        minusWord0 = qLine[0].pop()  #  Remove word from first part of line
        minusWord1 = qLine[1].pop()  #  Until better method introduced, cut rLine here
        if minusWord0 != minusWord1:  #  If there's a discrepency, such as converting contractions to uncontracted form
            #$print(lineno(), 'pLine/rLine discrepency')
            if "'" in minusWord1:  #  If rLine has a contraction, remove another word from other line
                minusWord0 = qLine[0].pop()  #  This just removes the second word
                minusWord0 = minusWord1  #  superBlackList will be adding minusWord0 later, and we want that to be the contraction        
        #  Some sort of contractionAction function should go here
        pWEmps = gF.empsLine(empLine, [minusWord0], emps, doubles, quantumList)
        pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)
        pLEmps = pLEmps[:-len(pWEmps)]  #  Cut emps from main line
        #$print(lineno(), 'snip qLineIndex in:', qLineIndexList, proxDicIndexList)
        qLineIndexList = qLineIndexList[:-1]
        proxDicIndexList = proxDicIndexList[:-1]
        #$print(lineno(), 'snip qLineIndex out:', qLineIndexList, proxDicIndexList)
        #qLineIndexList, proxDicIndexList = proxDataBuilder(qLineIndexList, proxDicIndexList, qLineIndexList, proxDicIndexList, (runLine[0]+qLine[0], runLine[1]+qLine[1]), len(runLine[1]+qLine[1]))
        superBlackList = superBlackList[:(len(qLine[1])+1)]  #  If we leave blacklisted words further down the road, they may negate an otherwise compatible sentence
        #$print(lineno(), 'minusWord0:', minusWord0)
        superBlackList[len(qLine[1])].append(minusWord0)  #  Add to blackList at correct point
    #superBlackList[-1].append(minusWord0)  #  To avoid a loop, prevent popList from checking branch again
    else:
        pLEmps, qLineIndexList, proxDicIndexList = [], [], []
    #if len(superPopList) > (len(qLine[1]) + 1):  #  If we've gone further than checking the list of next words
    #$print(lineno(), 'rMR - snipPopList')
    superPopList = superPopList[:(len(qLine[1]) + 1)]
    #$print(lineno(), 'removeWordR-out', qLine, '| len(superPopList):', len(superPopList))
    return pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine


def acceptWordL(qLine, nextWord, qLineIndexList, proxDicIndexList):  #  Add the rightmost word to line

##  INVERT THESE VALUES

    #$print('acceptWord:', qLine, '|', nextWord)
    pLine.append(nextWord)
    if len(proxNumList) > 0:
        proxNum = proxNumList[-1] + 1
    else:
        proxNum = 0
    proxNumList.append(proxNum)
    proxLineNum = proxLineNumList[0] + 1
    proxLineNumList.insert(0, proxLineNum)
    return qLineIndexList, proxDicIndexList, qLine


def acceptWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine, nextWord):  #  Add word to right side of line
    #$print('acceptWordR-in:', runLine, qLine, '|', nextWord)
    for each in nextWord[0]:
        qLine[0].append(each)
    for each in nextWord[1]:
        qLine[1].append(each)
    #qLineIndexList, proxDicIndexList = proxDataBuilder(qLineIndexList, proxDicIndexList, qLineIndexList, proxDicIndexList, qLine, len(qLine[1]))
    #if len(superBlackList) == len(qLine[1]):  #  We don't have any blackListed words that far ahead
    superBlackList.append([])
    qLineIndexList, proxDicIndexList = proxDataBuilder(qLineIndexList, proxDicIndexList, (runLine[0]+qLine[0], runLine[1]+qLine[1]), len(runLine[1]+qLine[1]))
    #superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(empLine, superPopList, [], superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
    #$print('acceptWordR-out:', qLine, '|', nextWord, qLineIndexList, proxDicIndexList)
    return superBlackList, superPopList, expressList, qLineIndexList, proxDicIndexList, qLine


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


def proxDataBuilder(qLineIndexList, proxDicIndexList, qLine, limitNum):  #  Takes the qLine and builds proxData up to a certain length
    #$print(lineno(), 'proxDataBuilder |', qLine, qLineIndexList, proxDicIndexList)
    qLineLen = len(qLine[1])
    proxInt = int(0)  #  Starts the proxData
    thisqLineIndexList, thisproxDicIndexList = [], []
    while proxInt < qLineLen:  #  Creates a list of indexes and the reverse list to index proxDics
        thisproxDicIndexList.append(proxInt)
        thisqLineIndexList.insert(0, proxInt)
        proxInt+=1
    qLineIndexList.append(thisqLineIndexList)
    proxDicIndexList.append(thisproxDicIndexList)
    #$print(lineno(), 'proxData:', qLineIndexList, proxDicIndexList)
    return qLineIndexList, proxDicIndexList


def superPopListMaker(empLine, superPopList, expressList, proxExpress, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine): #  Creates a list-of-lists to pull from
    #$print(lineno(), 'sPLM init | len(superPopList)', len(superPopList))
    if (len(superPopList) == (len(runLine[1]+qLine[1])+1)) and (len(superPopList[-1]) > 0):
        #$print(lineno(), 'sending back superPopList')
        return superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
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
    #$print(lineno(), 'superPopMaker start |', len(superPopList), '|', testLine, 'proxData:', qLineIndexList, proxDicIndexList)
    # qLineIndexList: List of positions on the qLine
    # proxDicIndexList: List of positions for the qLine to find in proxDics
##    if len(qLineIndexList) > len(testLine[1]):
##        qLineIndexList, proxDicIndexList = proxDataBuilder(qLineIndexList, proxDicIndexList, testLine, len(testLine[1]))  #  Refresh proxData
    #qLineIndexList, proxDicIndexList = proxDataBuilder(qLineIndexList, proxDicIndexList, testLine, len(testLine[1]))
    testLineLen = len(testLine[1])
    if testLineLen == 0:  #  If we've received a totally empty line, populate it with firstWords, but not directly or corrupt global bank
        #$print(lineno(), 'sPM - zeroLine')
        startList = firstWordSuperPopList(proxExpress, superBlackList)
        return startList, [[]], qLineIndexList, proxDicIndexList, qLine, runLine
              #superPopList, superBlackList, etc
    # use rWord here, make method for dealing with doubles
    #$print(lineno(), 'sPM - len(testLine) >= 1', qLineIndexList, proxDicIndexList)
    try:
        #$print(lineno(), 'sPM - this blackList:', qLine, len(superBlackList))#, superBlackList[len(qLine[1])])
        pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)
        while len(qLineIndexList[len(qLine[1])-1]) > 0:
            for all in proxP1[testLine[1][-1]]:
                if (all not in superBlackList[len(qLine[1])]):  #  Screen against the initial superBlackList
                    keepList.append(all)  #  Practically an 'else' clause, because the 'if' above returns an answer
            ##$print(lineno(), 'sPM - this keepList:', keepList)
            if len(qLineIndexList[len(qLine[1])-1]) > 1:  #  Only keep going if we need more than 2 words analyzed
                for each in proxDicIndexList[len(qLine[1])-1][1:]:  #  Skip first indexNum, we already found it
                    testList = proxPlusLista[each][testLine[1][qLineIndexList[len(qLine[1])-1][each]]]  #  Scans approximate words with indexes
                    burnList = []  #  burnList holds words that don't match with mutual proxLists
                    testString = str()  #  Look for that same string in the rawText
                    ##$print(lineno(), each, len(superBlackList))
                    ##$print(lineno(), superBlackList[qLineIndexList[len(qLine[1])-1][0]-len(runLine[0])])
                    #qLineIndexLen = len(qLineIndexList[len(qLine[1])-1])  #  Use this to rebuild testString without words that have failed
                    for all in qLineIndexList[len(qLine[1])-1]:  #  Build a line with words already used
                        testString = testLine[1][all]+' '+testString  #  Build backwards because we trim failed lines from the front
                    for all in keepList:
                        testString+=all+' '  #  Add the new word to the string, plus a space so we don't see a false positive with a partial word ('you' mistaken for 'your')
                        if (all not in testList) or (testString not in rawText) or (all in superBlackList[len(qLine[1])]):  #  Add blackList screening later
                            burnList.append(all)  #  Screen it with a burnList so we don't delete as we iterate thru list
                        testString = testString[:-(len(all)+1)]  #  Remove the word to prepare for another testString addition
                    ##$print(lineno(), 'len(keepList):', len(keepList), 'len(burnList):', len(burnList))
                    if len(keepList) > 0:
                        for all in burnList:
                            keepList.remove(all)
                    else:  #  If we run out prematurely, stop iterating over the list
                        #$print(lineno(), 'sPLM keepList out')
                        break
            keepList = listSorter(keepList, [], [])
            if len(keepList) == 0:
                qLineIndexList[len(qLine[1])-1] = qLineIndexList[len(qLine[1])-1][:-1]
                proxDicIndexList[len(qLine[1])-1] = proxDicIndexList[len(qLine[1])-1][:-1]
                #$print(lineno(), 'snipping proxData', qLineIndexList[len(qLine[1])-1], proxDicIndexList[len(qLine[1])-1])
                if len(qLineIndexList[len(qLine[1])-1]) > 0:  #  Ensure that the line has something to check
                    if (len(qLineIndexList[len(qLine[1])-1]) <= proxMinDial):  #  This keeps the chain longer than a minimum length
                        pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
                        return superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine  #  Give up
            else:
                #$print(lineno(), 'superPopMaker grown |', len(superPopList), len(superPopList[-1]), '|', testLine, 'proxData:', qLineIndexList, proxDicIndexList)
                break
    except KeyError:
        #$print(lineno(), 'kE:', testLine, 'len(superPopList):', len(superPopList))
        unknownWords.write(qLine[1][-1])
        pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
        #qLineIndexList, proxDicIndexList = proxDataBuilder(qLineIndexList, proxDicIndexList, qLine, len(qLine[0]))
        return superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
    ##$print(superPopList)
    #input('waiting...')
    while len(superPopList) <= len(qLine[1]):  #  If we don't have a proper amount to pop from
        superPopList.append([])
    for all in keepList:
        if all not in superPopList[-1]:
            superPopList[-1].append(all)  #  If we didn't find anything, append an empty set
    while len(expressList) <= len(qLine[1]):  #  If we don't have a proper amount to pop from
        expressList.append([])
    for all in proxExpress:
        if all in superPopList[-1] and all not in expressList[-1]:
            expressList[-1].append(superPopList[-1].pop(superPopList[-1].index(all)))
    #$print(lineno(), 'exL:', len(expressList), len(expressList[-1]), testLine)
    #$print(lineno(), 'sPL:', len(superPopList), len(superPopList[-1]), testLine)
    return superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine


def plainPopDigester():  #  Digests words from list without regard to their syllables or meter
    return doo, doo


def empPopDigester():  #  Digests words based on the length of their syllables
    return doo, doo


def testEmpLine(empLine, superBlackList, expressList, proxExpress, superPopList, qLineIndexList, proxDicIndexList, qLine, runLine, qWord):  #  A subfunction of metPopDigester, which tests words given to it
    #$print(lineno(), 'testEmpLine:', empLine, qLine, qWord)
    testLine, hitSwitch = [], False  #  HitSwitch is a boolean that tells whether a word has been found
    for each in qLine[0]:
        testLine.append(each)
    for each in qWord[0]:
        testLine.append(each)   
    testEmps = gF.empsLine(empLine, testLine, emps, doubles, quantumList)
    #superBlackList[len(qLine[1])].append(pWord)  #  Add to blackList at correct point
    #$print(lineno(), 'superBlackListLen:', len(superBlackList[len(qLine[1])]))
    if len(testEmps) <= len(empLine):  #  This is to screen against an error
        #$print(lineno(), 'mPD testEmp0 |', qWord)
        if testEmps == empLine[:len(testEmps)]:  #  Check if the word is valid
            #$print(lineno(), 'mPD testEmp pass')
            hitSwitch = True
            superBlackList, superPopList, expressList, qLineIndexList, proxDicIndexList, qLine = acceptWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine, qWord)
            #$print(lineno(), 'mPD acceptR', qLine, testEmps, qLineIndexList, proxDicIndexList)
            return testEmps, superBlackList, qLineIndexList, proxDicIndexList, qLine, hitSwitch
    return testEmps, superBlackList, qLineIndexList, proxDicIndexList, qLine, hitSwitch


def metPopDigester(empLine, superPopList, expressList, proxExpress, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine):  #  Digests words that fit a particular meter
    #$print(lineno(), 'mPD start | len(superPopList):', len(superPopList), qLine, runLine)
    if len(superPopList) > 0:
        #$print(lineno(), 'len(superPopList[-1]):', len(superPopList[-1]))
        superPopListLenLine = []
        for each in superPopList:
            superPopListLenLine.append(len(each))
        #$print(lineno(), 'superPopListLenLine:', superPopListLenLine)
    if len(expressList) > 0:
        #$print(lineno(), 'len(expressList[-1]):', len(expressList[-1]))
        expressListLenLine = []
        for each in expressList:
            expressListLenLine.append(len(each))
        #$print(lineno(), 'expressListLenLine:', expressListLenLine)
    if len(superBlackList) > 0:
        superBlackListLenLine = []
        #$print(lineno(), 'len(superBlackList[-1]):', len(superBlackList[-1]))
        superBlackListLenLine = []
        for each in superBlackList:
            superBlackListLenLine.append(len(each))
        #$print(lineno(), 'superBlackListLenLine:', superBlackListLenLine)
    #$print(lineno(), 'proxData:', qLineIndexList, proxDicIndexList)
    #qLineIndexList, proxDicIndexList = proxDataBuilder(qLineIndexList, proxDicIndexList, (runLine[0]+qLine[0], runLine[1]+qLine[1]), len(runLine[1]+qLine[1]))
    superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(empLine, superPopList, expressList, proxExpress, superBlackList,  qLineIndexList, proxDicIndexList, qLine, runLine)
    while len(superPopList) > 0:
        contractionWords, punxList, thesWords = [], [], []
        while len(expressList[-1]) > 0:
            pWord = expressList[-1].pop(random.choice(range(0, len(expressList[-1]))))
            qWord = ([pWord], [pWord])  #  pWord is the same word unless the phonetic data doesn't match the 'real' data
            if (pWord in contractionList) and (pWord[:-2] != "'s") and (pWord[-1] != "'") and (pWord[:2] != ("o'" or "d'")):  #  This line will place contractions in a special list to be switched if nothing works
                contractionWords.append(pWord)
            elif pWord in allPunx:
                punxList.append(pWord)
            elif pWord not in allPunx:  #  A zero-length emps value is an unrecognized word
                if (thesSwitch == True) and (pWord not in quantumList):
                    thesWords.append(pWord)
                superBlackList[len(qLine[1])].append(pWord)  #  Make sure that it doesn't keep going thru the same words over and over
                #$print(lineno(), empLine, qLine, qWord)
                testEmps, superBlackList, qLineIndexList, proxDicIndexList, qLine, hitSwitch = testEmpLine(empLine, superBlackList, expressList, proxExpress, superPopList, qLineIndexList, proxDicIndexList, qLine, runLine, qWord)
                if hitSwitch == True:
                    return testEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine            
        while len(superPopList[-1]) > 0:
            pWord = superPopList[-1].pop(random.choice(range(0, len(superPopList[-1]))))
            qWord = ([pWord], [pWord])  #  pWord is the same word unless the phonetic data doesn't match the 'real' data
            if (pWord in contractionList) and (pWord[:-2] != "'s") and (pWord[-1] != "'") and (pWord[:2] != ("o'" or "d'")):  #  This line will place contractions in a special list to be switched if nothing works
                contractionWords.append(pWord)
            elif pWord in allPunx:
                punxList.append(pWord)
            elif pWord not in allPunx:  #  A zero-length emps value is an unrecognized word
                if (thesSwitch == True) and (pWord not in quantumList):
                    thesWords.append(pWord)
                superBlackList[len(qLine[1])].append(pWord)  #  Make sure that it doesn't keep going thru the same words over and over
                #$print(lineno(), empLine, qLine, qWord)
                testEmps, superBlackList, qLineIndexList, proxDicIndexList, qLine, hitSwitch = testEmpLine(empLine, superBlackList, expressList, proxExpress, superPopList, qLineIndexList, proxDicIndexList, qLine, runLine, qWord)
                if hitSwitch == True:
                    return testEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
        #$print(lineno(), 'contSwitch:', contSwitch)
        if (contSwitch == True) and (len(contractionWords) > 0):  #  If any contractions were found in the superPopList we just tried
            #$print(lineno(), 'contractionWords:', contractionWords)
            for each in contractionWords:
                contWord = contractionDic[each]
                if len(contWord) == 0:  #  If there's no contraction, it's just a word with an apostrophe
                    contWord = pWord
                #$print(lineno(), 'contWord:', contWord)
                qWord = (contWord, [pWord])  #  Appending two different words to the line
                #$print(lineno(), 'contraction attempt:', each, qWord)
                testEmps, superBlackList, qLineIndexList, proxDicIndexList, qLine, hitSwitch = testEmpLine(empLine, superBlackList, expressList, proxExpress, superPopList, qLineIndexList, proxDicIndexList, qLine, runLine, qWord)
                if hitSwitch == True:
                    return testEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
        #$print(lineno(), 'thesSwitch:', thesSwitch)
        if thesSwitch == True:
            while len(thesWords) > 0:
                #$print(lineno(), 'thesCheck | len(thesWords):', len(thesWords))
                thesWord = thesWords.pop(random.choice(range(0, len(thesWords))))
                try:
                    syns = thesDic[thesWord]
                except KeyError:
                    syns = []
                    #$print(lineno(), 'kE:synWord')
                    continue
                #$print(lineno(), 'syns:', syns)
                while len(syns) > 0:
                    synonym = syns.pop()
##                    if '_' in synonym:
##                        #$print(lineno(), 'synSplit:', synonym)
##                        synonym = synonym.split('_')
##                        #$print(lineno(), 'becomes:', synonym)
                    qWord = ([synonym], [thesWord])
                    #$print(lineno(), 'thes qWord:', qWord)
                    testEmps, superBlackList, qLineIndexList, proxDicIndexList, qLine, hitSwitch = testEmpLine(empLine, superBlackList, expressList, proxExpress, superPopList, qLineIndexList, proxDicIndexList, qLine, runLine, qWord)
                    if hitSwitch == True:
                        return testEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
        if (len(qLine[1]) > 2):  #  We want qLine to have more than 2 words before trying punctuation because it sounds better, although it isn't necessary for function. Also, make sure to exhaust all other possibilities first
            #$print(lineno(), 'punxSearch', qLine[1][-(min(punxProxNum, len(qLine[1]))):])
            punxCt = int(0)
            for all in qLine[1][-(min(punxProxNum, len(qLine[1]))):]:
                if all in allPunx:  #  Will discriminate any puncuation within the designated length of punxProxNum
                    #$print(lineno(), 'found punk within punxProxNum:', all)
                    punxCt+=1
            if (punxCt == 0) and (len(punxList) > 0):
                punxWord = punxList.pop(random.choice(range(0, len(punxList))))
                qWord = ([punxWord], [punxWord])
                superBlackList, superPopList, expressList, qLineIndexList, proxDicIndexList, qLine = acceptWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine, ([pWord], [pWord]))
                #$print(lineno(), 'punxD acceptR', qLine)
                testEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)                
                return testEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
        if (len(qLineIndexList[len(qLine[1])-1]) > proxMinDial) and (len(runLine[1]+qLine[1]) > proxMinDial):
            #$print(lineno(), 'snip qLineIndex in:', qLineIndexList, proxDicIndexList, runLine[1], qLine[1])
            qLineIndexList[len(qLine[1])-1] = qLineIndexList[len(qLine[1])-1][:-1]
            proxDicIndexList[len(qLine[1])-1] = proxDicIndexList[len(qLine[1])-1][:-1]
            #$print(lineno(), 'snip qLineIndex out:', qLineIndexList, proxDicIndexList)
            superPopList = superPopList[:-1]
            superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(empLine, superPopList, expressList, proxExpress, superBlackList,  qLineIndexList, proxDicIndexList, qLine, runLine)
        elif len(qLine[1]) > 0: #and len(qLine[1]) > proxMinDial:  #  If we have enough words, then we can remove rightmost element and metadata, then try again
            #$print(lineno(), 'snipLine', qLine, '|', runLine, len(superPopList))
            pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(empLine, superPopList, expressList, proxExpress, superBlackList,  qLineIndexList, proxDicIndexList, qLine, runLine)
        #$print(lineno(), 'superPopList:', len(superPopList), len(superPopList[-1]))
        if (len(qLine[1]) == 0) and (len(superPopList[-1]) == 0):
            #$print(lineno(), 'no qLine or runLine or superPopList[-1]')
            return [], [[]], [[]], [[]], [], [], ([],[]), ([],[])  #  redButton situation
                  #pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
        #$print(lineno(), 'mPD end whilesub')
    pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)
    #$print(lineno(), 'mPD end whilemain | pLEmps:', pLEmps, qLine)
    return pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine
              #pLEmps, superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine    
 
        
def firstWordSuperPopList(proxExpress, superBlackList):  #  Creates a superPopList that reloads the global firstWords list
    #$print(lineno(), 'firstWordSuperPopList start')
    superPopList, expressList = [[]], [[]]
    for all in firstWords:
        if all not in superBlackList[0]:
            superPopList[0].append(all)
    for all in proxExpress:
        expressList[0].append(all)
    qLineIndexList, proxDicIndexList = [], []
    #$print(lineno(), 'len(superPopList):', len(superPopList), '| len(superPopList[0]):', len(superPopList[0]), qLineIndexList, proxDicIndexList)
    return superPopList, expressList, qLineIndexList, proxDicIndexList


def makeList(listA):  #  Simple function that appends all from one list to other, so they are not bound together
    [] = listB
    for all in listA:
        listB.append(all)
    return listB
        
    
##############
#  line building


def vetoLine(qAnteLine, proxExpress, superBlackList):  #  Resets values in a line to
    #$print(lineno(), 'resetLine, qAnteLine:', qAnteLine)
    runLine = ([],[])
    for each in qAnteLine[0]:  #  Re-create any qAnteLinesuperPopList, superBlackList, qLine, qLineIndexList, proxDicIndexList as a mutable variable
        runLine[0].append(each)
    for each in qAnteLine[1]:  #  Re-create any qAnteLinesuperPopList, superBlackList, qLine, qLineIndexList, proxDicIndexList as a mutable variable
        runLine[1].append(each)
    if len(runLine[1]) == 0:
        superPopList = firstWordSuperPopList(proxExpress, superBlackList)
    else:
        superPopList = [[]]
    return superPopList, [], superBlackList, [], [], ([],[]), runLine, False
          #superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine, redButton


def plainLinerLtoR(vars):
    data
    # without rhyme or meter


def plainLinerRtoL(vars):
    data


def firstWordMet(empLine, proxExpress, superBlackList, usedList, runLine):
    #$print(lineno(), 'firstWord met | len(superBlackList[0]):', len(superBlackList[0]))
    superPopList, expressList, qLineIndexList, proxDicIndexList = firstWordSuperPopList(proxExpress, superBlackList)
    #$print(lineno(), 'len(superPopList):', len(superPopList))
    pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = metPopDigester(empLine, superPopList, expressList, proxExpress, superBlackList, qLineIndexList, proxDicIndexList, ([], []), ([], []))
    #$print(lineno(), 'proxData:', qLineIndexList, proxDicIndexList)
    if len(superPopList[0]) == 0 and len(qLine[1]) == 0:
        #$print(lineno(), 'redButton == True')
        return superPopList, expressList, superBlackList, usedList, qLineIndexList, proxDicIndexList, qLine, runLine, True #  redButton event
    else:
        return superPopList, expressList, superBlackList, usedList, qLineIndexList, proxDicIndexList, qLine, runLine, False #  redButton event


def meterLiner(empLine, expressList, proxExpress, superBlackList, usedList, qLineIndexList, proxDicIndexList, qLine, qAnteLine):  #
    #$print(lineno(), 'meterLiner start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    runLine = ([], [])
    for each in qAnteLine[0]:  #  qAnteLine gets appended to runLine because this function will be cutting from it when it doesn't yield results
        runLine[0].append(each)
    for each in qAnteLine[1]:
        runLine[1].append(each)
    pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)
    while pLEmps != empLine:  #  Keep going until the line is finished or returns blank answer
        if (len(runLine[1]) == 0) and (len(qLine[1]) == 0):  #  Check if we're starting with a completely empty line, load firstWords to superPopList if so
            superPopList, expressList, superBlackList, usedList, qLineIndexList, proxDicIndexList, qLine, runLine, redButton = firstWordMet(empLine, expressList, superBlackList, usedList, runLine)
            #$print(lineno(), 'proxData:', qLineIndexList, proxDicIndexList)
        elif len(runLine[1]) > 0:  #  Checks before trying to manipulate runLine just below, also loops it so it subtracts from anteLine first
            #$print(lineno(), 'met if1')
            while len(superBlackList) <= len(qLine[1]):  #  Make sure superBlackList is long enough to add to w/ runLine
                superBlackList.append([])
            #$print(lineno(), 'runLine + qLine:', runLine, qLine, ', superBlackList:', len(superBlackList))
            if len(qLine[1]) == 0:
                qLineIndexList, proxDicIndexList = proxDataBuilder(qLineIndexList, proxDicIndexList, (runLine[0], runLine[1]), len(runLine[1]))
            superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(empLine, [], expressList, proxExpress, superBlackList,  qLineIndexList, proxDicIndexList, qLine, runLine)
            pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = metPopDigester(empLine, superPopList, expressList, proxExpress, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
        elif len(qLine[1]) > 0:
            #$print(lineno(), 'met if2 qLine:', qLine, 'len(superBlackList):', len(superBlackList), 'len(superPopList):', len(superPopList), qLineIndexList, proxDicIndexList)
            #superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(empLine, superPopList, expressList, proxExpress, superBlackList,  qLineIndexList, proxDicIndexList, qLine, runLine)
            pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = metPopDigester(empLine, superPopList, expressList, proxExpress, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            if len(superPopList[0]) == 0 and len(qLine[1]) == 0:  #  Nothing seems to work
                #$print(lineno(), 'met if2-redButton')
                return superPopList, expressList, superBlackList, usedList, qLine, runLine, True  #  redButton event, as nothing in the list worked
        elif len(runLine[0]) == 1 and runLine[-1] in endPunx:
            runLine = ([], [])  #  Render runLine inocuous because we're starting another sentence
            #$print(lineno(), 'met if3', runLine)
            superPopList, superBlackList, usedList, qLineIndexList, proxDicIndexList, qLine, runLine, redButton = firstWordMet(empLine, superBlackList, usedList, runLine)
            if len(superPopList[0]) == 0 and len(qLine[1]) == 0:
                #$print(lineno(), 'redButton == True')
                return superPopList, expressList, superBlackList, usedList, qLine, runLine, True #  redButton event
        else:  #  No runLine, no qLine, and superPopList[0] is out of firstWords
            #$print(lineno(), 'met if4')
            superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine, redButton = vetoLine(qAnteLine, [], superBlackList)
            return [[]], superBlackList, usedList, qLine, qAnteLine, True
        #$print(lineno(), 'end of meterLiner ifchecks')
        if len(qLine[1]) > 0:  #  Make sure there's a line to analyze
            #$print(lineno(), 'metLiner if out')
            pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)
        elif len(runLine[1]) == 0:  #  If runLine is also out, redButton
            #$print(lineno(), 'metLiner elif out')
            return [[]], expressList, superBlackList, usedList, qLine, runLine, True
        while len(pLEmps) > len(empLine):  #  If somehow the line went over the numbered lists
            (lineno(), 'meterLiner over emps')
            pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            #superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(empLine, superPopList, expressList, proxExpress, superBlackList,  qLineIndexList, proxDicIndexList, qLine, runLine)
        if pLEmps == empLine:
            #$print(lineno(), 'meterLiner pLEmps == empLine | superPopList:', len(superPopList), len(superPopList[-1]))
            if qLine[1][-1] in nonEnders:  #  Words that don't sound good as the last word of a line, such as conjunctions without something else to connect
                pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            else:
                superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(empLine, superPopList, expressList, proxExpress, superBlackList,  qLineIndexList, proxDicIndexList, qLine, runLine)
                for all in allPunx:
                    if all in superPopList[-1]:  #  If puncuation fits, place one on the end of a line (will give the next line an easier start, too)
                        superBlackList, superPopList, expressList, qLineIndexList, proxDicIndexList, qLine = acceptWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine, ([all], [all]))
                        break                        
    #$print(lineno(), 'meterLiner out:', qLine, 'len(superPopList):', len(superPopList))
    return superPopList, expressList, superBlackList, usedList, qLine, qAnteLine, False
          #superPopList, qAnteLine, qLine, usedList, redButton
            

def rhymeLiner(empLine, superPopList, expressList, proxExpress, superBlackList, usedList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine):
    #$print(lineno(), 'rhymeLiner start\nPrevious:', qAnteLine, '\nempLine:', empLine)
    runLine = ([], [])
    for each in qAnteLine[0]:  #  qAnteLine gets appended to runLine because this function will be cutting from it when it doesn't yield results
        runLine[0].append(each)
    for each in qAnteLine[1]:
        runLine[1].append(each)    
    expressList = [[]]
    for each in proxExpress:
        expressList[0].append(each)
    pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)
    while (pLEmps != empLine) or (qLine[0][-1] not in rhymeList):
        if (len(runLine[1]) == 0) and (len(qLine[1]) == 0):  #  Check if we're starting with a completely empty line, load firstWords to superPopList if so
            #$print(lineno(), 'rhy if0')
            superPopList, superBlackList, usedList, qLineIndexList, proxDicIndexList, qLine, runLine, redButton = firstWordMet(empLine, proxExpress, superBlackList, usedList, runLine)
        elif len(runLine[1]) > 0:  #  Checks before trying to manipulate runLine just below, also loops it so it subtracts from anteLine first
            #$print(lineno(), 'rhy if1')
            while len(superBlackList) <= len(qLine[1]):  #  Make sure superBlackList is long enough to add to w/ runLine
                superBlackList.append([])
            #$print(lineno(), 'runLine + qLine:', runLine, qLine, ', superBlackList:', len(superBlackList))
            if len(qLine[1]) == 0:
                qLineIndexList, proxDicIndexList = proxDataBuilder(qLineIndexList, proxDicIndexList, (runLine[0], runLine[1]), len(runLine[1]))
            superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(empLine, superPopList, expressList, proxExpress, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = metPopDigester(empLine, superPopList, expressList, proxExpress, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
        elif len(qLine[1]) > 0:
            #$print(lineno(), 'rhy if2 qLine:', qLine, 'len(superBlackList):', len(superBlackList), 'len(superPopList):', len(superPopList))
            pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = metPopDigester(empLine, superPopList, expressList, proxExpress, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            if len(superPopList[0]) == 0 and len(qLine[1]) == 0:  #  Nothing seems to work
                #$print(lineno(), 'rhy if2-redButton')
                return superPopList, expressList, superBlackList, usedList, qLine, runLine, True  #  redButton event, as nothing in the list worked                
        elif len(runLine[0]) == 1 and runLine[-1] in endPunx:                
            runLine = ([], [])  #  Render runLine inocuous because we're starting another sentence
            #$print(lineno(), 'rhy if3', runLine)
            superPopList, superBlackList, usedList, qLineIndexList, proxDicIndexList, qLine, runLine, redButton = firstWordMet(empLine, superBlackList, usedList, runLine)
            if len(superPopList[0]) == 0 and len(qLine[1]) == 0:
                #$print(lineno(), 'redButton == True')
                return superPopList, expressList, superBlackList, usedList, qLine, runLine, True #  redButton event
        else:  #  No runLine, no qLine, and superPopList[0] is out of firstWords
            #$print(lineno(), 'rhy redButton')
            superPopList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine, redButton = vetoLine(qAnteLine, [], superBlackList)
            return [[]], expressList, superBlackList, usedList, qLine, runLine, True    
        #$print(lineno(), 'end of rhymeLiner ifchecks')
        if len(qLine[1]) > 0:  #  Make sure there's a line to analyze
            #$print(lineno(), 'rhyLiner if out')
            pLEmps = gF.empsLine(empLine, qLine[0], emps, doubles, quantumList)
        elif len(runLine[1]) == 0:  #  If runLine is also out, redButton
            #$print(lineno(), 'rhyLiner elif out')
            return [[]], expressList, superBlackList, usedList, qLine, runLine, True
        while len(pLEmps) > len(empLine):  #  If somehow the line went over the numbered lists
            (lineno(), 'rhyLiner over emps')
            pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            #superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(empLine, superPopList, expressList, proxExpress, superBlackList,  qLineIndexList, proxDicIndexList, qLine, runLine)
        if pLEmps == empLine:
            #$print(lineno(), 'rhymeLiner pLEmps == empLine | qLine[0]:', qLine[0])
            ##$print(lineno(), len(superPopList), 'superPopList[-1]:', superPopList[-1])
            if (qLine[0][-1] in nonEnders) or (qLine[0][-1] not in rhymeList):  #  Words that don't sound good as the last word of a line, such as conjunctions without something else to connect
                pLEmps, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = removeWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
                superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(empLine, superPopList, expressList, rhymeList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
            else:
                superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine = superPopListMaker(empLine, superPopList, expressList, proxExpress, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine)
                #$for all in rhymeList:
                    #$if all in superPopList[-1]:
                        #$print(lineno(), 'rhyfound!:', all)
                #$print(lineno(), 'rhymeList:', rhymeList)
                for all in allPunx:
                    if all in superPopList[-1]:  #  If puncuation fits, place one on the end of a line (will give the next line an easier start, too)
                        superBlackList, superPopList, expressList, qLineIndexList, proxDicIndexList, qLine = acceptWordR(empLine, superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, runLine, ([all], [all]))
                        break                 
    #$print(lineno(), 'rhymeLiner out:', qLine, 'len(superPopList):', len(superPopList))             
    return superPopList, expressList, superBlackList, usedList, qLine, runLine, False


def lineGovernor(superBlackList, qAnteLine, usedList, rhymeThisLine, rhymeList, empLine):
    #$print(lineno(), 'lineGovernor start', rhymeThisLine)
    superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine, redButton = vetoLine(qAnteLine, [], superBlackList)  #  Start with empty variables declared. This function is also a reset button if lines are to be scrapped.
##    stopTimeM = int(str(datetime.datetime.now())[14:16])
##    stopTimeH = str(datetime.datetime.now())[11:13]
##    if (stopTimeM > (startTimeM + 11)) or ((startTimeH != stopTimeH) and
##                                           (startTimeM < (stopTimeM + 49))):
##        #$print(lineno(), 'timer redButton', startTimeH, startTimeM, '|', stopTimeH, stopTimeM)
##        startTimeM = int(str(datetime.datetime.now())[14:16])
##        startTimeH = str(datetime.datetime.now())[11:13]
##        return [], [], ([],[]), True
              #superBlackList, usedList, qLine, redButton
    if rhymeThisLine == True:
        #$print(lineno(), 'len(rhymeList):', len(rhymeList))
        if (len(rhymeList) > 0):  #  This dictates whether stanzaGovernor sent a rhyming line. An empty line indicates metered-only, or else it would've been a nonzero population
            proxExpress = []
            for each in rhymeList:  #  Find words that come before rhymeWords, so you direct it towards that one
                try:
                    for all in proxMinusLista[:len(empLine)]:  #  Only go as far as the empLine, as if all words are one-syllable long
                        thisProxList = all[each]
                        for proxWord in thisProxList:
                            if proxWord not in proxExpress:
                                proxExpress.append(proxWord)
                except KeyError:
                    continue
            #$print(lineno(), 'len(proxExpress):', len(proxExpress))
            superPopList, expressList, superBlackList, usedList, qLine, runLine, redButton = rhymeLiner(empLine, superPopList, expressList, proxExpress, superBlackList, usedList, rhymeList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
        else:
            #$print(lineno(), 'no rhymes')
            return superBlackList, [], ([],[]), True  #  usedList, qLine, redButton
    elif metSwitch == True:  #  If metSwitch is off, then we wouldn't have either rhyme or meter
        #$print(lineno(), 'lineGov - meterLiner activate')
        superPopList, expressList, superBlackList, usedList, qLine, qAnteLine, redButton = meterLiner(empLine, [], [], superBlackList, usedList, qLineIndexList, proxDicIndexList, qLine, qAnteLine)
    else:
        #$print(lineno(), 'lineGov - plainLiner activate')
        usedList, qLine, redButton = plainLinerLtoR(qAnteLine, usedList, rhymeList, qLineIndexList, proxDicIndexList, empLine)
    if redButton == True:
        #$print(lineno(), 'lineGov - redButton')
        superPopList, expressList, superBlackList, qLineIndexList, proxDicIndexList, qLine, qAnteLine, redButton = vetoLine(qAnteLine, [], superBlackList)
        return superBlackList, [], [], True
    else:
        #$print(lineno(), 'lineGov - last else', qLine)
        return superBlackList, usedList, qLine, False  #  usedList, qLine, redButton
            


################
#  poem building


def vetoStanza(usedList):
    return [], ([],[]), [], int(0), False, False
          #stanza, qAnteLine, usedList, lineCt, redButton


def removeLine(stanza, superBlackList):
    #$print(lineno(), 'removeLine in | len(stanza):', len(stanza))
    if len(stanza) > 0:
        stanzaSnip = stanza.pop()  #  Remove the last line of the stanza
        superBlackList[0].append(stanzaSnip[0][0])  #  Add the first word of the line to blacklist to ensure the repeat doesn't happen
        #$print(lineno(), 'stanzaSnip:', stanzaSnip)
    #$print(lineno(), 'removeLine', len(superBlackList))
    qAnteLine = ([],[])  #  Rebuild qAnteLine, meant to direct the proceeding line(s). Returns empty if stanza empty
    if len(stanza) > 1:
        for each in stanza[-1][0]:
            qAnteLine[0].append(each)
        for each in stanza[-1][1]:
            qAnteLine[1].append(each)
    #$print(lineno(), 'removeLine out | len(stanza):', len(stanza))
    return stanza, superBlackList, qAnteLine


def acceptLine(stanza, superBlackList, newLine):
    #$print(lineno(), 'acceptLine in | len(stanza):', len(stanza))
    stanza.append(newLine)
    superBlackList = [[]]  #  Reset superBlackList to apply to next line
    #$print(lineno(), 'acceptLine in | len(stanza):', len(stanza))
    return stanza, superBlackList, newLine
          #stanza, qAnteLine


def stanzaGovernor(usedList):
    #$print(lineno(), 'stanzaGovernor begin len(rhyMap):', len(rhyMap), 'len(empMap):', len(empMap))
    expressList = []  #  A list of words that go to the front of the line. Declared and left empty, for now
    superBlackList = [[]]  #  Must be declared separate from vetoStanza because it starts empty but may hold screened words
    stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])  #  Creates a fresh stanza, no usedList
    while lineCt < len(rhyMap):
##        global startTimeM, startTimeH
##        startTimeM = int(str(datetime.datetime.now())[14:16])
##        startTimeH = str(datetime.datetime.now())[11:13]
        anteRhyme = lineCt
        if rhySwitch == True:
            anteRhyme = rhyMap.index(rhyMap[lineCt])  #  Use the length of the stanza with rhyMap to determine if a previous line should be rhymed with the current
            #$print(lineno(), 'stanzaGov -', anteRhyme, lineCt)
            #$for each in stanza:
                #$print(each)
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
                        #$print(lineno(), "iE:", rhymeLine, lastWordIndex)
                        return  [], [], True  #  redButton event
                #$print(lineno(), 'stanzaGov - rhymeWord:', rhymeWord)
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
                    #$print(lineno(), 'stanzaGov - rhymer', rhymeWord, '|', rhymeList)
                    superBlackList, usedList, newLine, redButton = lineGovernor(superBlackList, qAnteLine, usedList, rhymeThisLine, rhymeList, empMap[lineCt])  #  If so, we try to create rhyming lines
                else:  #  Our lines created nothing, so we hit a redbutton event
                    return [], [], True
            else:  #  Then you don't need rhymes
                rhymeList = []
                #$print(lineno(), 'stanzaGov -', qAnteLine, usedList, False, rhymeList, empMap[lineCt])
                superBlackList, usedList, newLine, redButton = lineGovernor(superBlackList, qAnteLine, usedList, False, rhymeList, empMap[lineCt])  #
        elif metSwitch == False:
            usedList, newLine, redButton = plainLinerLtoR(qAnteLine, usedList, rhymeList, empMap[lineCt])
        else:
            #$print(lineno(), 'stanzaGov - lineGov')
            superBlackList, usedList, newLine, redButton = lineGovernor(superBlackList, qAnteLine, usedList, rhymeThisLine, [], empMap[lineCt])
        if redButton == True:  #  Not an elif because any of the above could trigger this; must be separate if statement
            #$print(lineno(), 'stanzaGov - redButton')
            if (anteRhyme < lineCt) and (rhySwitch == True):  #  This line cuts back to the rhyming line to try another
                while len(stanza) > anteRhyme:
                    #$print(lineno(), 'removing rhyLine from: ', stanza)
                    stanza, superBlackList, qAnteLine = removeLine(stanza, superBlackList)
                #$print(lineno(), stanza)
##            stopTimeM = int(str(datetime.datetime.now())[14:16])
##            stopTimeH = str(datetime.datetime.now())[11:13]
##            if (stopTimeM > (startTimeM + 11)) or ((startTimeH != stopTimeH) and
##                                           (startTimeM < (stopTimeM + 49))):
##                #$print(lineno(), 'timer redButton', startTimeH, startTimeM, '|', stopTimeH, stopTimeM)
##                stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])  #  Creates a fresh stanza, no usedList
##            else:
            else:
                #$print(lineno(), 'regular line remove: ', stanza)
                stanza, superBlackList, qAnteLine = removeLine(stanza, superBlackList)
        elif len(newLine[1]) > 0:  #  Line-building functions will either return a valid, nonzero-length line, or trigger a subtraction in the stanza with empty list
            #$print(lineno(), 'stanzaGov - newLine:', newLine)
            stanza, superBlackList, qAnteLine = acceptLine(stanza, superBlackList, newLine)
        elif len(stanza) > 0:  #  Check if the stanza is nonzero-length, otherwise there's nothing to subtract, resulting in an error
            stanza, superBlackList, qAnteLine = removeLine(stanza, superBlackList)
        else:  #  Redundant, as the stanza should logically be vetoed already, but just to clean house
            #$print(lineno(), 'stanzaGov - vetoStanza')
            #stanza, qAnteLine, usedList, lineCt, rhymeThisLine, redButton = vetoStanza([])
            stanza, superBlackList, qAnteLine = removeLine(stanza, superBlackList)
        lineCt = len(stanza)  #  Count the length of the stanza, provided no redButton events occurred...
        #$print(lineno(), 'end whileloop', lineCt)

    return stanza, usedList, redButton


############0####
#  poem building


def vetoPoem():
    return [], [], 0, False
          #poem, usedList, stanzaCt, redButton


def poemGovernor(usedList):  #  Outlines the parameters of the poem
    #$print(lineno(), 'poemGovernor initialized\n'+str(time.ctime())+'\n')
    #$print(rhyMap, '+', empMap, '+', usedList)
    poem, usedList, stanzaCt, redButton = vetoPoem()
    while len(poem) < stanzaQuota:
        stanza, usedList, redButton = stanzaGovernor(usedList)
        #$print(lineno(), 'gotStanza\n')
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
            #$print(thisString[1].upper()+thisString[2:])
#        input('press enter to continue')
            writtenStanza+=thisString[1].upper()+thisString[2:]+'\n'
        #$print('\n')
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


def main__init(defaultSwitch0, language0, accent0, textFile0, poemQuota0, stanzaQuota0, rhyMap0, empMap0, usedSwitch0, rhySwitch0, metSwitch0, thesSwitch0, proxMinDial0, proxMaxDial0, punxProxNum0):


    contSwitch0 = True
    #  Returns error if these are declared global directly, so this is just a switch to make these global
    global defaultSwitch, language, accent, textFile, poemQuota, stanzaQuota, rhyMap, empMap, usedSwitch, rhySwitch, metSwitch, thesSwitch, contSwitch, proxMinDial, proxMaxDial, punxProxNum
    defaultSwitch, language, accent, textFile, poemQuota, stanzaQuota, rhyMap, empMap, usedSwitch, rhySwitch, metSwitch, thesSwitch, contSwitch, proxMinDial, proxMaxDial, punxProxNum = defaultSwitch0, language0, accent0, textFile0, poemQuota0, stanzaQuota0, rhyMap0, empMap0, usedSwitch0, rhySwitch0, metSwitch0, thesSwitch0, contSwitch0, proxMinDial0, proxMaxDial0, punxProxNum0

    global lang
    #$print(lineno(), 'defaultSwitch:', defaultSwitch)
    if defaultSwitch == True:  #  Preset values so you don't have to type everything every time you start the program
        lang = 'eng'
        accent = 'USen'
        empMode = 'USen-unik'
        textFile = 'ulysses'
        poemQuota = 20
        stanzaQuota = 1
        proxMinDial = int(2)
        proxMaxDial = int(20)
        punxProxNum = int(3)
        usedSwitch = False
        rhySwitch = True
        metSwitch = True
        thesSwitch = True
        rhyMap = 'aa'
        empMap = [[bool(0), bool(1), bool(0), bool(1), bool(0), bool(1), bool(0), bool(1)],
                  #[bool(0), bool(1), bool(0), bool(1), bool(0), bool(1), bool(0), bool(1)],
                  #[bool(0), bool(1), bool(0), bool(1), bool(0), bool(1), bool(0), bool(1)],
                  [bool(0), bool(1), bool(0), bool(1), bool(0), bool(1), bool(0), bool(1)]]

    if language == 'English':
        lang = 'eng'
    elif language == 'Espanol':
        lang = 'esp'

        
    #textFile = 'bibleX'
    #$print(lineno(), 'initializing program', str(time.ctime())[11:20], '\ntextFile:', textFile, '\nrhyMap:', rhyMap, '\nempMap:')
    #$for each in empMap:
        #$print(each)
    #########################
    #  Static data, will change with GUI and testVals progs

##    values = guiInterface()
    global rhyDic
    rhyDic = defaultdict(list)

     
    global rawText
    rawText = str(open(lang+'/data/textLibrary/'+textFile+'.txt', 'r', encoding='latin-1').read())
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

    #global proxMinDial, proxMaxDial, punxProxNum


    stanza, usedList = [], []

    unknownWords = open(lang+'/data/unknownWords.txt', 'a')

    contractionFile = open(lang+'/data/'+accent+'/contractionList.txt', 'r')
    contractionSwitch = csv.reader(open(lang+'/data/'+accent+'/contractionSwitches.csv', 'r+'))
    global contractionDic, contractionList  #  These are immutable and should be accessed wherever
    contractionDic = defaultdict(list)  #  Use a dictionary to look up contraction switches
    contractionList = []  #  Use a list to check if the contraction exists (circumvents excepting KeyErrors)
    for line in contractionFile:  #  Makes a dictionary of contractions
        contractionList.append(line[:-1])  #  Remove '\n' before appending
    #$print(lineno(), 'len(contractionList):', len(contractionList), contractionList[:10])
    try:
        for line in contractionSwitch:
            #if "'s" not in line[0]:  #  There's a problem with whether the line is a possessive or contraction of "___ is"
            contractionDic[line[0]] = line[1]
    except IndexError:
        contractionDic = defaultdict(list)
    ##$print(contractionDic)
    #$print(lineno(), 'len(contractionDic):', len(contractionDic), contractionDic["can't"], contractionDic["don't"])
        
        
    global rSyls
    rSyls = 2

    global thesDic 
    thesDic = {}
    try:
        thesaurusFile = csv.reader(open(lang+'/data/textLibrary/textData/'+textFile+'-thesaurusFile.csv', 'r'))
        #$print(lineno(), 'loading thesDic...')
        for line in thesaurusFile:
            thesWords = line[1].split('^')
            thesDic[line[0]] = []
            for all in thesWords:
                if (len(all) > 0) and (all not in allPunx) and (all != line[0]):
                    thesDic[line[0]].append(all)
        
    except FileNotFoundError:
        #$print(lineno(), 'building thesDic...')
        thesaurusFile = csv.writer(open(lang+'/data/textLibrary/textData/'+textFile+'-thesaurusFile.csv', 'w+'))
        for all in splitText:
            finalList = []
            try:
                #$print('\n.\n')
                thesDic[all]  #  Test to see if the thesaurus has an entry already
            except KeyError:
                try:
                    syns = wn.synsets(all)
                    for each in syns:
                        wordData = str(each).split("'")
                        synList = [str(lemma.name()) for lemma in wn.synset(wordData[1]).lemmas()]
                        for syn in synList:
                            if (syn not in finalList) and (syn != all) and (len(syn) > 0) and (syn not in allPunx):
                                finalList.append(syn)
                    #$print('thesaurus['+all+']:', finalList)
                    thesDic[all] = finalList
                    thesLine = str()
                    for each in finalList:
                        thesLine+=(each+'^')
                    thesaurusFile.writerow([all, thesLine[:-1]])
                except ValueError:
                    #$print('ValueError:', all)
                    continue

    
    #
    ##########################


    #$print('opening fonoFiles')  #  These are global values, so they need to be opened regardless
    global emps
    emps = gF.globalOpen(lang+'/data/'+accent+'/empDic-'+empMode+'.csv', 'lista')
    for key, val in emps.items():  #  Stored as ints because could be numbers up to 2. Change to bools
        boolSwitch = []
        for each in val:
            if each == '1':
                boolSwitch.append(bool(True))
            else:
                boolSwitch.append(bool(False))
        emps[key] = boolSwitch
    vocs = gF.globalOpen(lang+'/data/'+accent+'/vocDic-USen-MAS.csv', 'lista')
    cons = gF.globalOpen(lang+'/data/'+accent+'/conDic-USen-MAS.csv', 'lista')
    fono = gF.globalOpen(lang+'/data/'+accent+'/fonDic-USen-MAS.csv', 'lista')
    
    # if rhySwitch == on, load rhyming dictionary here
    # write it in __gloFunk
    
    #$print(lineno(), 'len(emps):', len(emps))
    #$print(lineno(), 'opening doubles')
    global doubles
    doubles = []
    for key, val in emps.items():
        if '(' in key:
            doubles.append(key[:-3])
    #$print(lineno(), "rhySwitch =", rhySwitch)
    loadmakeData(lang, textFile, proxPlusLista, proxMinusLista)  #  Loads the data needed or makes it
    poemCt = int(0)
    print('PROGRAM INITIALIZED | ', str(time.ctime())[11:20], '\n')
    while poemCt < poemQuota:
        poem, usedList = poemGovernor(stanzaQuota)
        poemCt+=1
        print('Poem #'+str(poemCt), '|', str(time.ctime())[11:20])
        for each in poem:
            print(each, '\n')
        #$input('paused')

    print('PROGRAM FINISHED')

#main__init() #  and now that everything's in place, set it off!

##  END
