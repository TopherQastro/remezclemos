nums = '1', '2', '0'

vocs = 'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW'
cons = 'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N', 'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH'

fonoFile = list(open('USen-primaryFono.txt', 'r'))
print('fonoLen:', len(fonoFile))
newFonoFile = open('fonoLib-NEW.txt', 'x')
newVocsFile = open('vocsLib-NEW.txt', 'x')
newConsFile = open('consLib-NEW.txt', 'x')
newEmpsFullFile = open('empsFullLib-NEW.txt', 'x')
newEmpsEvenFile = open('empsEvenLib-NEW.txt', 'x')
newEmpsUnikFile = open('empsUnikLib-NEW.txt', 'x')
doublesFile = open('doubleList.txt', 'x')
doubList = []
contractionFile = open('contractionList.txt', 'x')
contractionList = []

def doubBuild(doublesFile):
    print('beginning doubles build')
    for line in fonoFile:
        line = line.replace('\n', '')
        commaSpot = line.index(' ')
        word = word = line[:commaSpot].lower()
        if '(1)' in word:
            doubList.append(word[:-3])
            print('double:', word[:-3])
            doublesFile.write(word[:-3]+'\n')
    return doubList


def fonoBuild(doubles):
    print('starting')
    for line in fonoFile:
        print(line)
        line = line.replace('\n', '')
        commaSpot = line.index(' ')
        word = line[:commaSpot].lower()
        print(word)
        if word in doubList:
            print('doubled:', word)
            word = word+'(0)'
        if ("'" in word) and (word[-2:] != "'s") and (word[-1] != "'"):
            contractionFile.write(word+'\n')
        fono = line[commaSpot+2:]
        fono = fono.replace(' ', '^')
        empString = str()
        for eachChar in fono:
            if eachChar in nums:
                empString+=eachChar
        print(empString)
        newEmpsFullFile.write(word+','+empString+'\n')
        for num in nums:
            fono = fono.replace(num, '')
        newLine = word+','+fono+'\n'
        newFonoFile.write(newLine)
        print(newLine.replace('\n', ''))
        vocsAndCons = fono.split('^')
        theseVocs = []
        theseCons = []
        for bits in vocsAndCons:
            if bits in vocs:
                theseVocs.append(bits)
            elif bits in cons:
                theseCons.append(bits)
            else:
                print('dunno this sound:', bits)
        vocString = str()
        for theVocs in theseVocs:
            vocString+=theVocs+'^'
        newVocsFile.write(word+','+vocString[:-1]+'\n')
        print(vocString[:-1])
        conString = str()
        for theCons in theseCons:
            conString+=theCons+'^'
        newConsFile.write(word+','+conString[:-1]+'\n')
        print(conString[:-1])
    newFonoFile.close()
    newVocsFile.close()
    newConsFile.close()
    newEmpsFullFile.close()
    newEmpsEvenFile.close()
    newEmpsUnikFile.close()
    doublesFile.close()
    contractionFile.close()
            
doubLisnt = doubBuild(doublesFile)
print('building fonoFiles')
fonoBuild(doubList)
