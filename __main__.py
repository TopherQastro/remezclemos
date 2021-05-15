
print('_m_: PROGRAM INITIALIZED')

import globalFunctions as gF

def main__init():
    print('_m_:',  gF.lineno(), 'beginning main__init')
    gF.guiFunk.start()
    print('_m_:', gF.lineno(), 'exiting main__init')

fonoDics, fullList = gF.fonoFunk.fonoBuild_USen()
gF.fonoFunk.fonoBuild_SQLmain(fonoDics, fullList)
main__init()

print('_m_ | PROGRAM FINISHED')
