
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

    