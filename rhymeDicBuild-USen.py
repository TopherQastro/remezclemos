#!/usr/local/bin/python3.3

from string import *
import csv
import nltk.corpus
from collections import defaultdict

csv.field_size_limit(int(9999999))

rhyDic0 = defaultdict(list)
rhyDic1 = defaultdict(list)

#  In this emp data, the '1' signifies the dominant stress, which may be confusing
#  since '2' is numerically greater but emphasized quieter, and the '0' remains
#  lesser in both cases...

fCons = 'B', 'D', 'G', 'JH', 'L', 'N', 'P', 'S', 'T', 'V', 'ZH', 'CH', 'DH', 'F', 'HH', 'K', 'M', 'NG', 'R', 'SH', 'TH', 'W', 'Z'
fVocs = ['AA0', 'AH0', 'AW0', 'EH0', 'EY0', 'IH0', 'OW0', 'UH0', 'AE0', 'AO0', 'AY0', 'ER0', 'IY0', 'OY0', 'UW0', 'Y0',
         'AA1', 'AH1', 'AW1', 'EH1', 'EY1', 'IH1', 'OW1', 'UH1', 'AE1', 'AO1', 'AY1', 'ER1', 'IY1', 'OY1', 'UW1', 'Y1']
         

phonoFile = open('data/USen/phonoLib-USen.txt', "r")


print('rhyDic start')
for line in phonoFile:
    dicData = line[:-1].split(' ')
    theseVocs = []
    for each in dicData[2:]:
        if '2' in each:
            thisVoc = each.replace('2', '1')
        else:
            thisVoc = each
        theseVocs.append(thisVoc)
    #print(dicData[0].lower(), theseVocs)
    rhyDic0[dicData[0].lower()] = theseVocs
    rhyDic1[dicData[0].lower()] = theseVocs
print('rhyDic complete')


totalVs = int(1)


def rhyMaker(totalVs, rSyls):
    tName = str(totalVs)
    rName = str(rSyls)
    if totalVs < 10:
        tName = '0'+tName
    if rSyls < 10:
        rName = '0'+rName
    try:
        libFile = csv.reader(open('data/USen/rhymes/alt/rhymeLib-t'+tName+"r"+rName+".csv", "r"))
        print('rhymeLib-t'+tName+"r"+rName+" already exists")
    except IOError:
        dicFile = csv.writer(open('data/USen/rhymes/alt/rhymeLib-t'+tName+"r"+rName+".csv", 'w+', encoding='latin-1'))
        print('rhymeLib-t'+tName+"r"+rName+" beginning....")
        yaFound = []
        thisRhyDic = {}
        for key, val in rhyDic0.items():
            keyList, valList = [], []
            keyString, valString = str(), str()
            if key not in yaFound:
                #print('finding:', key, val)
                vocCount  = int(0)
                presentVocs = []
                for all in fVocs:
                    if all in val:
                        #print('voc:', all)
                        presentVocs.append(all)
                        vocCount+=val.count(all)
                        #if val.count(all) > 1:
                            #print('FLAG THIS')
                #print('vocCount=', vocCount)
                if vocCount >= totalVs:
                    if vocCount == totalVs:
                        valList.append(key)
                    else:
                        keyList.append(key)
                    vocList = []
                    for all in presentVocs:
                        #print('trying:', all)
                        vocIndexer, vocTarget = int(0), int(0)
                        try:
                            while vocIndexer < totalVs:
                                #print(vocTarget, vocIndexer)
                                vocTarget=val[vocIndexer:].index(all)
                                vocList.append(vocTarget+vocIndexer)
                                vocIndexer+=(vocTarget+1)
                        except IndexError:
                            #print('iE')
                            vocIndexer = totalVs
                            continue
                        except ValueError:
                            #print('vE')
                            continue
                    vocList.sort()
                    #print('vocSpots:', key, val, vocList)
                    try:
                        rCutter = val[vocList[-rSyls]:]
                        #print('rCutter:', rCutter)
                        yaFound.append(key)
                        for key, val in rhyDic1.items():
                            try:
                                #print('tester:', key, val[-len(rCutter):])
                                if val[-len(rCutter):] == rCutter:
                                    #print('match found:', key)
                                    yaFound.append(key)
                                    vocCount = int(0)
                                    for all in fVocs:
                                        if all in val:
                                            vocCount+=val.count(all)
                                    #print('vocCount:', vocCount, totalVs, rSyls)
                                    if vocCount >= totalVs:
                                        if vocCount == totalVs:
                                            valList.append(key)
                                            # print('addVal')
                                        else:
                                            keyList.append(key)
                                        #print('addKey')
                            except IndexError:
                                continue
                        #print('foundthese', len(keyList), len(valList))
                    except IndexError:
                        continue
                #print('writing to file:', len(keyList), len(valList))
                if len(valList) > 0:
                    for all in keyList:
                        keyString+=(all+'^')
                    for all in valList:
                        valString+=(all+'^')
                    #print(keyString, valString)
                    dicFile.writerow([keyString[:-1], valString[:-1]])
        print('rhyDic complete')


for totalVs in range(1, 11):
    for rSyls in range(1, 11):
        if rSyls <= totalVs:
            rhyMaker(totalVs, rSyls)
