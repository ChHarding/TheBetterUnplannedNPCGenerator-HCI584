import os
import csv

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

from NPC import NPC

class BetterNPCGenerator():

    presetsFilePath = "resources\\presets\\"
    occupationTypesFilePath = "resources\\occupations"
    namesFilePath = "resources\\names"

    leftStartColumn = 0
    middleStartColumn = 1
    rightStartColumn = 4



    def __init__(self):
        self.root = Tk()
        self.root.title("The Better Unplanned NPC Generator")

        self.raceTraitsOptions = self.loadOptionsFromFile(self.presetsFilePath + "Default.csv")
        self.npcHistoryList = []

        self.headerFont = font.Font(family="Century Schoolbook", size=10, weight="bold")

        self.optionsLabelFont = font.Font(family="Century Schoolbook", size=10, weight="bold")
        self.optionsMenuFont = font.Font(family="Century Gothic", size=9)
        self.optionsTextFont = font.Font(family="Centure Gothic", size=11)

        # ==================== #
        # Left Column: Presets #
        # ==================== #

        # Set up 3 Column structure
        self.selectPreset = LabelFrame(self.root, text='Select Preset', font=self.headerFont)
        leftColumn = self.selectPreset
        leftColumn.grid(row=0, column=self.leftStartColumn, rowspan=50, padx=5, pady=5, ipadx=5, ipady=5, sticky='NWES') 

        presets = os.listdir(self.presetsFilePath)

        self.selectedPreset = StringVar()
        self.buildPresetsMenu(presets, "Default.csv")

        # On Click of another preset in list: reload options
        # File name will be [ OptionName + ".csv" ] in resources>presets



        # ====================== #
        # Middle Column: Options #
        # ====================== #

        self.optionsRowCounter = 0

        self.options = LabelFrame(self.root, text="Options", font=self.headerFont)
        middleColumn = self.options
        middleColumn.grid(row=0, column=self.middleStartColumn, rowspan=50, columnspan=3, padx=5, pady=5, ipadx=5, ipady=5, sticky="NWES") 

        optionsInstructions = Label(self.options, text='Choose your options, then click "Generate NPC"', font=self.optionsTextFont)
        optionsInstructions.grid(row=self.optionsRowCounter,column=self.middleStartColumn,columnspan=3)

        self.optionsRowCounter += 1

        # Race
        self.raceOptions = ["Any"]
        for race in self.raceTraitsOptions:
            self.raceOptions.append(race[0])

        self.raceChoice = StringVar()
        self.raceChoice.set("Any")

        self.raceDropDown = self.configureOptionsDropDownMenu("Race", self.raceChoice, self.raceOptions)

        # Gender
        self.genderOptions = ["Any","Male","Female","Nonbinary"]
        #TODO: Load from CSV to allow user to configure custom genders
        self.genderChoice = StringVar()
        self.genderChoice.set("Any")

        self.genderDropDown = self.configureOptionsDropDownMenu("Gender", self.genderChoice, self.genderOptions)

        # Life Stage 
        self.lifeStageOptions = ["Any","Child","Adolescent","Young Adult","Adult","Elder"] 
        #TODO: Load from the preset header label
        self.lifeStageChoice = StringVar()
        self.lifeStageChoice.set("Any")

        self.lifeStageDropDown = self.configureOptionsDropDownMenu("Life Stage", self.lifeStageChoice, self.lifeStageOptions)


        # Occupation
        occupations =  os.listdir(self.occupationTypesFilePath)
        self.occupationTypeOptions = ["Any"]
        for occupation in occupations:
            self.occupationTypeOptions.append(str.removesuffix(occupation,".csv"))
        self.occupationTypeChoice = StringVar()
        self.occupationTypeChoice.set("Any")

        self.occupationTypeDropDown = self.configureOptionsDropDownMenu("Occupation Type", self.occupationTypeChoice, self.occupationTypeOptions, )

        # Profession
        self.professionTypeOptions = ["Any"]
        self.professionTypeChoice = StringVar()
        self.professionTypeChoice.set("Any")

        self.professionTypeDropDown = self.configureOptionsDropDownMenu("Profession", self.professionTypeChoice, self.professionTypeOptions)
        self.professionTypeDropDown.configure(state=DISABLED)


        # Culture
        self.cultureChoice = StringVar()
        self.cultureChoice.set("Any")

        self.configureOptionsLabel("Name Culture")
        self.optionsRowCounter += 1

        self.cultureChoicesFrame = Frame(self.options)
        self.cultureChoicesFrame.grid(row=self.optionsRowCounter,column=self.middleStartColumn,columnspan=3)
        self.configureRadioOptions(self.cultureChoicesFrame, self.cultureChoice, ["Any","Common","Traditional"])
        self.optionsRowCounter += 1


        # Buttons
        generateNPCButton = Button(self.options, text='Generate NPC',command=self.generateNPC,width=15,font=("Arial",12,"bold"))
        generateNPCButton.grid(row=self.optionsRowCounter,column=self.middleStartColumn,columnspan=3, padx=5, pady=5, ipadx=5, ipady=5)



        # ========================= #
        # Right Column: NPC Display #
        # ========================= #

        self.npcFrame = LabelFrame(self.root, text='NPC', font=self.headerFont)
        rightColumnTop = self.npcFrame
        rightColumnTop.grid(row=0,column=self.rightStartColumn,sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5) 

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


        # NPC History Panel
        npcHistory = LabelFrame(self.root, text='History')
        rightColumnBottom = npcHistory
        rightColumnBottom.grid(row=2,column=self.rightStartColumn,sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5) 

        Label(npcHistory, text='Last 10 NPCs Generated').grid(row=4,column=self.rightStartColumn)
        self.npcHistoryBox = Listbox(npcHistory,width=47,activestyle="none",font=('Courier New',8))
        self.npcHistoryBox.grid(row=5,column=self.rightStartColumn)
        self.npcHistoryBox.bind("<<ListboxSelect>>", self.recallNPC)



        self.root.mainloop()




     # Helper Methods #   

    def configureOptionsLabel(self, labelText):
        label = Label(self.options, text=labelText, justify="left", anchor="w", font=self.optionsLabelFont)
        label.grid(row=self.optionsRowCounter, column=self.middleStartColumn, sticky="w", padx=5, pady=5, ipadx=5, ipady=5)

    def configureOptionsDropDownMenu(self, labelText, variable, menuOptions, command=""):
        self.configureOptionsLabel(labelText)
        menu = OptionMenu(self.options, variable, *menuOptions, command=command)
        menu.configure(font=self.optionsMenuFont)
        menu.configure(width=30)
        ddMenu = self.root.nametowidget(menu.menuname)
        ddMenu.config(font=self.optionsMenuFont)
        menu.grid(row=self.optionsRowCounter, column=self.middleStartColumn+1, columnspan=2, sticky="ew", padx=5, pady=5, ipadx=2, ipady=2)
        self.optionsRowCounter += 1
        return menu

    def configureRadioOption(self, radioFrame, text, variable, value):
        radio = Radiobutton(radioFrame, text=text, variable=variable, value=value, font=self.optionsTextFont)
        radio.pack(side="left",anchor="w")

    def configureRadioOptions(self, frame, variable, options):
        if (options[0] is tuple):
            for option in options:
                self.configureRadioOption(frame, option[0], variable, option[1])
        else:
            for option in options:
                self.configureRadioOption(frame, option, variable, option)
        
        






    def generateNPC(self):

        npc = NPC(  self.raceTraitsOptions,
                    self.raceChoice.get(),
                    self.genderChoice.get(),
                    self.lifeStageChoice.get(),
                    self.occupationTypeChoice.get(),
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

