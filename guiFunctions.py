
import globalFunctions as gF

class GUIstart:
    def __init__(self, master):
        #1: Create a builder
        self.builder = builder = gF.pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('wemyx-pygubuGUI.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('Toplevel_2', master)
        
        self.textFile = self.builder.get_object('textFile')
        self.poemQuota = self.builder.get_object('poemQuota')
        self.stanzaQuota = self.builder.get_object('stanzaQuota')
        self.defaultSwitch = self.builder.get_variable('defaultSwitch')
        self.langBox = self.builder.get_variable('langBox')
        self.accent = self.builder.get_variable('accent')

        self.rhy0 = self.builder.get_object('rhy0')
        self.rhy1 = self.builder.get_object('rhy1')
        self.rhy2 = self.builder.get_object('rhy2')
        self.rhy3 = self.builder.get_object('rhy3')
        self.rhy4 = self.builder.get_object('rhy4')
        self.rhy5 = self.builder.get_object('rhy5')
        self.rhy6 = self.builder.get_object('rhy6')
        self.rhy7 = self.builder.get_object('rhy7')

        self.emp0 = self.builder.get_object('emp0')
        self.emp1 = self.builder.get_object('emp1')
        self.emp2 = self.builder.get_object('emp2')
        self.emp3 = self.builder.get_object('emp3')
        self.emp4 = self.builder.get_object('emp4')
        self.emp5 = self.builder.get_object('emp5')
        self.emp6 = self.builder.get_object('emp6')
        self.emp7 = self.builder.get_object('emp7')

        self.metSwitch = self.builder.get_variable('metSwitch')
        self.metSwitch.set(True)  #  Are these statements overriding choice in GUI?
        self.rhySwitch = self.builder.get_variable('rhySwitch')
        self.rhySwitch.set(True)
        self.thesSwitch = self.builder.get_variable('thesSwitch')
        self.thesSwitch.set(True)
        self.usedSwitch = self.builder.get_variable('usedSwitch')

        self.proxMinDial = self.builder.get_object('proxMinDial')
        self.proxMaxDial = self.builder.get_object('proxMaxDial')
        self.punxDial = self.builder.get_object('punxDial')

        self.Text_1 = self.builder.get_object('Text_1')

        builder.connect_callbacks(self)

        callbacks = {
            'start_click': self.clickButton
            #'reset': self.clickButton 
            }

        builder.connect_callbacks(callbacks)

    def clickButton(self):
        gF.defaultSwitch = self.defaultSwitch.get()

        gF.textFile = self.textFile.get()
        gF.poemQuota = self.poemQuota.get()
        gF.poemQuota = int(gF.poemQuota)
        gF.stanzaQuota = self.stanzaQuota.get()
        gF.stanzaQuota = int(gF.stanzaQuota)
        gF.language = self.langBox.get()
        gF.accent = self.accent.get()
        print(gF.language)
        if gF.language == 'English':
            gF.lang = 'eng'
        elif gF.language == 'Espanol':
            gF.lang = 'esp'
        gF.lang = 'eng'
        print(gF.lang)
        rhyMap = str()
        rhyMap+=self.rhy0.get()
        rhyMap+=self.rhy1.get()
        rhyMap+=self.rhy2.get()
        rhyMap+=self.rhy3.get()
        rhyMap+=self.rhy4.get()
        rhyMap+=self.rhy5.get()
        rhyMap+=self.rhy6.get()
        rhyMap+=self.rhy7.get()

        empBuildr = list()
        empBuildr+=[self.emp0.get()]
        empBuildr+=[self.emp1.get()]
        empBuildr+=[self.emp2.get()]
        empBuildr+=[self.emp3.get()]
        empBuildr+=[self.emp4.get()]
        empBuildr+=[self.emp5.get()]
        empBuildr+=[self.emp6.get()]
        empBuildr+=[self.emp7.get()]
        if '' in empBuildr:
            cutPoint = empBuildr.index('')
            empBuildr = empBuildr[:cutPoint]
        empMap = []
        for each in empBuildr:
            thisEmpLine = []
            for all in each:
                if all == '0':
                    thisEmpLine.append(False)
                else:
                    thisEmpLine.append(True)
            empMap.append(thisEmpLine)
        
        gF.empKey = empMap
        gF.rhyMap = rhyMap

        gF.metSwitch = self.metSwitch.get()
        gF.rhySwitch = self.rhySwitch.get()
        gF.thesSwitch = self.thesSwitch.get()
        gF.usedSwitch = self.usedSwitch.get()

        gF.proxMinDial = int(self.proxMinDial.get())
        gF.proxMaxDial = int(self.proxMaxDial.get())
        gF.punxDial = int(self.punxDial.get())

        gF.rawtextFunk.gov()
        writtenPoem = gF.poemFunk.gov()
        print('Poem:\n', writtenPoem)
        #input('paused')
    

def start():
    print('gui: | 0')
    root = gF.tk.Tk()
    print('gui: | 1')
    app = GUIstart(root)
    print('gui: | 2')
    root.mainloop()



