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

#  Organization of variables: empLine, qEmpLine, superPopList, rhymeList, qLineIndexList, proxDicIndexList, qWord, qLine, qAnteLine, redButton


##########
##  declaration of libraries
##########

#  External, pre-existing libraries
from string import *
import tkinter as tk
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

#  Internal, self-created file
import _gloFunk as gFunk
import _proxFunk as pFunk
import remezcla_gui as wemyxGUI
import poemGovernor as poemG
import stanzaGovernor as stanzaG
import lineGovernor as lineG
import meterGovernor as meterG
import popListGovernor as popListG

##########
##  basic, essential, universal functions & lists
##########


def lineno():     ##  Returns the current line number in our program.
    return inspect.currentframe().f_back.f_lineno

global quantumList  #  List of words used for quantum emp patterns
quantumList = ['was', 'be', 'and', 'to', 'for', 'a', 'the', 'in', 'at', 'but', 'an',
               'not', 'is', 'do', 'did', 'can', 'could', 'will', 'does', 'of', 'as',
               'when', 'than', 'then', 'my', 'your', 'too', 'would', 'should']  
nonEnders = ['and', 'or', 'a', 'but', 'the', 'an', ',', ';', ':', '--']

allPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '"', "''", '-', '\\', '+', '=', '/', '<', '>', '(', ')']  #  Doesn't include apostrophe, because that could be part of a contraction
midPunx = [',', ';', ':', '--']
endPunx = ['.', '!', '?']  #  To gather which words immediately thereafter should start a sentence

bannedChops = ['@', '#', '&', '*', '\\', '+', '=', '/', '<', '>']


def main__init(defaultSwitch0, language0, accent0, textFile0, poemQuota0, stanzaQuota0, rhyMap0, empMap0, usedSwitch0, rhySwitch0, metSwitch0, thesSwitch0, proxMinDial0, proxMaxDial0, punxProxNum0):


    contSwitch0 = True
    #  Returns error if these are declared global directly, so this is just a switch to make these global
    global defaultSwitch, language, accent, textFile, poemQuota, stanzaQuota
    global rhyMap, empMap, usedSwitch, rhySwitch, metSwitch, thesSwitch, contSwitch
    global proxMinDial, proxMaxDial, punxProxNum
    defaultSwitch, language, accent, textFile, poemQuota, stanzaQuota, rhyMap, empMap, usedSwitch, rhySwitch, metSwitch, thesSwitch, contSwitch, proxMinDial, proxMaxDial, punxProxNum = defaultSwitch0, language0, accent0, textFile0, poemQuota0, stanzaQuota0, rhyMap0, empMap0, usedSwitch0, rhySwitch0, metSwitch0, thesSwitch0, contSwitch0, proxMinDial0, proxMaxDial0, punxProxNum0

    global lang
    print(lineno(), 'defaultSwitch:', defaultSwitch)
    if defaultSwitch == True:  #  Preset values so you don't have to type everything every time you start the program
        lang = 'eng'
        accent = 'USen'
        empMode = 'USen-unik'
        textFile = 'bibleX'
        poemQuota = 100
        stanzaQuota = 1
        proxMinDial = int(3)
        proxMaxDial = int(20)
        punxProxNum = int(3)
        usedSwitch = False
        rhySwitch = True
        metSwitch = True
        thesSwitch = True
        rhyMap = 'abab'
        empMap = [[bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)],
                  [bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)],
                  [bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)],
                  #[bool(0), bool(1), bool(0), bool(0), bool(1)],
                  [bool(0), bool(1), bool(0), bool(0), bool(1), bool(0), bool(1)]]

    if language == 'English':
        lang = 'eng'
    elif language == 'Espanol':
        lang = 'esp'
          
    #########################
    #  Static data, will change with GUI and testVals progs

