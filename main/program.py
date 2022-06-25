from tkinter import *

from sqlalchemy import column
from NPC import NPC
import csv

class BetterNPCGenerator():

    optionsFilePath = "main\\resources\\presets\\"
    namesFilePath = "main\\resources\\names"

    leftStartColumn = 0
    middleStartColumn = 1
    rightStartColumn = 4

    def __init__(self):
        self.root = Tk()

        self.raceTraitsOptions = self.loadOptionsFromFile(self.optionsFilePath + "Race Traits - Default.csv")

        for race in self.raceTraitsOptions:
            print(race)



        # ==================== #
        # Left Column: Presets #
        # ==================== #

        # Set up 3 Column structure
        selectPreset = LabelFrame(self.root, text='Select Preset')
        leftColumn = selectPreset
        leftColumn.grid(row=0, column=self.leftStartColumn, rowspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='NWES') 

        Label(selectPreset, text='Default').grid(row=0,column=self.leftStartColumn)
        # On Click of another preset in list: reload options
        # File name will be [ "Race Traits - " + OptionName + ".csv" ] in resources>presets



        # ====================== #
        # Middle Column: Options #
        # ====================== #

        options = LabelFrame(self.root, text='Options')
        middleColumn = options
        middleColumn.grid(row=0, column=self.middleStartColumn, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='NWES') 

        optionsInstructions = Label(options, text='Choose your options, then click "Generate NPC"')
        optionsInstructions.grid(row=0,column=self.middleStartColumn,columnspan=3)

        # Race
        self.raceOptions = ["Any"]
        for race in self.raceTraitsOptions:
            self.raceOptions.append(race[0])

        self.raceChoice = StringVar()
        self.raceChoice.set("Any")

        raceDropDownLabel = Label(options,text="Race")
        raceDropDownLabel.grid(row=1,column=self.middleStartColumn)
        self.raceDropDown = OptionMenu(options, self.raceChoice, *self.raceOptions)
        self.raceDropDown.grid(row=1,column=self.middleStartColumn+1)

        # Gender
        self.genderOptions = ["Any","Male","Female","Nonbinary"]
        #TODO: Load from CSV to allow user to configure custom genders
        self.genderChoice = StringVar()
        self.genderChoice.set("Any")

        genderDropDownLabel = Label(options,text="Gender")
        genderDropDownLabel.grid(row=2,column=self.middleStartColumn)
        self.genderDropDown = OptionMenu(options, self.genderChoice, *self.genderOptions)
        self.genderDropDown.grid(row=2,column=self.middleStartColumn+1)

        # Life Stage 
        self.lifeStageOptions = ["Any","Child","Adolescent","Young Adult","Adult","Elder"] 
        #TODO: Load from the preset header label
        self.lifeStageChoice = StringVar()
        self.lifeStageChoice.set("Any")

        lifeStageDropDownLabel = Label(options,text="Life Stage")
        lifeStageDropDownLabel.grid(row=3,column=self.middleStartColumn)
        self.lifeStageDropDown = OptionMenu(options, self.lifeStageChoice, *self.lifeStageOptions) 
        #TODO: Make into multi-select option to allow user to select from a range
        self.lifeStageDropDown.grid(row=3,column=self.middleStartColumn+1)

        # Culture
        self.cultureOptions = ["Any","Male","Female","Nonbinary"]
        self.cultureChoice = StringVar()
        self.cultureChoice.set("Any")

        cultureLabel = Label(options,text="Name Culture",justify="left",anchor="w")
        cultureLabel.grid(row=4,column=self.middleStartColumn,columnspan=3,sticky="w")

        anyRadio = Radiobutton(options,text="Any",variable=self.cultureChoice,value="Any")
        anyRadio.grid(row=5,column=self.middleStartColumn)

        commonRadio = Radiobutton(options,text="Common",variable=self.cultureChoice,value="Common")
        commonRadio.grid(row=5,column=self.middleStartColumn+1)

        traditionalRadio = Radiobutton(options,text="Traditional",variable=self.cultureChoice,value="Traditional")
        traditionalRadio.grid(row=5,column=self.middleStartColumn+2)

        generateNPCButton = Button(options, text='Generate NPC',command=self.generateNPC)
        generateNPCButton.grid(row=10,column=self.middleStartColumn,columnspan=2)



        # ========================= #
        # Right Column: NPC Display #
        # ========================= #

        npcFrame = LabelFrame(self.root, text='NPC')
        rightColumnTop = npcFrame
        rightColumnTop.grid(row=0,column=self.rightStartColumn,sticky='NWES') 

        self.nameLabel = Label(npcFrame, text='Click "Generate NPC"',font='Arial 18 bold')
        self.nameLabel.grid(row=0,column=self.rightStartColumn)
        self.raceLabel = Label(npcFrame, text="Race: ")
        self.raceLabel.grid(row=1,column=self.rightStartColumn)
        self.ageLabel = Label(npcFrame, text="Age: ")
        self.ageLabel.grid(row=2,column=self.rightStartColumn)
        self.genderLabel = Label(npcFrame, text="Gender: ")
        self.genderLabel.grid(row=3,column=self.rightStartColumn)

        Button(npcFrame, text='Export NPC').grid(row=4,column=self.rightStartColumn)

        npcHistory = LabelFrame(self.root, text='History')
        rightColumnBottom = npcHistory
        rightColumnBottom.grid(row=2,column=self.rightStartColumn,sticky='NWES') 

        testList = ('NPC1', 'NPC2', 'NPC3', 'NPC4', 'NPC5')

        Label(npcHistory, text='Last 5 NPCs Generated').grid(row=4,column=self.rightStartColumn)
        Listbox(npcHistory,listvariable=testList).grid(row=5,column=self.rightStartColumn)



        self.root.mainloop()

    def generateNPC(self):

        npc = NPC(  self.raceTraitsOptions,
                    self.raceChoice.get(),
                    self.genderChoice.get(),
                    self.lifeStageChoice.get(),
                    self.cultureChoice.get()    )


        self.nameLabel.configure(text=npc.name[0] + " " + npc.name[1])
        self.raceLabel.configure(text="Race: " + npc.race)
        self.ageLabel.configure(text="Age: " + npc.age)
        self.genderLabel.configure(text="Gender: " + npc.gender)

        #updateNPCHistory(npc)

    def updateNPCHistory(npc):
        # Update the NPC History
        return None

    def loadOptionsFromFile(self, optionsFileName):
        optionsPresetFile = open(optionsFileName)

        optionsReader = csv.reader(optionsPresetFile)

        next(optionsReader) # Remove header values from returned results

        raceTraits = []
        for race in optionsReader:
            raceTraits.append(race)

        optionsPresetFile.close()

        return raceTraits
        
    def refreshOptionsForm(self, options):
        self.raceDropDown.configure(values=options)


app = BetterNPCGenerator()