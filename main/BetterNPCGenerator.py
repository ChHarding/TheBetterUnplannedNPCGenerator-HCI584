from cProfile import label
import os
from tkinter import *

from sqlalchemy import column
from NPC import NPC
import csv

class BetterNPCGenerator():

    presetsFilePath = "main\\resources\\presets\\"
    namesFilePath = "main\\resources\\names"

    leftStartColumn = 0
    middleStartColumn = 1
    rightStartColumn = 4

    def __init__(self):
        self.root = Tk()
        self.root.title("The Better Unplanned NPC Generator")

        self.raceTraitsOptions = self.loadOptionsFromFile(self.presetsFilePath + "Default.csv")

        # ==================== #
        # Left Column: Presets #
        # ==================== #

        # Set up 3 Column structure
        self.selectPreset = LabelFrame(self.root, text='Select Preset')
        leftColumn = self.selectPreset
        leftColumn.grid(row=0, column=self.leftStartColumn, rowspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='NWES') 

        presets = os.listdir(self.presetsFilePath)

        self.selectedPreset = StringVar()
        self.buildPresetsMenu(presets, "Default.csv")

        # Label(selectPreset, text='Default').grid(row=0,column=self.leftStartColumn)
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

        # Occupation
        self.occupationTypeOptions = ["Any"]
        #TODO: Load from a file
        self.occupationTypeChoices = StringVar()
        self.occupationTypeChoices.set("Any")

        occupationTypeDropDownLabel = Label(options,text="Occupation Type")
        occupationTypeDropDownLabel.grid(row=4,column=self.middleStartColumn)
        self.occupationTypeDropDown = OptionMenu(options, self.occupationTypeChoices, *self.occupationTypeOptions) 
        #TODO: Make into multi-select option to allow user to select from a range
        self.occupationTypeDropDown.grid(row=4,column=self.middleStartColumn+1)


        # Lifestyle
        self.lifestyleTypeOptions = ["Any"]
        #TODO: Load from a file
        self.lifestyleTypeChoices = StringVar()
        self.lifestyleTypeChoices.set("Any")

        lifestyleTypeDropDownLabel = Label(options,text="Lifestyle")
        lifestyleTypeDropDownLabel.grid(row=5,column=self.middleStartColumn)
        self.lifestyleTypeDropDown = OptionMenu(options, self.lifestyleTypeChoices, *self.lifestyleTypeOptions) 
        #TODO: Make into multi-select option to allow user to select from a range
        self.lifestyleTypeDropDown.grid(row=5,column=self.middleStartColumn+1)




        # Culture
        self.cultureChoice = StringVar()
        self.cultureChoice.set("Any")

        cultureLabel = Label(options,text="Name Culture",justify="left",anchor="w")
        cultureLabel.grid(row=6,column=self.middleStartColumn,columnspan=3,sticky="w")

        anyRadio = Radiobutton(options,text="Any",variable=self.cultureChoice,value="Any")
        anyRadio.grid(row=7,column=self.middleStartColumn)

        commonRadio = Radiobutton(options,text="Common",variable=self.cultureChoice,value="Common")
        commonRadio.grid(row=7,column=self.middleStartColumn+1)

        traditionalRadio = Radiobutton(options,text="Traditional",variable=self.cultureChoice,value="Traditional")
        traditionalRadio.grid(row=7,column=self.middleStartColumn+2)


        # Buttons
        generateNPCButton = Button(options, text='Generate NPC',command=self.generateNPC)
        generateNPCButton.grid(row=10,column=self.middleStartColumn,columnspan=2)

        savePresetButton = Button(options, text='Test Presets',command=self.buildPresetsMenu(presets, "Default.csv"))
        savePresetButton.grid(row=10,column=self.middleStartColumn+1,columnspan=2)



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
        self.heightLabel = Label(npcFrame, text="Height: ")
        self.heightLabel.grid(row=4,column=self.rightStartColumn)
        self.bodyTypeLabel = Label(npcFrame, text="Body Type: ")
        self.bodyTypeLabel.grid(row=5,column=self.rightStartColumn)
        self.eyeColorLabel = Label(npcFrame)
        self.eyeColorLabel.grid(row=6,column=self.rightStartColumn)
        self.skinLabel = Label(npcFrame)
        self.skinLabel.grid(row=7,column=self.rightStartColumn)
        self.attribute1Label = Label(npcFrame)
        self.attribute1Label.grid(row=8,column=self.rightStartColumn)
        self.attribute2Label = Label(npcFrame)
        self.attribute2Label.grid(row=9,column=self.rightStartColumn)
        self.attribute3Label = Label(npcFrame)
        self.attribute3Label.grid(row=10,column=self.rightStartColumn)

        Button(npcFrame, text='Export NPC').grid(row=20,column=self.rightStartColumn)

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
                    self.occupationTypeChoices.get(),
                    self.lifestyleTypeChoices.get(),
                    self.cultureChoice.get()    )

        self.nameLabel.configure(text=npc.name[0] + " " + npc.name[1])
        self.raceLabel.configure(text="Race: " + npc.race)
        self.ageLabel.configure(text="Age: " + npc.age + " (" + npc.lifeStage + ")")
        self.genderLabel.configure(text="Gender: " + npc.gender)
        self.heightLabel.configure(text="Height: " + npc.height)
        self.bodyTypeLabel.configure(text="Body Type: " + npc.bodyType)
        self.eyeColorLabel.configure(text="Eye Color: " + npc.eyeColor)
        self.skinLabel.configure(text=npc.raceSkinLabel + npc.primaryColor)
        self.attribute1Label.configure(text=npc.att1Label + npc.att1Property)
        self.attribute2Label.configure(text=npc.att2Label + npc.att2Property)
        self.attribute3Label.configure(text=npc.att3Label + npc.att3Property)

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
    
    def buildPresetsMenu(self, values, select):
        for item in self.selectPreset.winfo_children():
            item.destroy()
        displayRow = 0
        for text in values:
            radio = Radiobutton(self.selectPreset, text = str.removesuffix(text,".csv"), variable = self.selectedPreset,
                value = text, indicator = 0,
                background = "light blue")
            radio.grid(row=displayRow,column=self.leftStartColumn)
            displayRow = displayRow + 1
        self.selectedPreset.set(select)
            