##    values = guiInterface()
    global rhyDic
    rhyDic = defaultdict(list)

     
    global rawText
    rawText = str(open(lang+'/data/textLibrary/'+textFile+'.txt', 'r', 
                  encoding='utf-8').read())
    nullSpace = ''  #  Certain characters will be replaced by null character
    nullReplace = ['- \n', '-\n', '\n']  #  Hyphen at the end of lines indicates words that are broken
    whiteSpace = ' '  #  Whitespace erases characters, then whitespace shrinks itself
    whiteReplace = ['_', '^', '~', '     ', '    ', '   ', '  ']
    
    rawText = rawText.replace('``', '"')
    rawText = rawText.replace("''", '"')
    rawText = rawText.replace('`', "'")
    rawText = rawText.replace('&', ' and ')
    for all in allPunx:  #  Put a space around punctuation to tokenize later
        rawText = rawText.replace(all, ' '+all+' ')
    for nullSpaceVictims in nullReplace:
        rawText = rawText.replace(nullSpaceVictims, nullReplace)
    for whiteSpaceVictims in whiteReplace:
        rawText = rawText.replace(whiteSpaceVictims, whiteReplace)  

    rawText = rawText.lower()

    #  Tokenizes raw text, grooms into lists of words
    global splitText
    splitText = rawText.split(' ')  # The reason for placing a space between all tokens to be grabbed

    global proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9
    global proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17
    global proxP18, proxP19, proxP20
    global proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9
    global proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17
    global proxM18, proxM19, proxM20
    global proxPlusLista, proxMinusLista, proxLib # gramProxLib, gramProxPlusLista, gramProxMinusLista
    #  These dictionaries contain lists of words that come after
    proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    #  The dictionaries are organized into lists that are accessed by index. Useful in while loops with ascending/descending numbers
    proxPlusLista = [proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17, proxP18, proxP19, proxP20]
    proxMinusLista = [proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17, proxM18, proxM19, proxM20]

    #global proxMinDial, proxMaxDial, punxProxNum

    unknownWords = open(lang+'/data/unknownWords.txt', 'a')

    contractionFile = open(lang+'/data/'+accent+'/contractionList.txt', 'r')
    contractionSwitch = csv.reader(open(lang+'/data/'+accent+'/contractionSwitches.csv', 'r+'))
    global contractionDic, contractionList  #  These are immutable and should be accessed wherever
    contractionDic = defaultdict(list)  #  Use a dictionary to look up contraction switches
    contractionList = []  #  Use a list to check if the contraction exists (circumvents excepting KeyErrors)
    for line in contractionFile:  #  Makes a dictionary of contractions
        contractionList.append(line[:-1])  #  Remove '\n' before appending
    print(lineno(), 'len(contractionList):', len(contractionList), contractionList[:10])
    try:
        for line in contractionSwitch:
            #if "'s" not in line[0]:  #  There's a problem with whether the line is a possessive or contraction of "___ is"
            contractionDic[line[0]] = line[1]
    except IndexError:
        contractionDic = defaultdict(list)
    #print(contractionDic)
    print(lineno(), 'len(contractionDic):', len(contractionDic), contractionDic["can't"],
          contractionDic["don't"])
        
        
    global rSyls
    rSyls = 2

    global thesDic 
    thesDic = {}
    try:
        thesaurusFile = csv.reader(open(lang+'/data/textLibrary/textData/'
                                        +textFile+'-thesaurusFile.csv', 'r'))
        print(lineno(), 'loading thesDic...')
        for line in thesaurusFile:
            thesWords = line[1].split('^')
            thesDic[line[0]] = []
            for all in thesWords:
                if (len(all) > 0) and (all not in allPunx) and (all != line[0]):
                    thesDic[line[0]].append(all)
        
    except FileNotFoundError:
        print(lineno(), 'building thesDic...')
        thesaurusFile = csv.writer(open(lang+'/data/textLibrary/textData/'+textFile+'-thesaurusFile.csv', 'w+'))
        for all in splitText:
            finalList = []
            try:
                #print('\n.\n')
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
                    #print('thesaurus['+all+']:', finalList)
                    thesDic[all] = finalList
                    thesLine = str()
                    for each in finalList:
                        thesLine+=(each+'^')
                    thesaurusFile.writerow([all, thesLine[:-1]])
                except ValueError:
                    print('ValueError:', all)
                    continue

    
    #
    ##########################


    print('opening fonoFiles')  #  These are global values, so they need to be opened regardless
    global emps
    emps = gFunk.globalOpen(lang+'/data/'+accent+'/empDic-'+empMode+'.csv', 'lista')
    for key, val in emps.items():  #  Stored as ints because could be numbers up to 2. Change to bools
        boolSwitch = []
        for each in val:
            if each == '1':
                boolSwitch.append(bool(True))
            else:
                boolSwitch.append(bool(False))
        emps[key] = boolSwitch
    vocs = gFunk.globalOpen(lang+'/data/'+accent+'/vocDic-USen-MAS.csv', 'lista')
    cons = gFunk.globalOpen(lang+'/data/'+accent+'/conDic-USen-MAS.csv', 'lista')
    fono = gFunk.globalOpen(lang+'/data/'+accent+'/fonDic-USen-MAS.csv', 'lista')
    
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
                                                 
    loadmakeData(lang, textFile, proxPlusLista, proxMinusLista)  #  Loads the data needed or makes it

    global superPopList, expressList, thesList, contList, punxList, superBlackList, qLineIndexList, proxDicIndexList, usedList
    superPopList, expressList, thesList, contList, punxList, superBlackList, qLineIndexList, proxDicIndexList, usedList = [[]], [[]], [[]], [[]], [[]], [[]], [], [], []

    global metaList
    metaList = superPopList, expressList, thesList, contList, punxList, qLineIndexList, proxDicIndexList
    
    print(lineno(), '_m_ | initializing program', str(time.ctime())[11:20], 
          '\ntextFile:', textFile, '\npoem template:')
    mapInt = int(0)
    while mapInt < len(rhyMap):
        mapWriteLine = str()
        mapWriteLine+=(rhyMap[mapInt]+' | ')
        for each in empMap[mapInt]:
            if each == True:
                mapWriteLine+='1'
            else:
                mapWriteLine+='0'
        print(mapWriteLine)
        mapInt+=1

    poemCt = int(0)
    print('_m_ |', lineno(), 'PROGRAM INITIALIZED | ', str(time.ctime())[11:20], '\n')
    while poemCt < poemQuota:
        poem, usedList = poemGovernor(stanzaQuota)
        poemCt+=1
        print('Poem #'+str(poemCt), '|', str(time.ctime())[11:20])
        for each in poem:
            print(each, '\n')
        input('paused')

    print('_m_ |', lineno(), 'PROGRAM FINISHED')

defaultSwitch0, language0, accent0, textFile0, poemQuota0, stanzaQuota0, rhyMap0, empMap0, usedSwitch0, rhySwitch0, metSwitch0, thesSwitch0, proxMinDial0, proxMaxDial0, punxProxNum0 = wemyxGUI.main()

main__init(defaultSwitch0, language0, accent0, textFile0, poemQuota0, stanzaQuota0, 
           rhyMap0, empMap0, usedSwitch0, rhySwitch0, metSwitch0, thesSwitch0, 
           proxMinDial0, proxMaxDial0, punxProxNum0)
