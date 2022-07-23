from ast import Num
import os
import csv

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from NPC import NPC

class BetterNPCGenerator():

    presetsFilePath = "resources\\presets\\"
    occupationsFilePath = "resources\\occupations"
    namesFilePath = "resources\\names"

    leftStartColumn = 0
    middleStartColumn = 1
    rightStartColumn = 4



    def __init__(self):
        self.root = Tk()
        self.root.title("The Better Unplanned NPC Generator")

        self.raceTraitsOptions = self.loadOptionsFromFile(self.presetsFilePath + "Default.csv")
        self.npcHistoryList = []

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

        # On Click of another preset in list: reload options
        # File name will be [ OptionName + ".csv" ] in resources>presets



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
        
        occupations =  os.listdir(self.occupationsFilePath)
        self.occupationTypeOptions = ["Any"]
        for occupation in occupations:
            self.occupationTypeOptions.append(str.removesuffix(occupation,".csv"))
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

        #savePresetButton = Button(options, text='Test Presets',command=self.buildPresetsMenu(presets, "Default.csv"))
        #savePresetButton.grid(row=10,column=self.middleStartColumn+1,columnspan=2)



        # ========================= #
        # Right Column: NPC Display #
        # ========================= #

        self.npcFrame = LabelFrame(self.root, text='NPC')
        rightColumnTop = self.npcFrame
        rightColumnTop.grid(row=0,column=self.rightStartColumn,sticky='NWES') 

        self.nameLabel = Label(self.npcFrame, text='Click "Generate NPC"',font='Arial 18 bold',width=20)
        self.nameLabel.grid(row=0,column=self.rightStartColumn,columnspan=2)
        self.occupationLabel = Label(self.npcFrame)
        self.occupationLabel.grid(row=1,column=self.rightStartColumn,columnspan=2)
        self.raceLabel = Label(self.npcFrame)
        self.raceLabel.grid(row=2,column=self.rightStartColumn,columnspan=2)
        self.ageLabel = Label(self.npcFrame)
        self.ageLabel.grid(row=3,column=self.rightStartColumn,columnspan=2)
        self.genderLabel = Label(self.npcFrame)
        self.genderLabel.grid(row=4,column=self.rightStartColumn,columnspan=2)
        self.heightLabel = Label(self.npcFrame)
        self.heightLabel.grid(row=5,column=self.rightStartColumn,columnspan=2)
        self.bodyTypeLabel = Label(self.npcFrame)
        self.bodyTypeLabel.grid(row=6,column=self.rightStartColumn,columnspan=2)
        self.eyeColorLabel = Label(self.npcFrame)
        self.eyeColorLabel.grid(row=7,column=self.rightStartColumn,columnspan=2)
        self.skinLabel = Label(self.npcFrame)
        self.skinLabel.grid(row=8,column=self.rightStartColumn,columnspan=2)
        self.attribute1Label = Label(self.npcFrame)
        self.attribute1Label.grid(row=9,column=self.rightStartColumn,columnspan=2)
        self.attribute2Label = Label(self.npcFrame)
        self.attribute2Label.grid(row=10,column=self.rightStartColumn,columnspan=2)
        self.attribute3Label = Label(self.npcFrame)
        self.attribute3Label.grid(row=11,column=self.rightStartColumn,columnspan=2)

        exportNPCButton = Button(self.npcFrame, text='Export to File', command=self.saveNPC, width=20)
        exportNPCButton.grid(row=20,column=self.rightStartColumn,padx=5, pady=5, ipadx=5, ipady=5)

        copyNPCButton = Button(self.npcFrame, text='Copy to Clipboard', command=self.copyNPC, width=20)
        copyNPCButton.grid(row=20,column=self.rightStartColumn+1, padx=(0,5), pady=5, ipadx=5, ipady=5)

        npcHistory = LabelFrame(self.root, text='History')
        rightColumnBottom = npcHistory
        rightColumnBottom.grid(row=2,column=self.rightStartColumn,sticky='NWES') 

        Label(npcHistory, text='Last 10 NPCs Generated').grid(row=4,column=self.rightStartColumn)
        self.npcHistoryBox = Listbox(npcHistory,width=47,activestyle="none",font=('Courier New',8))
        self.npcHistoryBox.grid(row=5,column=self.rightStartColumn)
        self.npcHistoryBox.bind("<<ListboxSelect>>", self.recallNPC)



        self.root.mainloop()




     # Helper Methods #   

    def generateNPC(self):

        npc = NPC(  self.raceTraitsOptions,
                    self.raceChoice.get(),
                    self.genderChoice.get(),
                    self.lifeStageChoice.get(),
                    self.occupationTypeChoices.get(),
                    "", #profession
                    self.cultureChoice.get()    )

        self.updateNPCUI(npc)

    def updateNPCUI(self, npc):

        self.currentNPC = npc

        self.nameLabel.configure(text=npc.nameDisplay)
        self.occupationLabel.configure(text=npc.occupationDisplay)
        self.raceLabel.configure(text=npc.raceDisplay)
        self.ageLabel.configure(text=npc.ageDisplay)
        self.genderLabel.configure(text=npc.genderDisplay)
        self.heightLabel.configure(text=npc.heightDisplay)
        self.bodyTypeLabel.configure(text=npc.bodyTypeDisplay)
        self.eyeColorLabel.configure(text=npc.eyeColorDisplay)
        self.skinLabel.configure(text=npc.skinDisplay)
        self.attribute1Label.configure(text=npc.attribute1Display)
        self.attribute2Label.configure(text=npc.attribute2Display)
        self.attribute3Label.configure(text=npc.attribute3Display)

        self.updateNPCHistory(npc)

    def updateNPCHistory(self, npc):
        if (npc not in self.npcHistoryList):
            if (len(self.npcHistoryList) >= 10):
                self.npcHistoryList.pop()
        else:
            self.npcHistoryList.remove(npc)

        self.npcHistoryList.insert(0,npc)

        # Clear and repopulate box
        self.npcHistoryBox.delete(0,END)
        for x, n in enumerate(self.npcHistoryList):
            name = n.nameDisplay[0:25] + self.spacer(n.nameDisplay, 25) + " | " + n.race + " " + n.gender
            self.npcHistoryBox.insert(x, name)
        self.npcHistoryBox.select_set(0)

    def recallNPC(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            npc = self.npcHistoryList[index]
            self.updateNPCUI(npc)
        self.npcHistoryBox.select_set(0)

    def saveNPC(self):
        npc = self.getCurrentNPC()
        if (npc == NONE):
            return

        file = filedialog.asksaveasfilename(filetypes=[("txt file", ".txt")],defaultextension=".txt", initialfile=npc.nameDisplay)
        if file:  # user selected file
            fob = open(file, 'w')
            for line in npc.npcDisplayText:
                fob.write(line + '\n')
            fob.close()

    def copyNPC(self):
        npc = self.getCurrentNPC()
        if (npc == NONE):
            return

        self.root.clipboard_clear
        for line in npc.npcDisplayText:
            self.root.clipboard_append(line + "\n")
        
        messagebox.showinfo("NPC Copied", npc.nameDisplay + " has been copied to the clipboard.")


    def getCurrentNPC(self):
        if (len(self.npcHistoryList) == 0):
            errorMessage = "No NPCs currently loaded."
            messagebox.showerror("NPC Save Error", errorMessage)
            return NONE
        else:
            return self.npcHistoryList[0]
    
    
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


    def spacer(self, text, width):
        spaces = ""
        num = width - len(text)

        for _ in range(num):
            spaces = spaces + " "

        return spaces

