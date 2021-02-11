
import globalFunctions as gF

def dynaDataWriter(lang, dynaList, textFile, dynaType):
    dynaFile = csv.writer(open(lang+'/data/textLibrary/textData/dynasaurus/'+textFile+'-'+dynaType+'.csv', 'w+'))
    dynaSaurus = {}
    for key, val in dynaList.items():
        svVal = str()
        for each in val:
            svVal = svVal+'^'
        dynaFile.writerow([pWord, svVal]) 
    #dynaFile.close()
    return dynaSaurus


def dynaDataOpener(lang, textFile, dynaType):
    dynaFile = csv.reader(open(lang+'/data/textLibrary/textData/dynasaurus/'+textFile+'-'+dynaType+'.csv', 'r'))
    dynaSaurus = {}
    for line in dynaFile:
        dynaSaurus[line[0]] = line[1].split('^')
    return dynaSaurus

def thisThesLoad():
    try:
        thesaurusFile = gF.csv.reader(open(gF.lang+'/data/textLibrary/textData/'
                                        +gF.textFile+'-thesaurusFile.csv', 'r'))
        print(gF.lineno(), 'loading thesDic...')
        for line in thesaurusFile:
            thesWords = line[1].split('^')
            gF.thesDic[line[0]] = []
            for all in thesWords:
                if (len(all) > 0) and (all not in gF.allPunx) and (all != line[0]):
                    gF.thesDic[line[0]].append(all)
            
        except FileNotFoundError:
            print(gF.lineno(), 'building thesDic...')
            thesaurusFile = gF.csv.writer(open(gF.lang+'/data/textLibrary/textData/'+gF.textFile+'-thesaurusFile.csv', 'w+'))
            for all in gF.splitText:
                finalList = []
                try:
                    #print('\n.\n')
                    gF.thesDic[all]  #  Test to see if the thesaurus has an entry already
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
                        gF.thesDic[all] = finalList
                        thesLine = str()
                        for each in finalList:
                            thesLine+=(each+'^')
                        thesaurusFile.writerow([all, thesLine[:-1]])
                    except ValueError:
                        print('ValueError:', all)
                        continue