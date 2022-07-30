import os
import csv

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

from NPC import NPC

class BetterNPCGenerator():

    # Folders & Filepaths #
    
    # TODO Migrate folders and file paths to a settings file instead of hard-coding.
    #      When this is complete, implement its use with the NPC class also.

    raceTraitsFileName = "Races.csv"
    defaultOptionsFileName = "Default.csv"
    genderOptionsFileName = "Genders.csv"

    generationCriteriaFolder = "generation-criteria\\"
    namesFolderPath = generationCriteriaFolder + "names\\"
    occupationTypesFolderPath = generationCriteriaFolder + "occupations\\"
    presetsFolderPath = generationCriteriaFolder + "presets\\"

    raceTraitsFilePath = generationCriteriaFolder + raceTraitsFileName
    genderOptionsFilePath = generationCriteriaFolder + genderOptionsFileName
    defaultOptionsFilePath = presetsFolderPath + defaultOptionsFileName

    # Panel Column Numbers #
    leftStartColumn = 0
    middleStartColumn = 1
    rightStartColumn = 4

    ##########
    # Colors #
    ##########

    # TODO Migrate style definitions to a separate module

    # Primary Colors
    inkBlack = "#27221f"
    veryLightParchment = "#fefdfb"
    lightParchment = "#f5f0e5"
    parchment = "#f0e6d1"
    darkParchment = "#efdfbb"

    # Accent Colors
    lycheeRed = "#bb2f43"
    ashGray = "#6f7678"

    # Assigned Colors
    defaultTextColor = inkBlack
    defaultBackgroundColor = lightParchment

    buttonColor = lycheeRed
    buttonTextColor = veryLightParchment

    presetButtonColor = darkParchment
    presetButtonTextColor = inkBlack
    presetButtonSelectedColor = veryLightParchment
    presetButtonHoverColor = parchment

    dropDownColor = darkParchment
    dropDownHoverColor = parchment
    dropDownTextColor = inkBlack
    dropDownExpandedHoverColor = ashGray
    dropDownExpandedHoverTextColor = veryLightParchment

    npcNameColor = lycheeRed

    npcHistoryColor = veryLightParchment
    npcHistorySelectColor = ashGray
    npcHistorySelectTextColor = veryLightParchment

    def __init__(self):

        # Initialize Tk Root
        self.root = Tk()
        self.root.title("The Better Unplanned NPC Generator")
        self.root.configure(bg=self.defaultBackgroundColor)

        #########
        # Fonts #
        #########

        self.headerFont = font.Font(family="Century Schoolbook", size=10, weight="bold")
        self.buttonFont = font.Font(family="Century Schoolbook", size=10, weight="bold")

        self.generateButtonFont = font.Font(family="Century Schoolbook", size=12, weight="bold")

        self.presetsFont = font.Font(family="Century Gothic",size=11)

        self.optionsLabelFont = font.Font(family="Century Schoolbook", size=10, weight="bold")
        self.optionsMenuFont = font.Font(family="Century Gothic", size=9, weight="bold")
        self.optionsTextFont = font.Font(family="Century Gothic", size=11)
        
        self.npcNameFont = font.Font(family="Century Schoolbook", size=15, weight="bold")
        self.npcDisplayFont = font.Font(family="Century Gothic", size=9)

        self.historyTextFont = font.Font(family="Century Gothic", size=9)


        # Load Races File and Default Preset #
        self.raceTraitsFile = self.loadOptionsFromCsv(self.raceTraitsFilePath, TRUE, TRUE)
        self.raceTraitsFile.sort()

        self.raceTraits = self.raceTraitsFile.copy()

        self.raceOptionsFile = []
        self.raceOptionsFile = self.loadOptionsFromCsv(self.defaultOptionsFilePath, TRUE, TRUE)

        self.npcHistoryList = []
    
        
        # ==================== #
        # Left Column: Presets #
        # ==================== #

        self.selectPreset = LabelFrame(self.root, text="Presets", font=self.headerFont,background=self.defaultBackgroundColor, foreground=self.defaultTextColor)
        leftColumn = self.selectPreset
        leftColumn.grid(row=0, column=self.leftStartColumn, rowspan=50, padx=5, pady=5, ipady=5, sticky='NWES') 

        presets = os.listdir(self.presetsFolderPath)
        presets.sort()
        presets.remove(self.defaultOptionsFileName)
        presets.insert(0,self.defaultOptionsFileName)
        self.selectedPreset = StringVar()
        self.configurePresetsMenu(presets, self.defaultOptionsFileName)


        # ====================== #
        # Middle Column: Options #
        # ====================== #

        # NOTE: Place all options menu configurations in desired 
        # display order and make sure row counter gets updated after each.

        # Row counter is automatically updated with the 
        # configureOptionsDropDownMenu method.
       
        # TODO Make this counter more robust
        self.optionsRowCounter = 0

        self.options = LabelFrame(self.root, text="Options", font=self.headerFont,background=self.defaultBackgroundColor, foreground=self.defaultTextColor)
        middleColumn = self.options
        middleColumn.grid(row=0, column=self.middleStartColumn, rowspan=50, columnspan=3, padx=5, pady=5, sticky="NWES") 

        optionsInstructions = Label(self.options, text='Choose your options, then click "Generate NPC"', font=self.optionsTextFont, background=self.defaultBackgroundColor, foreground=self.defaultTextColor)
        optionsInstructions.grid(row=self.optionsRowCounter,column=self.middleStartColumn,columnspan=3, pady=(10,5))

        self.optionsRowCounter += 1


        # Race
        self.raceOptions = ["Any"]
        self.raceWeights = []
        self.loadRaceOptionsAndWeights()
        self.raceChoice = StringVar()
        self.raceChoice.set("Any")

        self.raceDropDown = self.configureOptionsDropDownMenu("Race", self.raceChoice, self.raceOptions)


        # Gender
        self.genderOptions = self.loadOptionsFromCsv(self.genderOptionsFilePath, FALSE)
        self.genderOptions.insert(0,"Any")
        self.genderChoice = StringVar()
        self.genderChoice.set("Any")

        self.genderDropDown = self.configureOptionsDropDownMenu("Gender", self.genderChoice, self.genderOptions)


        # Life Stage 
        self.lifeStageOptions = ["Any","Child","Adolescent","Young Adult","Adult","Elder"] 
        #TODO: Load from a file
        self.lifeStageChoice = StringVar()
        self.lifeStageChoice.set("Any")

        self.lifeStageDropDown = self.configureOptionsDropDownMenu("Life Stage", self.lifeStageChoice, self.lifeStageOptions)


        # Occupation
        occupations =  os.listdir(self.occupationTypesFolderPath)
        self.occupationTypeOptions = ["Any"]
        for occupation in occupations:
            self.occupationTypeOptions.append(str.removesuffix(occupation,".csv"))
        self.occupationTypeChoice = StringVar()
        self.occupationTypeChoice.set("Any")

        self.occupationTypeDropDown = self.configureOptionsDropDownMenu("Occupation Type", self.occupationTypeChoice, self.occupationTypeOptions, self.updateProfessionsMenu)


        # Profession
        self.professionTypeOptions = ["Any"]
        self.professionTypeChoice = StringVar()
        self.professionTypeChoice.set("Any")

        self.professionTypeDropDown = self.configureOptionsDropDownMenu("Profession", self.professionTypeChoice, self.professionTypeOptions)
        self.professionTypeDropDown.configure(state=DISABLED)


        # Culture
        self.cultureChoice = StringVar()
        self.cultureChoice.set("Any")

        self.configureOptionsLabel("Name Culture",padding=(5,(5,0),2,2))
        self.optionsRowCounter += 1

        self.cultureChoicesFrame = Frame(self.options)
        self.cultureChoicesFrame.grid(row=self.optionsRowCounter,column=self.middleStartColumn,columnspan=3)
        self.configureRadioOptions(self.cultureChoicesFrame, self.cultureChoice, ["Any","Common","Traditional"])
        self.optionsRowCounter += 1


        # Buttons
        generateNPCButton = Button(self.options, text='Generate NPC',command=self.generateNPC,width=15,font=self.generateButtonFont, background=self.buttonColor, foreground=self.buttonTextColor)
        generateNPCButton.grid(row=self.optionsRowCounter,column=self.middleStartColumn,columnspan=3, padx=5, pady=5, ipadx=5, ipady=5)



        # ========================= #
        # Right Column: NPC Display #
        # ========================= #

        # NOTE: Place all NPC Display rows in display order 
        # and make sure row counter gets updated after each.
        
        # Row counter is automatically updated with the 
        # configureNPCDisplayField method.
       
        # TODO Make this counter more robust
        self.npcDisplayRowCount = 0

        self.npcFrame = LabelFrame(self.root, text='NPC', font=self.headerFont, background=self.defaultBackgroundColor, foreground=self.defaultTextColor)
        rightColumnTop = self.npcFrame
        rightColumnTop.grid(row=self.npcDisplayRowCount,column=self.rightStartColumn, sticky='NWES', padx=5, pady=5) 

        self.nameLabel = self.configureNPCDisplayField()
        self.nameLabel.configure(text='Click "Generate NPC"')
        self.nameLabel.configure(foreground=self.npcNameColor)
        self.nameLabel.configure(font=self.npcNameFont)

        self.occupationLabel = self.configureNPCDisplayField()
        self.raceLabel = self.configureNPCDisplayField()
        self.ageLabel = self.configureNPCDisplayField()
        self.genderLabel = self.configureNPCDisplayField()
        self.heightLabel = self.configureNPCDisplayField()
        self.bodyTypeLabel = self.configureNPCDisplayField()
        self.eyeColorLabel = self.configureNPCDisplayField()
        self.skinLabel = self.configureNPCDisplayField()
        self.attribute1Label = self.configureNPCDisplayField()
        self.attribute2Label = self.configureNPCDisplayField()
        self.attribute3Label = self.configureNPCDisplayField()

        # Buttons
        exportNPCButton = Button(self.npcFrame, text='Export to File', command=self.saveNPC, width=15, font=self.buttonFont, background=self.buttonColor, foreground=self.buttonTextColor)
        exportNPCButton.grid(row=self.npcDisplayRowCount,column=self.rightStartColumn,padx=5, pady=5, ipadx=5, ipady=5)

        copyNPCButton = Button(self.npcFrame, text='Copy to Clipboard', command=self.copyNPC, width=15, font=self.buttonFont, background=self.buttonColor, foreground=self.buttonTextColor)
        copyNPCButton.grid(row=self.npcDisplayRowCount,column=self.rightStartColumn+1, padx=(0,5), pady=5, ipadx=5, ipady=5)


        ###################################
        # Right Column: NPC History Panel #
        ###################################

        npcHistory = LabelFrame(self.root, text='History', font=self.headerFont, background=self.defaultBackgroundColor, foreground=self.defaultTextColor)
        rightColumnBottom = npcHistory
        rightColumnBottom.grid(row=2,column=self.rightStartColumn,sticky='NWES', padx=5, pady=5) 

        Label(npcHistory, text='Last 10 NPCs Generated', font=self.historyTextFont, background=self.defaultBackgroundColor).grid(row=4,column=self.rightStartColumn,pady=(5,0))
        self.npcHistoryBox = Listbox(npcHistory,activestyle="none",font=('Courier New',10),width=38,height=10,borderwidth=0,background=self.npcHistoryColor,foreground=self.defaultTextColor,selectbackground=self.npcHistorySelectColor,selectforeground=self.npcHistorySelectTextColor)
        self.npcHistoryBox.grid(column=self.rightStartColumn, columnspan=3,sticky="ew", pady=5, padx=5, ipadx=5, ipady=5)
        self.npcHistoryBox.bind("<<ListboxSelect>>", self.recallNPC)


        ####################
        # MAIN LOOP BEGINS #
        ####################

        # NOTE: All UI initialization should occur above this section #
        self.root.mainloop()




    ##################
    # Helper Methods #   
    ##################

    def configureOptionsLabel(self, labelText, padding=(5,5,2,2)):
        label = Label(self.options, text=labelText, justify="left", anchor="w", font=self.optionsLabelFont, background=self.defaultBackgroundColor, foreground=self.defaultTextColor)
        label.grid(row=self.optionsRowCounter, column=self.middleStartColumn, sticky="w", padx=padding[0], pady=padding[1], ipadx=padding[2], ipady=padding[3])

    def configureOptionsDropDownMenu(self, labelText, variable, menuOptions, command=""):
        self.configureOptionsLabel(labelText)
        menu = OptionMenu(self.options, variable, *menuOptions, command=command)
        menu.configure(font=self.optionsMenuFont)
        menu.configure(width=30)
        menu.configure(background=self.dropDownColor)
        menu.configure(foreground=self.dropDownTextColor)
        menu.configure(borderwidth=0)
        menu.configure(activebackground=self.dropDownHoverColor)
        ddMenu = self.root.nametowidget(menu.menuname)
        ddMenu.config(font=self.optionsMenuFont)
        ddMenu.config(background=self.dropDownHoverColor)
        ddMenu.config(activebackground=self.dropDownExpandedHoverColor)
        menu.grid(row=self.optionsRowCounter, column=self.middleStartColumn+1, columnspan=2, sticky="ew", padx=5, pady=5, ipadx=2, ipady=2)
        self.optionsRowCounter += 1
        return menu

    def configureRadioOption(self, radioFrame, text, variable, value):
        radio = Radiobutton(radioFrame, text=text, variable=variable, value=value, font=self.optionsTextFont, background=self.defaultBackgroundColor)
        radio.pack(side="left",anchor="w")

    def configureRadioOptions(self, frame, variable, options):
        if (options[0] is tuple):
            for option in options:
                self.configureRadioOption(frame, option[0], variable, option[1])
        else:
            for option in options:
                self.configureRadioOption(frame, option, variable, option)

    def configureNPCDisplayField(self):
        label = Label(self.npcFrame, background=self.defaultBackgroundColor, font=self.npcDisplayFont, foreground=self.defaultTextColor)
        label.grid(row=self.npcDisplayRowCount,column=self.rightStartColumn,columnspan=2)
        self.npcDisplayRowCount += 1
        return label

    def configurePresetsMenu(self, values, select):
        for item in self.selectPreset.winfo_children():
            item.destroy()
        displayRow = 0
        for text in values:
            radio = Radiobutton(self.selectPreset, text = str.removesuffix(text,".csv"), variable = self.selectedPreset,
                value = text, indicator = 0,
                background = self.presetButtonColor,
                foreground = self.presetButtonTextColor,
                activebackground = self.presetButtonSelectedColor,
                borderwidth=0,
                relief=FLAT,
                font=self.presetsFont)
            radio.grid(row=displayRow,column=self.leftStartColumn,sticky="ew", padx=5, pady=2, ipadx=7, ipady=2)
            radio.configure(command=lambda: self.updateRaceOptions(self.selectedPreset.get()))
            displayRow += 1
        self.selectedPreset.set(select)


    def updateProfessionsMenu(self, selection):
        if (selection != "Any"):
            self.professionTypeOptions = self.loadOptionsFromCsv(self.occupationTypesFolderPath + selection + ".csv", TRUE)
            self.updateOptionsMenu(self.professionTypeDropDown, self.professionTypeChoice, self.professionTypeOptions)            
            self.professionTypeDropDown.configure(state=ACTIVE)
        else:
            self.professionTypeDropDown.configure(state=DISABLED)
        self.professionTypeChoice.set("Any")

    def updateRaceOptions(self, presetName):
        self.raceTraits.clear()
        self.raceOptions.clear()
        self.raceWeights.clear()
        
        self.raceOptionsFile = self.loadOptionsFromCsv(self.presetsFolderPath + presetName, TRUE, TRUE)
        self.loadRaceOptionsAndWeights()
        
        # Reload raceTraits
        for raceTrait in self.raceTraitsFile:
            for raceOption in self.raceOptions:
                if (raceTrait[0] == raceOption):
                    self.raceTraits.append(raceTrait)

        self.updateOptionsMenu(self.raceDropDown, self.raceChoice, self.raceOptions)

    def updateOptionsMenu(self, optionMenu, variable, newOptions):
        menu = optionMenu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="Any", 
                             command=lambda value="Any": variable.set(value))
        for string in newOptions:
            s = string
            if (isinstance(string,list)):
                s = string[0]
            menu.add_command(label=s, 
                             command=lambda value=s: variable.set(value))
        variable.set("Any")
    
    
    def generateNPC(self):

        npc = NPC(  self.raceTraits,
                    self.raceChoice.get(),
                    self.raceWeights,
                    self.genderChoice.get(),
                    self.lifeStageChoice.get(),
                    self.occupationTypeChoice.get(),
                    self.professionTypeChoice.get(),
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
            name = " " + n.nameDisplay[0:20] + self.spacer(n.nameDisplay, 20) + " | " + n.race + " " + n.gender
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
        if file:
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
    
    
    def loadOptionsFromCsv(self, filePath, sort=TRUE, skipHeader=FALSE):
        file = open(filePath)
        reader = csv.reader(file)

        if (skipHeader):
            next(reader)

        items = []
        for item in reader:
            items.append(item)

        if (sort):
            items.sort()

        file.close()

        return items

    def loadRaceOptionsAndWeights(self):
        for race in self.raceOptionsFile:
            if (len(race[0]) > 0):
                self.raceOptions.append(race[0])
            else:
                self.raceOptions.append(race)
            weight = 0
            try:
                weight = float(race[1])
            except:
                weight = ""
            self.raceWeights.append(weight)

    def spacer(self, text, width):
        spaces = ""
        num = width - len(text)

        for _ in range(num):
            spaces = spaces + " "

        return spaces

