import globalFunctions as gF

def testAlts(pWord, altNum):
    altEmps = []
    altLet = str(altNum)
    altWord = pWord+'('+altLet+')'
    altNum+=1
    try:
        altEmps = emps[altWord]
    except KeyError:
        altNum = 2000

    return altEmps, altNum


def contractionLoad():
    contractionFile = open(gF.lang+'/data/'+gF.accent+'/contractionList.txt', 'r')
    contractionSwitch = gF.csv.reader(open(gF.lang+'/data/'+gF.accent+'/contractionSwitches.csv', 'r+'))
    for line in contractionFile:  #  Makes a dictionary of contractions
        gF.contractionList.append(line[:-1])  #  Remove '\n' before appending
    print(gF.lineno(), 'len(contractionList):', len(gF.contractionList), 
            gF.contractionList[:10])
    try:
        for line in contractionSwitch:
            #if "'s" not in line[0]:  #  There's a problem with whether the line is a possessive or contraction of "___ is"
            gF.contDic[line[0]] = line[1]
    except IndexError:
        gF.contDic = dd(list)
    #print(gF.contDic)
    print(gF.lineno(), 'len(contractionDic):', len(gF.contDic), 
            gF.contDic["can't"], gF.contDic["don't"])