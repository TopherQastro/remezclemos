
"""
This file allows each file to utilize global variables with 'import',
Removes a great deal of redundancy and clutter for this set of code.
"""

#  External, pre-existing libraries
from collections import defaultdict as dd
import csv
csv.field_size_limit(int(9999999))
import datetime
import inspect
import nltk
from nltk.corpus import wordnet as wn
import pygubu
import random
import shelve
import sqlite3
from string import *
import time
import tkinter as tk
from tkinter import messagebox

#  Internal, self-created files
import alternateFunctions as altFunk
import dynasaurusFunctions as dynaFunk
import fonoFunctions as fonoFunk
import guiFunctions as guiFunk
import lineFunctions as lineFunk
import meterLineFunctions as meterFunk
import plainLineFunctions as plainFunk
import poemFunctions as poemFunk
import popFunctions as popFunk
import proximityFunctions as proxFunk
import rawtextFunctions as rawtextFunk
import rhymeFunctions as rhyFunk
import stanzaFunctions as stanzaFunk


def lineno():     ##  Returns the current line number in our program.
    return inspect.currentframe().f_back.f_lineno


def begin():
    global defaultSwitch, usedSwitch, rhySwitch, metSwitch, thesSwitch, contSwitch
    global language, lang, accent, textFile, empMode
    global poemQuota, stanzaQuota, proxMaxDial, proxMinDial, punxDial
    global rhyMap, empMap, usedList, firstWords, firstPopList
    defaultSwitch, usedSwitch, rhySwitch, metSwitch, thesSwitch, contSwitch = True, True, True, True, True, True
    language, lang, accent, textFile, empMode = str(), str(), str(), str(), str()
    poemQuota, stanzaQuota, proxMaxDial, proxMinDial, punxDial = int(0), int(0), int(0), int(0), int(0)
    rhyMap, empMap, usedList, firstWords, firstPopList = [], [], [], [], []

    global superList, superPopList, expressList, thesList, dynaList, contList, punxList, superBlackList, qLineIndexList, proxDicIndexList
    superList, superPopList, expressList, thesList, dynaList, contList, punxList, superBlackList, qLineIndexList, proxDicIndexList = [], [], [], [], [], [], [], [], [], []
    superList = superPopList, expressList, thesList, dynaList, contList, punxList, superBlackList, qLineIndexList, proxDicIndexList

    global quantumList, nonEnders, upperAlphabet, lowerAlphabet, allPunx, midPunx, endPunx, deadPunx #  List of words used for quantum emp patterns
    quantumList = ['was', 'be', 'and', 'to', 'for', 'a', 'the', 'in', 'at', 'but', 'an',
                'not', 'is', 'do', 'did', 'can', 'could', 'will', 'does', 'of', 'as',
                'when', 'than', 'then', 'my', 'your', 'too', 'would', 'should', 'he', 'him',
                'his', 'she', 'her', 'hers', 'they', 'them', 'their', "they're", 'there',
                'have', 'had', 'has', 'must', 'with', 'i', 'from', 'through', 'now', 'on'] 
    nonEnders = ['and', 'or', 'a', 'but', 'the', 'an', ',', ';', ':', '--'] #  Words that don't sound well ending a sentence
    upperAlphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                     'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    lowerAlphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                     'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    allPunx = ['.', ',', ';', ',', ':', '!', '?', '--', '"', "''", '-', '\\', '+',
            '=', '/', '<', '>', '(', ')']  #  Doesn't include apostrophe, because
                                           #  that could be part of a contraction
    midPunx = [',', ';', ':', '--']
    endPunx = ['.', '!', '?']  #  To gather which words immediately thereafter should start 
                               #  a sentence
    deadPunx = ['(', ')', '<', '>', '"', '[', ']']


    vocsList = ['a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'V', 'Y', '3', '0', '@', '&', 'L', 'M',  'N', '%', '!', '#', '$', '^', '*', '(', ')', '?', '<', '>', '.', '|', ']', '[', '=']
    vow = 'y', 'a', 'e', 'i', 'o', 'u', 'ü', 'â', 'ê', 'è', 'ô', 'ö', 'õ', 'à', 'è', 'î', 'ã', 'ë', 'ä', 'ê', 'ĩ', 'ï', 'ũ', 'ü', 'û', 'ī', 'ū', '4', '5', '6', '7', '8', '9', '0', '@', '#', '$', '%', '&', '!', '?', '<', '.', ':', ';', '(', ')', '[', ']', '{', '}', '1', '2'
    accVow = 'á', 'é', 'ó', 'í', 'ú', 'ĕ', 'ė', 'ŏ', 'ő', 'ă', 'ą', 'Ə', 'ů', 'œ', 'þ', 'ø', 'æ'
    allVow = 'y', 'a', 'e', 'i', 'o', 'u', 'ü', 'á', 'é', 'ó', 'í', 'ú', 'â', 'ê', 'è', 'ô', 'ö', 'õ', 'à', 'è', 'î', 'ã', 'ë', 'ä', 'ê', 'ĩ', 'ï', 'ũ', 'ü', 'û', 'ī', 'ū', 'ĕ', 'ė', 'ŏ', 'ő', 'ă', 'ą', 'Ə', 'ů', 'œ', 'þ', 'ø', 'æ', '4', '5', '6', '7', '8', '9', '0', '@', '#', '$', '%', '&', '!', '?', ',', '.', ':', ';', '(', ')', '[', ']', '{', '}', '1', '2'
    espEmpPat1 = 's', 'n', 'a', 'e', 'i', 'o', 'u', 'y', 'ë', 'ä', 'ã', 'õ', 'ö', 'ê', 'ĩ', 'î', 'ï', 'ũ', 'ü', 'û', 'ī', 'ū'
    strippers = '”', '’', "'", '…', '…', '—', '·', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '@', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']', '{', '}', '<', '>', '"', ',', '!', '.', ',', '‘', '’', '`', '~', '/', '+', '=', '|', '\c', '\n', '?', ';', ':', '_', '-', '¿', '»', '«', '¡', '©', '“', '”', 'º', '/', '\c'
    spacers = '\n\n\n', '\n\n', '\n', '    ', '      ', '     ', '    ', '   ', '  '
    caps =  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ü'


    global rawText
    global splitText
    rawText = str()
    splitText = []

    #  These dictionaries organize the splitText words alphabetically based on 1st letter
    global splitTextA, splitTextB, splitTextC, splitTextD, splitTextE, splitTextF, splitTextG
    global splitTextH, splitTextI, splitTextJ, splitTextK, splitTextL, splitTextM, splitTextN
    global splitTextO, splitTextP, splitTextQ, splitTextR, splitTextS, splitTextT, splitTextU
    global splitTextV, splitTextW, splitTextX, splitTextY, splitTextZ, splitDics

    splitTextA, splitTextB, splitTextC, splitTextD = [], [], [], []
    splitTextE, splitTextF, splitTextG, splitTextH = [], [], [], []
    splitTextI, splitTextJ, splitTextK, splitTextL = [], [], [], []
    splitTextM, splitTextN, splitTextO, splitTextP = [], [], [], []
    splitTextQ, splitTextR, splitTextS, splitTextT = [], [], [], []
    splitTextU, splitTextV, splitTextW, splitTextX = [], [], [], []
    splitTextY, splitTextZ = [], []

    splitDics = [splitTextA, splitTextB, splitTextC, splitTextD, splitTextE, splitTextF, splitTextG, splitTextH, splitTextI, splitTextJ, splitTextK, splitTextL, splitTextM, splitTextN, splitTextO, splitTextP, splitTextQ, splitTextR, splitTextS, splitTextT, splitTextU, splitTextV, splitTextW, splitTextX, splitTextY, splitTextZ]

    global proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, proxP9
    global proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, proxP16, proxP17
    global proxP18, proxP19, proxP20, proxP21, proxP22, proxP23, proxP24
    global proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, proxM9
    global proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, proxM16, proxM17
    global proxM18, proxM19, proxM20, proxM21, proxM22, proxM23, proxM24
    global proxPlusLista, proxMinusLista, proxLib, proxPlusStrings, proxMinusStrings # gramProxLib, gramProxPlusLista, gramProxMinusLista
    proxP1, proxP2, proxP3, proxP4, proxP5 = dd(list), dd(list), dd(list), dd(list), dd(list) 
    proxP6, proxP7, proxP8, proxP9, proxP10 = dd(list), dd(list), dd(list), dd(list), dd(list)
    proxP11, proxP12, proxP13, proxP14, proxP15 = dd(list), dd(list), dd(list), dd(list), dd(list)
    proxP16, proxP17, proxP18, proxP19, proxP20 = dd(list), dd(list), dd(list), dd(list), dd(list)
    proxP21, proxP22, proxP23, proxP24 = dd(list), dd(list), dd(list), dd(list)
    proxM1, proxM2, proxM3, proxM4, proxM5 = dd(list), dd(list), dd(list), dd(list), dd(list) 
    proxM6, proxM7, proxM8, proxM9, proxM10 = dd(list), dd(list), dd(list), dd(list), dd(list)
    proxM11, proxM12, proxM13, proxM14, proxM15 = dd(list), dd(list), dd(list), dd(list), dd(list)
    proxM16, proxM17, proxM18, proxM19, proxM20 = dd(list), dd(list), dd(list), dd(list), dd(list)
    proxM21, proxM22, proxM23, proxM24 = dd(list), dd(list), dd(list), dd(list)
    proxPlusLista = [proxP1, proxP2, proxP3, proxP4, proxP5, proxP6, proxP7, proxP8, 
                        proxP9, proxP10, proxP11, proxP12, proxP13, proxP14, proxP15, 
                        proxP16, proxP17, proxP18, proxP19, proxP20, proxP21, proxP22, 
                        proxP23, proxP24]
    proxMinusLista = [proxM1, proxM2, proxM3, proxM4, proxM5, proxM6, proxM7, proxM8, 
                      proxM9, proxM10, proxM11, proxM12, proxM13, proxM14, proxM15, 
                      proxM16, proxM17, proxM18, proxM19, proxM20, proxM21, proxM22, 
                      proxM23, proxM24]
    proxPlusStrings = ['proxP1', 'proxP2', 'proxP3', 'proxP4', 'proxP5', 'proxP6', 'proxP7', 'proxP8',
                        'proxP9', 'proxP10', 'proxP11', 'proxP12', 'proxP13', 'proxP14', 'proxP15',
                        'proxP16', 'proxP17', 'proxP18', 'proxP19', 'proxP20', 'proxP21', 'proxP22', 
                        'proxP23', 'proxP24']
    proxMinusStrings = ['proxM1', 'proxM2', 'proxM3', 'proxM4', 'proxM5', 'proxM6', 'proxM7', 'proxM8',
                        'proxM9', 'proxM10', 'proxM11', 'proxM12', 'proxM13', 'proxM14', 'proxM15', 
                        'proxM16', 'proxM17', 'proxM18', 'proxM19', 'proxM20', 'proxM21', 'proxM22',
                        'proxM23', 'proxM24']



    global startTime, stopTime
    startTime = time.time()
    stopTime = time.time()

    global rSyls
    rSyls = 2

    global unknownWords, doubles
    unknownWords, doubles = [], []
    doubles_file = open('eng/data/USen/doubleList.txt', 'r')
    print('gloF:', lineno(), 'building doubles...')
    for line in doubles_file:
        line = line.replace('\n', '')  #  Take out \n from line
        doubles.append(line)
    print('gloF:', lineno(), 'len(doubles):', len(doubles))
    # for doubs in doubles:
    #     print('doubled word:', doubs)


    global contDic, contractionList  #  These are immutable and should be accessed wherever
    contDic = dd(list)  #  Use a dictionary to look up contraction switches
    contractionList = []  #  Use a list to check if the contraction exists (circumvents excepting KeyErrors)

    global thesDic 
    thesDic = dd(list)

    global fonoSwitch, vocsSwitch, consSwitch, empsSwitch

    global soundsLine
    soundsLine = [[],[],[],[]]

    # fono, vocs, cons, and emps are organized into alphabetical dictionaries
    global soundDicsIndex
    soundDicsIndex = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 
                     'I':8, 'J':9, 'K':10, 'L':11, 'M':12, 'N':13, 'O':14, 'P':15, 
                     'Q':16, 'R':17, 'S':18, 'T':19, 'U':20, 'V':21, 'W':22, 'X':23, 
                     'Y':24, 'Z':25}


    global fonoA, fonoB, fonoC, fonoD, fonoE, fonoF, fonoG
    global fonoH, fonoI, fonoJ, fonoK, fonoL, fonoM, fonoN
    global fonoO, fonoP, fonoQ, fonoR, fonoS, fonoT, fonoU
    global fonoV, fonoW, fonoX, fonoY, fonoZ, fonoDics

    fonoA, fonoB, fonoC, fonoD = {}, {}, {}, {}
    fonoE, fonoF, fonoG, fonoH = {}, {}, {}, {}
    fonoI, fonoJ, fonoK, fonoL = {}, {}, {}, {}
    fonoM, fonoN, fonoO, fonoP = {}, {}, {}, {}
    fonoQ, fonoR, fonoS, fonoT = {}, {}, {}, {}
    fonoU, fonoV, fonoW, fonoX = {}, {}, {}, {}
    fonoY, fonoZ = {}, {}

    fonoDics = [fonoA, fonoB, fonoC, fonoD, fonoE, fonoF, fonoG, fonoH, fonoI, 
                fonoJ, fonoK, fonoL, fonoM, fonoN, fonoO, fonoP, fonoQ, fonoR, 
                fonoS, fonoT, fonoU, fonoV, fonoW, fonoX, fonoY, fonoZ]

    global vocsA, vocsB, vocsC, vocsD, vocsE, vocsF, vocsG
    global vocsH, vocsI, vocsJ, vocsK, vocsL, vocsM, vocsN
    global vocsO, vocsP, vocsQ, vocsR, vocsS, vocsT, vocsU
    global vocsV, vocsW, vocsX, vocsY, vocsZ, vocsDics

    vocsA, vocsB, vocsC, vocsD = {}, {}, {}, {}
    vocsE, vocsF, vocsG, vocsH = {}, {}, {}, {}
    vocsI, vocsJ, vocsK, vocsL = {}, {}, {}, {}
    vocsM, vocsN, vocsO, vocsP = {}, {}, {}, {}
    vocsQ, vocsR, vocsS, vocsT = {}, {}, {}, {}
    vocsU, vocsV, vocsW, vocsX = {}, {}, {}, {}
    vocsY, vocsZ = {}, {}

    vocsDics = [vocsA, vocsB, vocsC, vocsD, vocsE, vocsF, vocsG, vocsH, vocsI, 
                vocsJ, vocsK, vocsL, vocsM, vocsN, vocsO, vocsP, vocsQ, vocsR, 
                vocsS, vocsT, vocsU, vocsV, vocsW, vocsX, vocsY, vocsZ]

    global consA, consB, consC, consD, consE, consF, consG
    global consH, consI, consJ, consK, consL, consM, consN
    global consO, consP, consQ, consR, consS, consT, consU
    global consV, consW, consX, consY, consZ, consDics

    consA, consB, consC, consD = {}, {}, {}, {}
    consE, consF, consG, consH = {}, {}, {}, {}
    consI, consJ, consK, consL = {}, {}, {}, {}
    consM, consN, consO, consP = {}, {}, {}, {}
    consQ, consR, consS, consT = {}, {}, {}, {}
    consU, consV, consW, consX = {}, {}, {}, {}
    consY, consZ = {}, {}

    consDics = [consA, consB, consC, consD, consE, consF, consG, consH, consI, 
                consJ, consK, consL, consM, consN, consO, consP, consQ, consR, 
                consS, consT, consU, consV, consW, consX, consY, consZ]

    global empsA, empsB, empsC, empsD, empsE, empsF, empsG
    global empsH, empsI, empsJ, empsK, empsL, empsM, empsN
    global empsO, empsP, empsQ, empsR, empsS, empsT, empsU
    global empsV, empsW, empsX, empsY, empsZ, empsDics

    empsA, empsB, empsC, empsD = {}, {}, {}, {}
    empsE, empsF, empsG, empsH = {}, {}, {}, {}
    empsI, empsJ, empsK, empsL = {}, {}, {}, {}
    empsM, empsN, empsO, empsP = {}, {}, {}, {}
    empsQ, empsR, empsS, empsT = {}, {}, {}, {}
    empsU, empsV, empsW, empsX = {}, {}, {}, {}
    empsY, empsZ = {}, {}

    empsDics = [empsA, empsB, empsC, empsD, empsE, empsF, empsG, empsH, empsI, 
                empsJ, empsK, empsL, empsM, empsN, empsO, empsP, empsQ, empsR, 
                empsS, empsT, empsU, empsV, empsW, empsX, empsY, empsZ]


    global sound_file, soundConn, soundCursor
    sound_file = 'eng/data/USen/USen_fonoDB.db'
    soundConn = sqlite3.connect(sound_file)
    soundCursor = soundConn.cursor()
    global prox_file, proxConn, proxCursor
    global rhyme_file, rhyme_conn, rhymeCursor
    # rhyme_file = sqlite3.connect(#sql database)
    # rhymeConn = sqlite3.connect(rhyme_file)
    # rhymeCursor = rhymeConn.cursor()


def printGlobalData(qLine):
    print('gF:', lineno(), '| printGlobalData() -', len(qLine[1]), qLine[1])
    # if len(superPopList) > 0:
    #     print('gF:', lineno(), 'printGlobalData() |', superPopList[-1], expressList[-1])
    print('gF:', lineno(), '| printGlobalData() - sPpL, expL, thes, dyna, cont, pnxL, sBkL, qLIL, pLDL')
    indInt = int(0)
    print(qLineIndexList, proxDicIndexList)
    for lists in superList:
        if len(lists) > 0:
            listsLenLine = []
            for subList in lists:
                listsLenLine.append(len(subList))
            print('gF:', lineno(), '|', indInt, 'len:', len(listsLenLine), '|', listsLenLine)
            # qLine1Int = len(qLine[1]) + 2
            # if len(listsLenLine) > qLine1Int:
            #     print('gF:', lineno(), '| printGlobalData() - fuckery -->', 
            #           len(listsLenLine), str(qLine1Int))
            #     input('paused')
        indInt+=1


begin()
print('gloFunk loaded')